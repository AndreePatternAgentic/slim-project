
# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
import os
import json
import asyncio
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import slim_bindings
from .state import (
    OutputState,
    AgentState,
    StatelessAgentState,
    StatelessOutputState,
    Message,
    Type as MsgType,
)
# Google AI API configuration (much easier than Vertex AI!)
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY must be set as an environment variable. Get it from https://aistudio.google.com/app/apikey")
is_stateless = os.getenv("STATELESS", "true").lower() == "true"
# Use Google AI API (Gemini) - much simpler!
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=google_api_key,
    temperature=0,
    max_retries=3,
)
print(f"Using Google AI API with model: {model_name}")
# Writer and subject role prompts
MARKETING_EMAIL_PROMPT_TEMPLATE = PromptTemplate.from_template(
    """
You are a highly skilled writer and you are working for a marketing company.
Your task is to write formal and professional emails. We are building a publicity campaign and we need to send a massive number of emails to many clients.
The email must be compelling and adhere to our marketing standards.
Based on the information provided, create a complete marketing email immediately. Do not ask for additional information - work with what you have and create a professional, engaging email.
The email must be engaging and persuasive. The subject line cannot exceed 5 words (no bold).
The email should be in the following format:
{{separator}}
subject
body
{{separator}}
IMPORTANT RULES:
- ALWAYS generate a complete email with the separator format shown above
- DO NOT ask for more information - create the email with the details provided
- DO NOT FORGET TO ADD THE SEPARATOR BEFORE THE SUBJECT AND AFTER THE EMAIL BODY!
- NEVER put a separator after the subject and before the email body!
- DO NOT ADD EXTRA TEXT - only generate the email in the specified format
""",
    template_format="jinja2",
)
# HELLO_MSG = ("Hello! I'm here to assist you in crafting a compelling marketing email "
#     "that resonates with your audience. To get started, could you please provide "
#     "some details about your campaign, such as the target audience, key message, "
#     "and any specific goals you have in mind?")
EMPTY_MSG_ERROR = (
    "Oops! It seems like you're trying to start a conversation with silence. ",
    "An empty message is only allowed if your email is marked complete. Otherwise, let's keep the conversation going! ",
    "Please share some details about the email you want to get.",
)
SEPARATOR = "**************"
# SLIM configuration
SLIM_SERVER_ADDRESS = os.getenv("SLIM_SERVER_ADDRESS", "http://slim-server:12345")
# Global SLIM client instance
slim_client = None
async def init_slim_client():
    """Initialize SLIM client for mailcomposer agent."""
    global slim_client
    if slim_client is None:
        slim_bindings.init_tracing({"log_level": "info"})
        slim_client = await slim_bindings.Slim.new("agntcy", "mailcomposer", "composer")
        await slim_client.connect({
            "endpoint": SLIM_SERVER_ADDRESS,
            "tls": {"insecure": True}
        })
        await slim_client.set_route("agntcy", "mailcomposer", "validator")
        print(f"SLIM client initialized - connected to {SLIM_SERVER_ADDRESS}")
    return slim_client
async def validate_email_via_slim(email_content: str) -> dict:
    """Send email to validator via SLIM and get validation result."""
    try:
        # Initialize SLIM client if needed
        slim = await init_slim_client()
        
        # Create request-response session
        session = await slim.create_session(
            slim_bindings.PySessionConfiguration.RequestResponse()
        )
        
        # Prepare request
        request = json.dumps({"email_content": email_content})
        
        # Send request and wait for response with timeout
        try:
            session_info, response = await asyncio.wait_for(
                slim.request_reply(
                    session,
                    request.encode(),
                    "agntcy",
                    "mailcomposer",
                    "validator"
                ),
                timeout=10.0  # 10 second timeout
            )
        except asyncio.TimeoutError:
            print("SLIM validation timed out after 10 seconds")
            return {
                "is_valid": True,
                "message": "Validation timed out - email accepted by default"
            }
        
        # Parse response
        validation_result = json.loads(response.decode())
        print(f"Email validation via SLIM - Valid: {validation_result.get('is_valid', False)}")
        
        return validation_result
        
    except Exception as e:
        print(f"SLIM validation error: {e}")
        # Return default validation result on error
        return {
            "is_valid": True,
            "message": f"Validation unavailable: {e}"
        }
def format_email(state):
    answer = interrupt(
        Message(
            type=MsgType.assistant,
            content="In what format would like your email to be?",
        )
    )
    state.messages = (state.messages or []) + [Message(**answer)]
    state_after_formating = generate_email(state)
    interrupt(
        Message(
            type=MsgType.assistant, content="The email is formatted, please confirm"
        )
    )
    state_after_formating = StatelessAgentState(
        **state_after_formating, is_completed=True
    )
    return final_output(state_after_formating)

def extract_mail(messages) -> str:
    for m in reversed(messages):
        splits: list[str] = []
        if isinstance(m, Message):
            if m.type == MsgType.human:
                continue
            splits = m.content.split(SEPARATOR)
        if isinstance(m, dict):
            if m.get("type", "") == "human":
                continue
            splits = m.get("content", "").split(SEPARATOR)
        if len(splits) >= 3:
            return splits[len(splits) - 2].strip()
        elif len(splits) == 2:
            return splits[1].strip()
        elif len(splits) == 1:
            return splits[0]
    return ""

def should_format_email(state: AgentState | StatelessAgentState):
    if state.is_completed and not is_stateless:
        return "format_email"
    return END

def convert_messages(messages: list) -> list[BaseMessage]:
    converted = []
    for m in messages:
        if isinstance(m, Message):
            mdict = m.model_dump()
        else:
            mdict = m
        if mdict["type"] == "human":
            converted.append(HumanMessage(content=mdict["content"]))
        else:
            converted.append(AIMessage(content=mdict["content"]))
    return converted

# Define mail_agent function
def email_agent(
    state: AgentState | StatelessAgentState,
) -> OutputState | AgentState | StatelessOutputState | StatelessAgentState:
    """This agent is a skilled writer for a marketing company, creating formal and professional emails for publicity campaigns.
    It interacts with users to gather the necessary details.
    Once the user approves by sending "is_completed": true, the agent outputs the finalized email in "final_email".
    """
    # Check subsequent messages and handle completion
    return final_output(state) if state.is_completed else generate_email(state)

def final_output(
    state: AgentState | StatelessAgentState,
) -> OutputState | AgentState | StatelessOutputState | StatelessAgentState:
    final_mail = extract_mail(state.messages)
    output_state: OutputState = OutputState(
        messages=state.messages,
        is_completed=state.is_completed,
        final_email=final_mail,
    )
    return output_state

def generate_email(
    state: AgentState | StatelessAgentState,
) -> (
    OutputState | AgentState | StatelessOutputState | StatelessAgentState
):  # Append messages from state to initial prompt
    messages = [
        Message(
            type=MsgType.human,
            content=MARKETING_EMAIL_PROMPT_TEMPLATE.format(separator=SEPARATOR),
        )
    ] + state.messages
    # Call the LLM
    ai_message = Message(
        type=MsgType.ai, content=str(llm.invoke(convert_messages(messages)).content)
    )
    
    # Validate email via SLIM if validation is enabled
    validation_enabled = os.getenv("ENABLE_SLIM_VALIDATION", "true").lower() == "true"
    if validation_enabled:
        try:
            # Extract email content for validation
            email_content = ai_message.content
            
            # Validate via SLIM (handle async properly)
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, create a task
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, validate_email_via_slim(email_content))
                        validation_result = future.result(timeout=30)
                else:
                    # If no loop running, use asyncio.run
                    validation_result = asyncio.run(validate_email_via_slim(email_content))
            except:
                # Fallback: disable validation for this request
                validation_result = {"is_valid": True, "message": "Validation skipped"}
            
            # Add validation feedback to the message
            if not validation_result.get("is_valid", True):
                validation_msg = f"\n\n[Validation: {validation_result.get('message', 'Issues found')}]"
                ai_message.content += validation_msg
                
        except Exception as e:
            print(f"Email validation failed: {e}")
            # Continue without validation on error
    if is_stateless:
        return {"messages": state.messages + [ai_message]}
    else:
        return {"messages": [ai_message]}

if is_stateless:
    graph_builder = StateGraph(StatelessAgentState, output=StatelessOutputState)
else:
    graph_builder = StateGraph(AgentState, output=OutputState)
graph_builder.add_node("email_agent", email_agent)
graph_builder.add_node("format_email", format_email)
graph_builder.add_edge(START, "email_agent")
# This node will only be added in stateful mode since langgraph requires checkpointer if any node should interrupt
graph_builder.add_conditional_edges("email_agent", should_format_email)
graph_builder.add_edge("format_email", END)
graph_builder.add_edge("email_agent", END)

if is_stateless:
    print("mailcomposer - running in stateless mode")
    graph = graph_builder.compile()
else:
    print("mailcomposer - running in stateful mode")
    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)


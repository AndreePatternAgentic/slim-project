#!/usr/bin/env python3
"""
Question Agent - AI-powered question generation using Google AI
Based on the exact working pattern from authenticated_agents.py
"""

import asyncio
import os
import sys
import time
import slim_bindings
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def create_authenticated_agent(org, ns, agent_name, secret):
    """Create an authenticated agent using SharedSecret pattern - EXACT COPY"""
    print(f"Creating authenticated agent: {org}/{ns}/{agent_name}")
    
    # Initialize tracing
    slim_bindings.init_tracing({
        "log_level": "info",
        "opentelemetry": {"enabled": False},
    })
    
    # Create agent with authentication (like the working tests)
    provider = slim_bindings.PyIdentityProvider.SharedSecret(
        identity=agent_name, shared_secret=secret
    )
    verifier = slim_bindings.PyIdentityVerifier.SharedSecret(
        identity=agent_name, shared_secret=secret
    )
    
    agent = await slim_bindings.Slim.new(
        org, ns, agent_name, provider, verifier
    )
    
    agent_id = agent.get_agent_id()
    print(f"✅ Agent created with ID: {agent_id}")
    
    # Connect to SLIM server (using insecure like the tests)
    endpoint = os.getenv('SLIM_ENDPOINT', 'http://127.0.0.1:46357')
    await agent.connect({
        "endpoint": endpoint, 
        "tls": {"insecure": True}
    })
    
    print(f"✅ Agent connected to SLIM server")
    return agent, agent_id

def init_google_ai():
    """Initialize Google AI"""
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY environment variable is required")
    
    genai.configure(api_key=api_key)
    model_name = os.getenv('GOOGLE_AI_MODEL', 'gemini-1.5-flash')
    model = genai.GenerativeModel(model_name)
    print(f"✅ Google AI initialized with model: {model_name}")
    return model

async def generate_ai_question(model, conversation_count=0):
    """Generate AI question"""
    try:
        topics = os.getenv('CONVERSATION_TOPICS', 'technology,science,philosophy,creativity,problem-solving').split(',')
        
        prompt = f"""Generate an interesting, thought-provoking question for a conversation. 

Guidelines:
- Make it engaging and open-ended
- Topics can include: {', '.join(topics)}
- Keep it concise (one sentence)
- Avoid yes/no questions
- Make it suitable for an AI assistant to answer

This is question #{conversation_count + 1} in the conversation.

Question:"""
        
        print(f"🧠 Generating question #{conversation_count + 1}")
        response = await asyncio.to_thread(model.generate_content, prompt)
        question = response.text.strip()
        
        # Clean up the question
        if question.startswith('"') and question.endswith('"'):
            question = question[1:-1]
        
        print(f"✅ Generated question: '{question}'")
        return question
        
    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return f"What's your perspective on artificial intelligence and its impact on society?"

async def run_question_agent():
    """Run Question Agent (sender) with AI - EXACT PATTERN from authenticated_agents.py"""
    print("=== AI-Powered Question Agent - Sender ===")
    
    # Configuration
    org = os.getenv('SLIM_ORG', 'cisco')
    ns = os.getenv('SLIM_NAMESPACE', 'default')
    agent_a_name = 'question_agent'
    agent_b_name = 'answer_agent'
    secret = os.getenv('SLIM_SECRET', 'shared_secret_123')
    
    # Agent behavior configuration
    question_interval = int(os.getenv('QUESTION_INTERVAL', '15'))
    max_questions = int(os.getenv('MAX_CONVERSATION_LENGTH', '10'))
    
    # Initialize Google AI
    model = init_google_ai()
    
    # Create Agent A - EXACT SAME as authenticated_agents.py
    agent_a, agent_a_id = await create_authenticated_agent(org, ns, agent_a_name, secret)
    
    print(f"\n🎯 Question Agent ready: {org}/{ns}/{agent_a_name}")
    print(f"🎯 Agent ID: {agent_a_id}")
    print(f"🎯 Target: {org}/{ns}/{agent_b_name}")
    print(f"🤖 AI-powered question generation enabled")
    print(f"⏱️  Question interval: {question_interval} seconds")
    print()
    
    async with agent_a:
        # Set route to Answer Agent - EXACT SAME as authenticated_agents.py
        print(f"🛤️  Setting route to {org}/{ns}/{agent_b_name}")
        await agent_a.set_route(org, ns, agent_b_name)
        print("✅ Route set")
        
        # Create session - EXACT SAME as authenticated_agents.py
        session = await agent_a.create_session(
            slim_bindings.PySessionConfiguration.FireAndForget()
        )
        print(f"✅ Session created: {session.id}")
        print()
        
        # Conversation loop
        conversation_count = 0
        
        while conversation_count < max_questions:
            try:
                # ONLY CHANGE: Generate AI question instead of hardcoded message
                ai_question = await generate_ai_question(model, conversation_count)
                message = ai_question.encode()
                
                print(f"📤 Question Agent: Sending question #{conversation_count + 1}: '{ai_question}'")
                
                # Send message and wait for reply - EXACT SAME as authenticated_agents.py
                _, reply = await agent_a.request_reply(
                    session, message, org, ns, agent_b_name
                )
                
                reply_text = reply.decode()
                print(f"📨 Question Agent: Received answer: '{reply_text[:150]}{'...' if len(reply_text) > 150 else ''}'")
                print()
                print("🎉 Question-Answer exchange successful!")
                print("✅ AI-powered conversation working!")
                print("=" * 60)
                
                conversation_count += 1
                
                # Wait before next question
                if conversation_count < max_questions:
                    print(f"⏱️  Waiting {question_interval} seconds before next question...")
                    await asyncio.sleep(question_interval)
                
            except Exception as e:
                print(f"❌ Question Agent communication failed: {e}")
                import traceback
                traceback.print_exc()
                break
        
        print(f"\n🎉 Conversation completed! Asked {conversation_count} questions.")
        print("✅ AI-powered agent communication successful!")

if __name__ == "__main__":
    try:
        asyncio.run(run_question_agent())
    except KeyboardInterrupt:
        print("\n🛑 Question Agent stopped")
    except Exception as e:
        print(f"❌ Question Agent failed: {e}")
        import traceback
        traceback.print_exc()
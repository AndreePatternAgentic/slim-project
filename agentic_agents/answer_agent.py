#!/usr/bin/env python3
"""
Answer Agent - AI-powered responses using Google AI
Based on the exact working pattern from authenticated_agents.py
"""

import asyncio
import os
import sys
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

async def generate_ai_response(model, question):
    """Generate AI response to question"""
    try:
        prompt = f"""You are a helpful AI assistant. Provide a thoughtful, concise response to this question:

Question: {question}

Response (keep it conversational and under 200 words):"""
        
        print(f"🧠 Generating AI response for: '{question}'")
        response = await asyncio.to_thread(model.generate_content, prompt)
        answer = response.text.strip()
        print(f"✅ Generated response ({len(answer)} chars)")
        return answer
        
    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return f"I apologize, but I encountered an error processing your question: {str(e)}"

async def run_answer_agent():
    """Run Answer Agent (receiver) with AI - EXACT PATTERN from authenticated_agents.py"""
    print("=== AI-Powered Answer Agent - Receiver ===")
    
    # Configuration
    org = os.getenv('SLIM_ORG', 'cisco')
    ns = os.getenv('SLIM_NAMESPACE', 'default')
    agent_name = 'answer_agent'
    secret = os.getenv('SLIM_SECRET', 'shared_secret_123')
    
    # Initialize Google AI
    model = init_google_ai()
    
    # Create agent - EXACT SAME as authenticated_agents.py
    agent_b, agent_b_id = await create_authenticated_agent(org, ns, agent_name, secret)
    
    print(f"\n🎯 Answer Agent ready: {org}/{ns}/{agent_name}")
    print(f"🎯 Agent ID: {agent_b_id}")
    print("🤖 AI-powered responses enabled")
    print("Waiting for questions...")
    print("=" * 50)
    
    async def handle_session(session_id):
        """Handle messages for a specific session - EXACT PATTERN"""
        while True:
            try:
                print(f"👂 Answer Agent: Waiting for message on session {session_id}")
                session, msg = await agent_b.receive(session=session_id)
                question = msg.decode()
                print(f"📨 Answer Agent: RECEIVED: '{question}'")
                
                # ONLY CHANGE: Use AI instead of hardcoded reply
                ai_reply = await generate_ai_response(model, question)
                reply = f"AI Response: {ai_reply}"
                
                await agent_b.publish_to(session, reply.encode())
                print(f"📤 Answer Agent: SENT AI REPLY: '{reply[:100]}{'...' if len(reply) > 100 else ''}'")
                print("-" * 30)
                
            except Exception as e:
                print(f"❌ Answer Agent session error: {e}")
                break
    
    # Main receiver loop - EXACT SAME as authenticated_agents.py
    async with agent_b:
        while True:
            try:
                print("👂 Answer Agent: Waiting for new session...")
                session_info, _ = await agent_b.receive()
                print(f"🆕 Answer Agent: New session: {session_info.id}")
                
                # Handle session in background
                asyncio.create_task(handle_session(session_info.id))
                
            except Exception as e:
                print(f"❌ Answer Agent main loop error: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_answer_agent())
    except KeyboardInterrupt:
        print("\n🛑 Answer Agent stopped")
    except Exception as e:
        print(f"❌ Answer Agent failed: {e}")
        import traceback
        traceback.print_exc()
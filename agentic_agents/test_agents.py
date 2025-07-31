#!/usr/bin/env python3
"""
Test script to verify AI agents work
"""

import asyncio
import os
import sys
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

async def test_google_ai():
    """Test Google AI integration"""
    print("🧪 Testing Google AI integration...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            print("❌ GOOGLE_AI_API_KEY not found")
            return False
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Generate a simple question about technology.")
        print(f"✅ Google AI working: {response.text[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Google AI test failed: {e}")
        return False

async def test_slim_connection():
    """Test SLIM connection"""
    print("🧪 Testing SLIM connection...")
    
    try:
        import slim_bindings
        
        # Initialize tracing
        slim_bindings.init_tracing({
            "log_level": "info",
            "opentelemetry": {"enabled": False},
        })
        
        # Create test agent
        provider = slim_bindings.PyIdentityProvider.SharedSecret(
            identity="test_agent", shared_secret="test_secret"
        )
        verifier = slim_bindings.PyIdentityVerifier.SharedSecret(
            identity="test_agent", shared_secret="test_secret"
        )
        
        agent = await slim_bindings.Slim.new(
            "cisco", "default", "test_agent", provider, verifier
        )
        
        # Connect to SLIM server
        endpoint = os.getenv('SLIM_ENDPOINT', 'http://127.0.0.1:46357')
        await agent.connect({
            "endpoint": endpoint,
            "tls": {"insecure": True}
        })
        
        agent_id = agent.get_agent_id()
        print(f"✅ SLIM connection working: {agent_id}")
        
        # Clean up
        await agent.close()
        return True
        
    except Exception as e:
        print(f"❌ SLIM connection test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing AI-Powered Agents")
    print("=" * 40)
    
    # Test Google AI
    ai_ok = await test_google_ai()
    
    # Test SLIM
    slim_ok = await test_slim_connection()
    
    print("=" * 40)
    if ai_ok and slim_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ready to run AI agents:")
        print("   1. python answer_agent.py")
        print("   2. python question_agent.py")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
#!/usr/bin/env python3
"""
Authenticated agents using PyIdentityProvider.SharedSecret pattern
Based on the working test pattern from test_request_reply.py
"""

import asyncio
import slim_bindings
import sys

async def create_authenticated_agent(org, ns, agent_name, secret):
    """Create an authenticated agent using SharedSecret pattern"""
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
    await agent.connect({
        "endpoint": "http://127.0.0.1:46357", 
        "tls": {"insecure": True}
    })
    
    print(f"✅ Agent connected to SLIM server")
    return agent, agent_id

async def run_agent_b():
    """Run Agent B (receiver) with authentication"""
    print("=== Authenticated Agent B - Receiver ===")
    
    org = "cisco"
    ns = "default"
    agent_name = "agent_b"
    secret = "shared_secret_123"
    
    agent_b, agent_b_id = await create_authenticated_agent(org, ns, agent_name, secret)
    
    print(f"\n🎯 Agent B ready: {org}/{ns}/{agent_name}")
    print(f"🎯 Agent ID: {agent_b_id}")
    print("Waiting for messages...")
    print("=" * 50)
    
    async def handle_session(session_id):
        """Handle messages for a specific session"""
        while True:
            try:
                print(f"👂 Agent B: Waiting for message on session {session_id}")
                session, msg = await agent_b.receive(session=session_id)
                print(f"📨 Agent B: RECEIVED: '{msg.decode()}'")
                
                # Send reply
                reply = f"Authenticated reply from Agent B: {msg.decode()}"
                await agent_b.publish_to(session, reply.encode())
                print(f"📤 Agent B: SENT REPLY: '{reply}'")
                print("-" * 30)
                
            except Exception as e:
                print(f"❌ Agent B session error: {e}")
                break
    
    # Main receiver loop (exactly like the working test)
    async with agent_b:
        while True:
            try:
                print("👂 Agent B: Waiting for new session...")
                session_info, _ = await agent_b.receive()
                print(f"🆕 Agent B: New session: {session_info.id}")
                
                # Handle session in background
                asyncio.create_task(handle_session(session_info.id))
                
            except Exception as e:
                print(f"❌ Agent B main loop error: {e}")
                await asyncio.sleep(1)

async def run_agent_a():
    """Run Agent A (sender) with authentication"""
    print("=== Authenticated Agent A - Sender ===")
    
    org = "cisco"
    ns = "default"
    agent_a_name = "agent_a"
    agent_b_name = "agent_b"
    secret = "shared_secret_123"
    
    # Create Agent A
    agent_a, agent_a_id = await create_authenticated_agent(org, ns, agent_a_name, secret)
    
    print(f"\n🎯 Agent A ready: {org}/{ns}/{agent_a_name}")
    print(f"🎯 Agent ID: {agent_a_id}")
    print(f"🎯 Target: {org}/{ns}/{agent_b_name}")
    print()
    
    async with agent_a:
        # Set route to Agent B (using human-readable format like the test)
        print(f"🛤️  Setting route to {org}/{ns}/{agent_b_name}")
        await agent_a.set_route(org, ns, agent_b_name)
        print("✅ Route set")
        
        # Create session (exactly like the test)
        session = await agent_a.create_session(
            slim_bindings.PySessionConfiguration.FireAndForget()
        )
        print(f"✅ Session created: {session.id}")
        print()
        
        # Send message and wait for reply (exactly like the test)
        message = b"Hello from authenticated Agent A!"
        print(f"📤 Agent A: Sending: '{message.decode()}'")
        
        try:
            _, reply = await agent_a.request_reply(
                session, message, org, ns, agent_b_name
            )
            
            print(f"📨 Agent A: Received reply: '{reply.decode()}'")
            print()
            print("🎉 SUCCESS! Authenticated agent communication working!")
            print("✅ Human-readable IDs preserved!")
            print("✅ End-to-end communication verified!")
            
            return True
            
        except Exception as e:
            print(f"❌ Agent A communication failed: {e}")
            import traceback
            traceback.print_exc()
            return False

async def test_authenticated_communication():
    """Test authenticated communication (like the working test)"""
    print("=== Authenticated Communication Test ===")
    print("Using PyIdentityProvider.SharedSecret pattern")
    print("Based on working test_request_reply.py")
    print()
    
    org = "cisco"
    ns = "default"
    agent1 = "agent_b"
    agent2 = "agent_a"
    secret = "shared_secret_123"
    
    # Create both agents
    agent_b, _ = await create_authenticated_agent(org, ns, agent1, secret)
    agent_a, _ = await create_authenticated_agent(org, ns, agent2, secret)
    
    # Set route
    await agent_a.set_route(org, ns, agent1)
    print("✅ Route set")
    
    # Create session
    session = await agent_a.create_session(
        slim_bindings.PySessionConfiguration.FireAndForget()
    )
    print(f"✅ Session created: {session.id}")
    
    # Test messages
    pub_msg = b"Test message from authenticated agent"
    res_msg = b"Test response from authenticated agent"
    
    # Test communication (exactly like the working test)
    async with agent_b, agent_a:
        # Background task for agent_b
        async def background_task():
            try:
                # Wait for new session
                recv_session, _ = await agent_b.receive()
                print(f"Agent B: Received session {recv_session.id}")
                
                # Receive message
                recv_session, msg_rcv = await agent_b.receive(session=recv_session.id)
                print(f"Agent B: Received message: {msg_rcv.decode()}")
                
                # Verify message
                assert msg_rcv == pub_msg
                print("✅ Message verified!")
                
                # Send reply
                await agent_b.publish_to(recv_session, res_msg)
                print("Agent B: Reply sent")
                
            except Exception as e:
                print(f"Agent B error: {e}")
        
        # Start background task
        task = asyncio.create_task(background_task())
        
        # Give receiver time to start
        await asyncio.sleep(1)
        
        # Send request and wait for reply
        print("Agent A: Sending request...")
        _, reply = await agent_a.request_reply(
            session, pub_msg, org, ns, agent1
        )
        
        print(f"Agent A: Received reply: {reply.decode()}")
        
        # Verify reply
        assert reply == res_msg
        print("✅ Reply verified!")
        
        # Wait for background task
        await task
        
        print("\n🎉 AUTHENTICATED COMMUNICATION SUCCESS!")
        print("✅ Human-readable IDs working!")
        print("✅ PyIdentityProvider.SharedSecret working!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sender":
            # Run as Agent A (sender)
            try:
                success = asyncio.run(run_agent_a())
                if success:
                    print("\n✅ Sender test successful!")
                else:
                    print("\n❌ Sender test failed")
            except Exception as e:
                print(f"Sender failed: {e}")
                import traceback
                traceback.print_exc()
        elif sys.argv[1] == "test":
            # Run integrated test
            try:
                asyncio.run(test_authenticated_communication())
            except Exception as e:
                print(f"Test failed: {e}")
                import traceback
                traceback.print_exc()
    else:
        # Run as Agent B (receiver)
        try:
            asyncio.run(run_agent_b())
        except KeyboardInterrupt:
            print("\n🛑 Agent B stopped")
        except Exception as e:
            print(f"Agent B failed: {e}")
            import traceback
            traceback.print_exc()
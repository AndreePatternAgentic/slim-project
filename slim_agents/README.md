# SLIM Agent Communication

A working implementation of agent-to-agent communication using AGNTCY's SLIM (Secure Low-Latency Interactive Messaging) data plane server.

## Quick Start

### Prerequisites
1. SLIM data plane server running on `localhost:46357`
2. Python 3.8+ with `slim_bindings` installed (built from source with authentication support)

### Running the Agents

#### Start Agent B (Receiver)
```bash
python authenticated_agents.py
```

#### Send Message from Agent A (Sender)
```bash
python authenticated_agents.py sender
```

#### Run Integrated Test
```bash
python authenticated_agents.py test
```

## What This Demonstrates

- ✅ **Agent-to-Agent Communication** - Two separate processes communicating through SLIM
- ✅ **Authentication** - Using PyIdentityProvider.SharedSecret for secure identity
- ✅ **Message Routing** - Proper routing with human-readable agent IDs
- ✅ **Session Management** - Creating and managing communication sessions
- ✅ **Bidirectional Messaging** - Request-reply pattern with full message exchange

## Current Capabilities

### What the Agents Can Do
- Authenticate with SLIM server using shared secrets
- Route messages to specific agents by ID (`agntcy/default/agent_name`)
- Create sessions for organized conversations
- Send/receive binary messages asynchronously
- Handle multiple concurrent sessions

### What They Cannot Do (Yet)
- AI reasoning (no LLM integration)
- Task execution (no complex workflows)
- Tool usage (no external API calls)
- Memory (no persistent state)

## Architecture

```
┌─────────────────┐    SLIM Protocol    ┌─────────────────┐
│    Agent A      │◄──────────────────►│    Agent B      │
│   (Sender)      │                     │  (Receiver)     │
└─────────────────┘                     └─────────────────┘
         │                                       │
         └───────────────┐       ┌───────────────┘
                         ▼       ▼
                  ┌─────────────────┐
                  │  SLIM Server    │
                  │ localhost:46357 │
                  └─────────────────┘
```

## Next Steps

To evolve this into intelligent agents:
1. Add LLM integration (OpenAI/Anthropic APIs)
2. Implement tool calling abilities
3. Create specialized agent roles
4. Add memory systems
5. Build task planning capabilities

## Files

- **`authenticated_agents.py`** - Main agent implementation
- **`requirements.txt`** - Dependencies (note: slim_bindings must be built from source)
- **`README.md`** - This file

This provides the foundational infrastructure for distributed AI agent systems - the "plumbing" is working, agents can communicate reliably through SLIM.
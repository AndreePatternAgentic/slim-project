# SLIM Agent Communication

A working implementation of agent-to-agent communication using AGNTCY's SLIM (Secure Low-Latency Interactive Messaging) data plane server.

## Requirements

### 1. SLIM Data Plane Server
You need a SLIM server running on `localhost:46357`. You can either:

**Option A: Use Docker (Recommended)**
```bash
# Build SLIM server from source
git clone https://github.com/agntcy/slim.git
cd slim
docker build -t slim -f "./data-plane/Dockerfile" --platform linux/arm64 --target slim-release .

# Run SLIM server
docker run -it \
    -v ./data-plane/config/base/server-config.yaml:/config.yaml \
    -p 46357:46357 \
    slim /slim --config /config.yaml
```

**Option B: Build from Source**
```bash
# Clone and build SLIM
git clone https://github.com/agntcy/slim.git
cd slim/data-plane
cargo build --release

# Run SLIM server
./target/release/slim --config config/base/server-config.yaml
```

### 2. Python Dependencies
```bash
pip install slim-bindings
```

## Quick Start

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

## Complete Setup Instructions

### Step 1: Install Python Dependencies
```bash
pip install slim-bindings
```

### Step 2: Start SLIM Server
Choose one of the options above to get a SLIM server running on `localhost:46357`

### Step 3: Test Agent Communication
```bash
# Terminal 1: Start Agent B (receiver)
python authenticated_agents.py

# Terminal 2: Send message from Agent A
python authenticated_agents.py sender

# Or run integrated test
python authenticated_agents.py test
```

## Files

- **`authenticated_agents.py`** - Main agent implementation
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This file

## Troubleshooting

**"Connection refused" errors**: Make sure SLIM server is running on `localhost:46357`

**"No module named 'slim_bindings'"**: Run `pip install slim-bindings`

**Agent ID errors**: The agents use authentication to preserve human-readable IDs - this is normal and required

## Next Steps

To evolve this into intelligent agents:
1. Add LLM integration (OpenAI/Anthropic APIs)
2. Implement tool calling abilities
3. Create specialized agent roles
4. Add memory systems
5. Build task planning capabilities

## What This Provides

This is the foundational infrastructure for distributed AI agent systems - the "plumbing" is working, agents can communicate reliably through SLIM. You can build intelligent agents on top of this communication layer.
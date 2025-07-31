# SLIM Agent Communication

A working implementation of agent-to-agent communication using the SLIM (Secure Low-Latency Interactive Messaging) data plane server.

## Overview

This project demonstrates successful bidirectional communication between two separate agent processes through SLIM infrastructure. It solves the critical agent ID transformation issue found in SLIM's base/insecure mode and provides a clean, working solution for agent communication.

## Quick Start

### Prerequisites
- Python 3.7+
- SLIM data plane server running on localhost:46357

### Installation
```bash
cd slim_agents
pip install -r requirements.txt
```

### Usage
```bash
# Start Agent B (receiver)
python authenticated_agents.py

# In another terminal, start Agent A (sender)
python authenticated_agents.py sender

# Or run integrated test
python authenticated_agents.py test
```

## Repository Structure

```
├── README.md                    # This file - project overview
├── slim_agents/                 # Working agent implementation
│   ├── README.md               # Detailed setup and usage instructions
│   ├── authenticated_agents.py # Complete agent communication solution
│   └── requirements.txt        # Python dependencies
└── docs/                       # Complete technical documentation
    ├── documentation-index.md  # Documentation catalog
    ├── slim-agent-id-mismatch-fix.md  # Technical solution details
    ├── agent-communication-architecture-plan.md  # System architecture
    └── [additional documentation files]
```

## Key Features

- ✅ **Bidirectional Communication**: Agents can send and receive messages
- ✅ **Separate Processes**: Each agent runs as an independent process
- ✅ **Authentication Support**: Uses PyIdentityProvider.SharedSecret pattern
- ✅ **Human-Readable IDs**: Preserves agent identifiers for proper routing
- ✅ **Complete Documentation**: Comprehensive setup and technical docs

## Technical Achievement

This implementation solves the agent ID transformation issue in SLIM's base/insecure mode by using authenticated communication patterns. The solution enables proper message routing between agents while maintaining human-readable agent identifiers.

## Getting Started

1. **For immediate use**: See [`slim_agents/README.md`](slim_agents/README.md) for detailed setup instructions
2. **For technical details**: Browse the [`docs/`](docs/) folder for comprehensive documentation
3. **For understanding the solution**: Read [`docs/slim-agent-id-mismatch-fix.md`](docs/slim-agent-id-mismatch-fix.md)

## Documentation

Complete technical documentation is available in the [`docs/`](docs/) folder, including:
- System architecture and design decisions
- Technical problem analysis and solutions
- Step-by-step implementation guide
- Troubleshooting and debugging information

## License

This project demonstrates SLIM agent communication patterns and is intended for educational and development purposes.
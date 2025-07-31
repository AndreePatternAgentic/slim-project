# AI-Powered Agent Communication

A proof of concept demonstrating intelligent agent-to-agent communication using Google AI and SLIM infrastructure.

## 🎯 What This Does

- **Question Agent**: Generates intelligent questions using Google AI
- **Answer Agent**: Provides thoughtful AI-powered responses
- **SLIM Communication**: Secure message routing between agents
- **Container Ready**: Each agent runs as independent container

## 🚀 Quick Start

### Prerequisites
- SLIM server running on `localhost:46357` (see [main project docs](../docs/))
- Google AI API key
- Docker (for containerized deployment)

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google AI API key
GOOGLE_AI_API_KEY=your_actual_api_key_here
```

### 2. Local Development (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start Answer Agent (must start first)
python answer_agent.py

# Terminal 2: Start Question Agent
python question_agent.py
```

### 3. Container Deployment
```bash
# Build and run all services
cd docker
docker-compose up --build

# Or run individual agents
docker build -f docker/Dockerfile.answer -t answer-agent .
docker build -f docker/Dockerfile.question -t question-agent .

docker run -e GOOGLE_AI_API_KEY=your_key answer-agent
docker run -e GOOGLE_AI_API_KEY=your_key question-agent
```

## 🤖 Agent Behavior

### Question Agent
- Generates thought-provoking questions using Google AI
- Sends questions to Answer Agent via SLIM
- Configurable question interval and conversation length
- Topics: technology, science, philosophy, creativity, problem-solving

### Answer Agent
- Listens for incoming questions
- Uses Google AI to generate intelligent responses
- Maintains conversation context
- Provides thoughtful, detailed answers

## 📋 Configuration

### Environment Variables
```bash
# Google AI
GOOGLE_AI_API_KEY=your_api_key_here
GOOGLE_AI_MODEL=gemini-1.5-flash

# SLIM Server
SLIM_ENDPOINT=http://127.0.0.1:46357
SLIM_ORG=cisco
SLIM_NAMESPACE=default
SLIM_SECRET=shared_secret_123

# Agent Behavior
QUESTION_INTERVAL=15                    # seconds between questions
MAX_CONVERSATION_LENGTH=10              # questions before stopping
CONVERSATION_TOPICS=technology,science  # comma-separated topics
```

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐
│  Question Agent     │    │  Answer Agent       │
│  Container          │    │  Container          │
│                     │    │                     │
│ ┌─────────────────┐ │    │ ┌─────────────────┐ │
│ │Google AI        │ │    │ │Google AI        │ │
│ │Question Gen     │ │    │ │Answer Gen       │ │
│ │SLIM Client      │ │    │ │SLIM Client      │ │
│ └─────────────────┘ │    │ └─────────────────┘ │
└─────────────────────┘    └─────────────────────┘
           │                           │
           └─────────┐         ┌───────┘
                     ▼         ▼
              ┌─────────────────────┐
              │   SLIM Server       │
              │   localhost:46357   │
              └─────────────────────┘
```

## 🔧 Technical Details

### SLIM Communication
- **Authentication**: PyIdentityProvider.SharedSecret pattern
- **Agent IDs**: `cisco/default/question_agent`, `cisco/default/answer_agent`
- **Sessions**: FireAndForget configuration
- **Pattern**: Request-reply with background session handling

### AI Integration
- **Model**: Google Gemini 1.5 Flash (configurable)
- **Question Generation**: Context-aware, topic-based prompts
- **Answer Generation**: Conversational, detailed responses
- **Error Handling**: Graceful fallbacks for API failures

## 📦 Files

```
agentic_agents/
├── question_agent.py          # AI-powered question generator
├── answer_agent.py            # AI-powered answer provider
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── README.md                 # This file
└── docker/
    ├── Dockerfile.question   # Question agent container
    ├── Dockerfile.answer     # Answer agent container
    └── docker-compose.yml    # Multi-container deployment
```

## 🚀 Cloud Deployment

### Docker Compose (Production)
```bash
# Set environment variables
export GOOGLE_AI_API_KEY=your_key
export SLIM_ENDPOINT=http://slim-server:46357

# Deploy
docker-compose -f docker/docker-compose.yml up -d
```

### Kubernetes (Scalable)
```yaml
# Each agent as separate deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: question-agent
spec:
  replicas: 1
  
---
apiVersion: apps/v1  
kind: Deployment
metadata:
  name: answer-agent
spec:
  replicas: 3  # Scale based on load
```

## 🎉 Expected Output

```
=== AI-Powered Question Agent - Sender ===
✅ Google AI initialized with model: gemini-1.5-flash
✅ Agent created with ID: cisco/default/question_agent
✅ Agent connected to SLIM server
🧠 Generating question #1
✅ Generated question: 'What role should AI play in education?'
📤 Question Agent: Sending question #1: 'What role should AI play in education?'
📨 Question Agent: Received answer: 'AI Response: AI can revolutionize education by providing personalized learning experiences...'
🎉 Question-Answer exchange successful!
```

## 🔍 Troubleshooting

- **"GOOGLE_AI_API_KEY required"**: Set your API key in `.env`
- **"Connection refused"**: Ensure SLIM server is running on port 46357
- **"No matching found"**: Start Answer Agent before Question Agent

## 🎯 Next Steps

This proof of concept demonstrates the foundation for intelligent multi-agent systems. To extend:

1. **Add more agent types**: Data analysts, web scrapers, coordinators
2. **Implement tool calling**: Enable agents to use external APIs
3. **Add memory systems**: Persistent conversation history
4. **Create workflows**: Multi-step task execution
5. **Scale deployment**: Kubernetes orchestration
Agent-to-Agent Communication Architecture

## Status
**Draft** - Architecture plan for implementing agent communication via SLIM

## Current Infrastructure
- SLIM data plane server running on `localhost:46357`
- Base configuration (no TLS, no authentication)
- Python environment with `slim-bindings` available

## Architecture Overview

### Approach Selection
**Selected: Direct SLIM Bindings** (Approach A from available-examples-analysis.md)
- Reason: Most direct path to proof-of-concept
- Working example: `slim/data-plane/python-bindings/examples/src/slim_bindings_examples/request_reply.py`
- Default endpoint already matches our server: `http://127.0.0.1:46357`

### Agent Architecture
```
Agent A (Sender)                    SLIM Server                    Agent B (Receiver)
├── create_local_app()             ├── localhost:46357           ├── create_local_app()
├── set_route()                     ├── Base config               ├── receive() loop
├── request_reply()                 ├── No auth/TLS               ├── publish_to() response
└── FireAndForget session          └── Message routing           └── Background tasks
```

### Communication Pattern
**Request-Response Pattern** (from request_reply.py example)
1. Both agents use `create_local_app()` with authentication (shared_secret required)
2. Agent A creates session: `PySessionConfiguration.FireAndForget()`
3. Agent A sends request: `await local_app.request_reply(session, message.encode(), org, namespace, agent)`
4. Agent B receives via: `await local_app.receive()`
5. Agent B responds via: `await local_app.publish_to(session, response.encode())`

### Agent Implementation
**Agent Structure (from actual examples):**
```python
# Agent initialization (from common.py create_local_app)
local_app = await create_local_app(
    local="org/namespace/agent",
    slim={"endpoint": "http://127.0.0.1:46357", "tls": {"insecure": True}},
    shared_secret="some_secret"  # Required by examples
)

# Sender mode (from request_reply.py lines 50-84)
remote_org, remote_namespace, remote_agent = split_id(remote)
await local_app.set_route(remote_org, remote_namespace, remote_agent)
session = await local_app.create_session(slim_bindings.PySessionConfiguration.FireAndForget())
_, reply = await local_app.request_reply(session, message.encode(), remote_org, remote_namespace, remote_agent)

# Receiver mode (from request_reply.py lines 96-124)
async with local_app:
    while True:
        session_info, _ = await local_app.receive()
        asyncio.create_task(background_task(session_info.id))
        
async def background_task(session_id):
    while True:
        session, msg = await local_app.receive(session=session_id)
        response = f"{msg.decode()} from {instance}"
        await local_app.publish_to(session, response.encode())
```

### Agent Identification
**Format:** `organization/namespace/agent` (from common.py split_id())
- Example: `"testorg/default/agent1"`, `"testorg/default/agent2"`

### Authentication Requirements
**Shared Secret Required** (from common.py create_local_app lines 228-232)
- Examples require either JWT/bundle OR shared_secret
- For base mode: use shared_secret authentication
- Provider/verifier created via `shared_secret_identity(identity=local, secret=shared_secret)`

## Implementation Plan

### Phase 1: Basic Proof of Concept
1. Create two agents using request_reply.py pattern with create_local_app()
2. Use shared secret authentication (required by examples)
3. Agent A sends message to Agent B via request_reply()
4. Agent B responds using background task pattern
5. Verify end-to-end communication

### Phase 2: Enhanced Communication
1. Add message validation
2. Implement error handling
3. Add logging and monitoring

## Working Examples Available
- `slim/data-plane/python-bindings/examples/src/slim_bindings_examples/request_reply.py` - Complete sender/receiver implementation
- `slim/data-plane/python-bindings/examples/src/slim_bindings_examples/common.py` - create_local_app() and utilities
- Default configuration matches current server setup: `"http://127.0.0.1:46357"`

## Dependencies
- `slim-bindings` Python package
- Running SLIM server on `localhost:46357`
- Python 3.x environment
- Shared secret for authentication (required by examples)

## Compatibility Note
**Authentication Gap**: Examples require authentication but our server runs in base/insecure mode. Need to verify compatibility or adjust approach.

## Risk Mitigation
- Use proven examples as foundation
- Minimal custom code required
- Server already operational and tested
- Authentication pattern established in examples
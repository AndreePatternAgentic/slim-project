# Available Examples Analysis

## SLIM Python Bindings Examples

### Location: `slim/data-plane/python-bindings/examples/src/slim_bindings_examples/`

**request_reply.py**
- Creates SLIM participant with `slim_bindings.Slim.new(org, namespace, agent)`
- Connects to server: `await slim.connect({"endpoint": address, "tls": {"insecure": True}})`
- Sets routes: `await slim.set_route(remote_org, remote_namespace, remote_agent)`
- Creates FireAndForget session: `await slim.create_session(slim_bindings.PySessionConfiguration.FireAndForget())`
- Sends request and waits for reply: `await slim.request_reply(session, message, org, namespace, agent)`
- Receiver mode: waits for sessions with `await slim.receive()`, handles in background tasks

**fire_and_forget.py**
- Same setup as request_reply.py
- Uses `await slim.publish()` to send messages
- Uses `await slim.receive(session=session.id)` to get responses
- Shows sender/receiver pattern

**pubsub.py**
- Creates bidirectional streaming session: `PySessionConfiguration.Streaming(PySessionDirection.BIDIRECTIONAL)`
- Uses `await slim.subscribe()` for topic subscription
- Shows moderator pattern with `await slim.invite()` for adding participants
- Background tasks for continuous message receiving

**common.py**
- `split_id()` function for parsing "org/namespace/agent" format
- `shared_secret_identity()` for authentication setup
- `create_local_app()` helper for SLIM initialization
- Default endpoint: `"http://127.0.0.1:46357"`

## App-SDK Examples

### Location: `app-sdk/docs/USAGE_GUIDE.md`

**Weather Agent Example**
- Creates A2A server with agent card and request handler
- Uses `AgntcyFactory().create_transport("SLIM", endpoint="http://localhost:46357")`
- Creates bridge: `factory.create_bridge(server, transport=transport)`
- Starts with `await bridge.start(blocking=True)`

**Weather Client Example**
- Creates A2A client: `await factory.create_client(ProtocolTypes.A2A.value, agent_topic=topic, transport=transport)`
- Sends messages: `await client.send_message(request)`
- Uses A2A protocol over SLIM transport

### Location: `app-sdk/tests/e2e/test_a2a.py`

**Test Implementation**
- Shows parameterized testing across different transports including SLIM
- Creates factory and transport: `factory.create_transport(transport, endpoint=endpoint)`
- Creates client with both URL and topic: `agent_url=endpoint, agent_topic="Hello_World_Agent_1.0.0"`
- Sends test messages and validates responses

## Two Available Approaches

### Approach A: Direct SLIM Bindings
**What it is:** Direct use of `slim_bindings` Python library
**Examples:** `request_reply.py`, `fire_and_forget.py`, `pubsub.py`
**Key components:**
- `slim_bindings.Slim.new(org, namespace, agent)`
- `await slim.connect(config)`
- `await slim.request_reply()` / `await slim.publish()` / `await slim.receive()`
- Manual session and route management

### Approach B: App-SDK Factory Pattern
**What it is:** Higher-level abstraction using AgntcyFactory with A2A protocol
**Examples:** Weather agent/client in `USAGE_GUIDE.md`, `test_a2a.py`
**Key components:**
- `AgntcyFactory().create_transport("SLIM", endpoint)`
- `factory.create_client("A2A", agent_topic, transport)`
- `factory.create_bridge(server, transport)`
- A2A protocol abstraction over SLIM transport
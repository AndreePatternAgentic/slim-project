# SLIM Agent Communication Documentation Index

## Goal: Get Two Agents to Talk Using SLIM

This document lists all relevant documentation for understanding and implementing agent-to-agent communication using SLIM.

## Our Project Documentation (docs/)

### Setup & Build
- [`successful-build.md`](./successful-build.md) - Working Docker build command with platform fixes
- [`successful-run.md`](./successful-run.md) - Working Docker run command for SLIM server
- [`status-july29-5pm.md`](./status-july29-5pm.md) - Current project status and next steps

### Troubleshooting
- [`debug-analysis.md`](./debug-analysis.md) - Docker container debugging and distroless explanation

## SLIM Repository Documentation

### Core Documentation
- [`slim/README.md`](../slim/README.md) - Main SLIM overview, features, and prerequisites
- [`slim/data-plane/README.md`](../slim/data-plane/README.md) - Data plane build, run, and configuration guide

### Configuration Examples
- [`slim/data-plane/config/base/server-config.yaml`](../slim/data-plane/config/base/server-config.yaml) - Base server config (no auth/encryption)
- [`slim/data-plane/config/base/client-config.yaml`](../slim/data-plane/config/base/client-config.yaml) - Base client config for agents
- [`slim/data-plane/config/reference/config.yaml`](../slim/data-plane/config/reference/config.yaml) - Complete configuration reference

### Python Bindings & Examples
- [`slim/data-plane/python-bindings/README.md`](../slim/data-plane/python-bindings/README.md) - Python bindings with complete examples:
  - Request-Response pattern
  - Publish-Subscribe pattern
  - Fire-and-Forget pattern
  - Streaming pattern

## Agent Implementation

### Current Agents (agents/)
- [`agents/slim_mail_composer.py`](../agents/slim_mail_composer.py) - Mail composer agent with SLIM bindings (needs config fix)
- [`agents/slim_mail_validator`](../agents/slim_mail_validator) - Mail validator agent with SLIM bindings (needs config fix)

**Note**: Both agents have SLIM bindings implemented but require configuration updates to connect to `localhost:46357`.

## Key Configuration Points

### Server Connection
- **Endpoint**: `localhost:46357` or `http://localhost:46357`
- **Mode**: Base (no TLS, no authentication)
- **Agent ID Format**: `organization/namespace/agent` (e.g., `myorg/default/composer`)

### Communication Patterns Available
1. **Request-Response**: Synchronous communication
2. **Publish-Subscribe**: Topic-based messaging
3. **Fire-and-Forget**: One-way messaging
4. **Streaming**: Bidirectional streaming

## External Reference Examples

### Agentic Apps Repository
- **Location**: `agentic-apps/slim/data-plane/python-bindings/examples/`
- **Key Reference**: `request-reply.py` - Most relevant example for our use case
- **Note**: Use strictly as reference - focus only on SLIM binding patterns, ignore other repo content

## Next Steps
1. Update agent configurations to connect to running SLIM server
2. Test agent-to-agent communication
3. Verify message routing and delivery
# Successful SLIM Server Run

## Working Command

```bash
docker run -it \
    -e PASSWORD=${PASSWORD} \
    -v ./slim/data-plane/config/base/server-config.yaml:/config.yaml \
    -p 46357:46357 \
    slim /slim --config /config.yaml
```

**Reference**: [slim/data-plane/README.md](../slim/data-plane/README.md) lines 135-139

## Prerequisites

- Built container with `--target slim-release` (see [`successful-build.md`](./successful-build.md))
- Base mode configuration (no encryption/authentication)

## Key Points

1. **Port mapping**: `-p 46357:46357` exposes server port
2. **Config path**: Must match your directory structure (`./slim/data-plane/config/...`)
3. **Binary path**: `/slim` (correct stage) vs `/slim-mcp-proxy` (wrong stage)
4. **Environment**: `-e PASSWORD=${PASSWORD}` (not needed for base mode but required by command)

## Expected Behavior

Server starts and listens on port 46357. Use Ctrl+C to stop.
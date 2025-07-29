# Successful SLIM Container Build

## Working Command

```bash
docker build -t slim -f "./slim/data-plane/Dockerfile" --platform linux/arm64 "./slim"
```

**Reference**: [slim/data-plane/README.md](../slim/data-plane/README.md) lines 27-30

## Prerequisites

- Docker Desktop
- Taskfile (`brew install go-task`)
- Rust toolchain
- Go toolchain

**Reference**: [slim/README.md](../slim/README.md) lines 13-17

## Changes Made

1. **Simplified paths**: Used `"./slim"` instead of `"${REPO_ROOT}"` (git rev-parse)
2. **Single platform**: `--platform linux/arm64` for Apple Silicon (vs multiarch)
3. **Fixed Dockerfile path**: `"./slim/data-plane/Dockerfile"` (was `"${REPO_ROOT}/data-plane/Dockerfile"`)

## Platform Notes

- **Apple Silicon (M1/M2)**: Use `--platform linux/arm64` (as shown above)
- **Ubuntu Linux (x86_64)**: Use `--platform linux/amd64` instead
- **Cross-platform**: Use original README command with `--platform linux/amd64,linux/arm64`

## Build Results

- **Duration**: ~11 minutes (normal for Rust release builds)
- **Image**: `docker.io/library/slim:latest`
- **Components**: SLIM server + MCP proxy
- **Size**: Optimized distroless container

## Next Steps

Use [`container-run.md`](./container-run.md) to start the server.
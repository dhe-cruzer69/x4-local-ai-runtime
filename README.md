# x4-local-ai-runtime

[![CI](https://github.com/dhe-cruzer69/x4-local-ai-runtime/actions/workflows/ci.yml/badge.svg)](https://github.com/dhe-cruzer69/x4-local-ai-runtime/actions)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Local-first model runtime with hardware-aware recommendations.**

Detect hardware, recommend runtime/model size, optional cloud fallback (explicit, never silent).

## Quick start

```bash
pip install -e ".[dev]"
x4-ai detect
x4-ai recommend --ram 8 --gpu-vram 0
```

## Design

- Local-first by default
- Cloud fallback only when explicitly enabled
- No production inference claims until backends are wired and tested

<!-- X4-APEX-DIAGRAM-START:x4-local-ai-runtime -->

```mermaid
flowchart TD
    USER[User or Local Agent] --> DETECT[Detect Hardware Resources]
    DETECT --> REC[Recommend Runtime and Model Size]
    REC --> LOCAL{Local Backend Available?}
    LOCAL -->|yes| MODEL[Use Explicitly Configured Local Model]
    LOCAL -->|no| STOP[Report Missing Backend or Model]
    MODEL --> HEALTH[Validate Availability Before Use]
    HEALTH -->|ready| INFER[Run Local Inference]
    HEALTH -->|not ready| STOP
    CLOUD{Cloud Fallback Explicitly Enabled?} -->|no| STOP
    CLOUD -->|yes| CONFIRM[Show Provider and Cost Boundary]
    CONFIRM --> REMOTE[Configured Cloud Adapter - if implemented]
    NOTE[README states backend wiring and production inference are not yet established] -. status boundary .-> REMOTE
```

<!-- X4-APEX-DIAGRAM-END:x4-local-ai-runtime -->

## License

Apache-2.0

## APEX Architecture Map

> Status: architecture documentation; implementation and deployment claims require independent verification.

```mermaid
sequenceDiagram
  autonumber
  participant CLI
  participant Runtime
  participant Config as Model configuration
  participant Ollama
  participant Cache
  CLI->>Runtime: Start with explicit model and limits
  Runtime->>Config: Validate provider, context, and resource budget
  Config-->>Runtime: Valid configuration or typed error
  Runtime->>Ollama: Check health and model availability
  alt model missing and network pulls permitted
    Runtime->>Ollama: Pull pinned model
    Ollama-->>Runtime: Pull status
  else offline or pulls disabled
    Runtime->>Runtime: Use local model only or fail clearly
  end
  Runtime->>Runtime: Mark ready only after health check
  CLI->>Runtime: Submit bounded inference request
  Runtime->>Ollama: Infer with timeout and context limits
  Ollama-->>Runtime: Result or provider error
  Runtime->>Cache: Store only if cache policy permits
  Runtime-->>CLI: Response + model provenance
```

**Evidence note:** Model pulling, cache persistence, offline fallback, and readiness semantics must be verified against runtime code and tests.


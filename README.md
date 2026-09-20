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

## License

Apache-2.0

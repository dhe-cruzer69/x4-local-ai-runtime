"""Hardware detection and model recommendations."""
from __future__ import annotations

import os
import platform
from typing import Any


def detect_hardware() -> dict[str, Any]:
    ram_gb = None
    try:
        # Best-effort; may be unavailable in some sandboxes.
        page = os.sysconf("SC_PAGE_SIZE")
        pages = os.sysconf("SC_PHYS_PAGES")
        ram_gb = round((page * pages) / (1024**3), 1)
    except (AttributeError, ValueError, OSError):
        ram_gb = None

    return {
        "os": platform.system(),
        "arch": platform.machine(),
        "cpu": platform.processor() or platform.machine(),
        "ram_gb": ram_gb,
        "gpu_vram_gb": None,
        "cloud_fallback": "disabled",
    }


def recommend(hw: dict[str, Any]) -> dict[str, Any]:
    ram = float(hw.get("ram_gb") or 8)
    gpu = float(hw.get("gpu_vram_gb") or 0)

    if gpu >= 16:
        model = "13B–34B quantized"
        runtime = "llama.cpp / vLLM"
    elif gpu >= 6 or ram >= 16:
        model = "7B–13B quantized"
        runtime = "llama.cpp"
    elif ram >= 8:
        model = "3B–7B quantized"
        runtime = "llama.cpp"
    else:
        model = "1B–3B quantized"
        runtime = "llama.cpp"

    return {
        "hardware": hw,
        "recommended_runtime": runtime,
        "recommended_model": model,
        "cloud_fallback": hw.get("cloud_fallback", "disabled"),
        "notes": "Recommendations only — no inference claimed until backends are integrated and tested.",
    }

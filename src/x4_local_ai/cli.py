"""CLI for local AI runtime."""
from __future__ import annotations

import argparse
import json

from .hardware import detect_hardware, recommend


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="x4-ai")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("detect")
    p_rec = sub.add_parser("recommend")
    p_rec.add_argument("--ram", type=float, default=None, help="RAM GB override")
    p_rec.add_argument("--gpu-vram", type=float, default=None, help="GPU VRAM GB override")
    args = parser.parse_args(argv)

    if args.cmd == "detect":
        print(json.dumps(detect_hardware(), indent=2))
        return 0

    if args.cmd == "recommend":
        hw = detect_hardware()
        if args.ram is not None:
            hw["ram_gb"] = args.ram
        if args.gpu_vram is not None:
            hw["gpu_vram_gb"] = args.gpu_vram
        print(json.dumps(recommend(hw), indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

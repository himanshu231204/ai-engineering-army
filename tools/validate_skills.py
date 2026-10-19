"""Compatibility entry point for the AIEA validator."""

from aiea import main

if __name__ == "__main__":
    raise SystemExit(main(["validate"]))

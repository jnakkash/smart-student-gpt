#!/usr/bin/env python3
"""Check that required Polymarket env values exist without printing secrets."""

from __future__ import annotations

import os
from dotenv import load_dotenv

REQUIRED = [
    "POLYMARKET_HOST",
    "POLYGON_CHAIN_ID",
    "PRIVATE_KEY",
    "POLYMARKET_API_KEY",
    "POLYMARKET_SECRET",
    "POLYMARKET_PASSPHRASE",
]


def main() -> None:
    load_dotenv()
    missing = [key for key in REQUIRED if not os.getenv(key)]
    if missing:
        print("Missing required variables:")
        for key in missing:
            print(f"  - {key}")
        raise SystemExit(1)

    print("All required Polymarket environment variables are present.")
    print("Secrets were not printed.")


if __name__ == "__main__":
    main()

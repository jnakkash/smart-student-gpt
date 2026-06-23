#!/usr/bin/env python3
"""
Generate or derive Polymarket CLOB API credentials and write them to .env.

Run locally only:
  pip install -r requirements.txt
  python generate_polymarket_env.py

This prompts for your Polygon private key locally. Do not paste private keys into chat.
"""

from __future__ import annotations

import os
from getpass import getpass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError as exc:
    raise SystemExit("Missing python-dotenv. Run: pip install -r requirements.txt") from exc

try:
    from py_clob_client_v2 import ClobClient
except ImportError as exc:
    raise SystemExit("Missing py-clob-client-v2. Run: pip install -r requirements.txt") from exc


ENV_PATH = Path(".env")
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137


def normalize_private_key(private_key: str) -> str:
    private_key = private_key.strip()
    if not private_key:
        raise ValueError("PRIVATE_KEY is empty.")
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key
    if len(private_key) != 66:
        raise ValueError("PRIVATE_KEY should be 64 hex characters, or 66 characters including 0x.")
    return private_key


def load_existing_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_env(path: Path, values: dict[str, str]) -> None:
    ordered_keys = [
        "POLYMARKET_HOST",
        "POLYGON_CHAIN_ID",
        "PRIVATE_KEY",
        "POLYMARKET_API_KEY",
        "POLYMARKET_SECRET",
        "POLYMARKET_PASSPHRASE",
    ]

    lines = [
        "# Polymarket CLOB local environment file",
        "# Do NOT commit this file to GitHub.",
        "",
    ]

    for key in ordered_keys:
        if key in values:
            lines.append(f"{key}={values[key]}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def mask(value: str, keep: int = 6) -> str:
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}...{value[-keep:]}"


def main() -> None:
    load_dotenv()
    existing = load_existing_env(ENV_PATH)

    private_key = os.getenv("PRIVATE_KEY") or existing.get("PRIVATE_KEY")
    if not private_key:
        private_key = getpass("Paste your Polygon PRIVATE_KEY locally: ")

    private_key = normalize_private_key(private_key)

    client = ClobClient(
        host=HOST,
        chain_id=CHAIN_ID,
        key=private_key,
    )

    credentials = client.create_or_derive_api_key()

    api_key = credentials.get("apiKey") or credentials.get("key")
    secret = credentials.get("secret")
    passphrase = credentials.get("passphrase")

    if not all([api_key, secret, passphrase]):
        raise RuntimeError(f"Unexpected credentials response keys: {list(credentials.keys())}")

    new_values = {
        **existing,
        "POLYMARKET_HOST": HOST,
        "POLYGON_CHAIN_ID": str(CHAIN_ID),
        "PRIVATE_KEY": private_key,
        "POLYMARKET_API_KEY": api_key,
        "POLYMARKET_SECRET": secret,
        "POLYMARKET_PASSPHRASE": passphrase,
    }

    write_env(ENV_PATH, new_values)

    print("\nWrote Polymarket credentials to .env")
    print(f"POLYMARKET_API_KEY={mask(api_key)}")
    print(f"POLYMARKET_SECRET={mask(secret)}")
    print(f"POLYMARKET_PASSPHRASE={mask(passphrase)}")
    print("\nKeep .env private and make sure it is in .gitignore.")


if __name__ == "__main__":
    main()

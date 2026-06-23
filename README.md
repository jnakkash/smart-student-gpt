# polymarket

Local setup repo for generating Polymarket CLOB API credentials into a private `.env` file.

## Important security rule

Do not commit `.env`. Do not paste your wallet private key into chat, GitHub, Slack, or any website you do not fully trust.

This repo includes `.gitignore` so `.env` stays local.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Generate your Polymarket API key

Run:

```bash
python generate_polymarket_env.py
```

Paste your Polygon private key only into the local terminal prompt. The script will call Polymarket CLOB auth locally and write the generated credentials into `.env`.

The `.env` file will contain:

```env
POLYMARKET_HOST=https://clob.polymarket.com
POLYGON_CHAIN_ID=137
PRIVATE_KEY=...
POLYMARKET_API_KEY=...
POLYMARKET_SECRET=...
POLYMARKET_PASSPHRASE=...
```

## Verify env is present

```bash
python check_env.py
```

The checker confirms required values exist without printing secrets.

## Files

- `generate_polymarket_env.py` — local-only script that derives/creates Polymarket CLOB credentials.
- `check_env.py` — verifies required environment variables are present.
- `requirements.txt` — Python dependencies.
- `polymarket.env.example` — safe template only.
- `.gitignore` — prevents `.env` from being committed.

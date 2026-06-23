# Smart Student GPT

## Polymarket local environment setup

This repo should not contain real credentials. Keep your actual `.env` file local only.

1. Install dependencies locally:

```bash
pip install py-clob-client-v2 python-dotenv
```

2. Create a local `.env` file using the keys returned by your Polymarket CLOB credential script:

```bash
cp polymarket.env.example .env
```

3. Fill in these local-only values:

```bash
POLYMARKET_HOST=https://clob.polymarket.com
POLYGON_CHAIN_ID=137
POLYMARKET_API_KEY=your_generated_api_key
POLYMARKET_SECRET=your_generated_secret
POLYMARKET_PASSPHRASE=your_generated_passphrase
```

4. Load them in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("POLYMARKET_API_KEY")
secret = os.getenv("POLYMARKET_SECRET")
passphrase = os.getenv("POLYMARKET_PASSPHRASE")
```

`.gitignore` already excludes `.env`, so the real credential file should stay off GitHub.

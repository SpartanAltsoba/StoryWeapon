# Civic Intelligence Aggregator

**An AI-assisted research platform that pulls authoritative U.S. government and financial data sources into structured, auditable intelligence.**

Civic Intelligence Aggregator is a Flask application that queries public federal data sources and uses a large language model to parse, clean, and structure the results into schema-conformant JSON — with a modular blueprint architecture, real-time workflow status, and comprehensive logging and error handling.

## Data sources

| Module | Source | What it pulls |
|--------|--------|---------------|
| `fec` | Federal Election Commission | Campaign finance / contributions |
| `edgar` | SEC EDGAR | Corporate filings |
| `court_listener` | CourtListener | Federal & state court records |
| `civic_info` | Google Civic | Representatives & civic data |
| `lobby_view` | Lobbying disclosures | Federal lobbying activity |
| `search` + `gpt_handler` | IRS Form 990 (PDF/CSV) | Nonprofit financials, LLM-structured to JSON |

## Architecture

Flask + blueprints (`search`, `dashboard`, `gpt_handler`, `civic_info`, `fec`, `edgar`, `court_listener`, `lobby_view`). Documents are ingested, parsed (pdfplumber for 990 PDFs), and structured by an LLM against a defined schema. Logging and error handling are centralized in `common.py` / `logger.py`.

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# provide API keys as environment variables (see config.py):
#   OPENAI_API_KEY, FEC_API_KEY, GOOGLE_CIVIC_API_KEY, COURTLISTENER_TOKEN,
#   LOBBY_VIEW_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID, ...
python app.py
```

## License

Apache License 2.0 — © 2026 Sierra Special Investigations LLC. See [`LICENSE`](LICENSE).

---
*Formerly developed internally as "StoryWeapon / 17thSCOG." Open-sourced by Sierra Special Investigations as a public standard.*

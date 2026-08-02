# LLM Docs Mirrors

Unofficial machine-readable mirrors of official payment & fintech documentation, converted to plain Markdown for **LLM agents, RAG pipelines, and knowledge graphs**. Mirrored and maintained with [`llms-mirror`](https://github.com/naelrudd/llms-mirror).

Every repo ships the same artifact set:

| Artifact | Purpose |
|---|---|
| `llms.txt` | official link index (verbatim) |
| `llms-full.txt` | entire corpus in one file — drop it into your agent context |
| `INDEX.md` | every page + first heading, for discovery |
| `README.md` | landing page |
| `rag.py` | zero-dep RAG starter kit (ChromaDB + embeddings, no API key) |

## Mirrors

| Docs | Pages | llms-full | Repo |
|---|---|---|---|
| Clerk | 2343 | 26.6 MB | [clerk-docs-llm-agents](https://github.com/naelrudd/clerk-docs-llm-agents) |
| Stripe | 473 | 11.5 MB | [stripe-docs-llm-agents](https://github.com/naelrudd/stripe-docs-llm-agents) |
| Canva Developers | 392 | 2.1 MB | [canva-docs](https://github.com/naelrudd/canva-docs) |
| Midtrans | 589 | 4.1 MB | [midtrans-docs-llm-agents](https://github.com/naelrudd/midtrans-docs-llm-agents) |
| Xendit | 336 | 5.2 MB | [xendit-docs-llm-agents](https://github.com/naelrudd/xendit-docs-llm-agents) |
| **Total** | **4133** | **49.5 MB** | |

## Quick start

```bash
# Agent: point your context at a single file
https://raw.githubusercontent.com/naelrudd/stripe-docs-llm-agents/main/llms-full.txt

# RAG: semantic search, fully local
pip install chromadb
python rag.py build          # inside any mirror repo
python rag.py query "how do I create a payment intent?"
```

## Mirror your own

```bash
pip install llms-mirror
llms-mirror mirror https://docs.example.com/llms.txt --out example-docs
```

## What's inside

- **Stripe**: Payments, Checkout, Billing, Connect, Identity, financial products, full API reference (test keys redacted).
- **Clerk**: auth, user management, frontend/backend SDKs, webhooks, email/sms.
- **Canva**: Connect API, Design APIs, Extensions, App SDK, Print API.
- **Midtrans**: Snap, Core API, payment channels (Indonesia-focused), webhooks, fraud.
- **Xendit**: payment links, invoices, disbursement, virtual accounts, cards, QRIS (Southeast Asia).

## Why

Official docs are great for humans, noisy for models. These mirrors strip the chrome and give you one markdown file per page — the format LLMs already read best — plus a single-file corpus for context stuffing and a zero-config RAG kit for retrieval.

## License & attribution

Mirrored content © respective copyright holders. Unofficial, not affiliated with or endorsed by the vendors. Source URLs are preserved in each page path and `llms.txt`.

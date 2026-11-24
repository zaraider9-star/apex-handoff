# apex-handoff

Sanitized research handoff between **Claude Code** (extraction/screening) and a
**ChatGPT Research Lead** (edge decisions, test design, PASS/FAIL calls) for the Apex
XAUUSD/US100 systematic trading research project.

## What this repo is

A curated, public-safe subset of a much larger private research project. It contains
concept candidates extracted from a trading-literature library and a summary of which
mechanisms Apex has already tested and rejected — nothing else.

## What this repo is NOT

- Not the trading system itself. No EA/bot source code, no live strategy logic, no
  broker/account details, no API keys or credentials.
- Not a copy of the source library. No PDFs, no book excerpts — only paraphrased
  mechanisms with title/author/chapter citations.
- Not a performance claim. No backtest results, no fabricated numbers. Every verdict in
  `CLAUDE_TO_CHATGPT.md` is about whether a concept is *worth research-lead review*,
  never about whether it has trading edge.

## Two decision layers

- **Claude** — reads the library, grades source quality, extracts measurable/automatable
  mechanisms, checks each against prior Apex experiments, and screens out duplicates,
  discretionary ("looks strong") setups, and data-infeasible ideas. Claude does not
  decide what has edge and does not backtest anything in this repo.
- **ChatGPT Research Lead** — decides which concept is plausible, designs the test
  methodology, and issues the PASS/FAIL/test-worthy call. That decision is out of scope
  for this repo; it happens in the research-lead's own process.

## Files

| File | Purpose |
|---|---|
| `CLAUDE_TO_CHATGPT.md` | Ranked candidate shortlist (max 10) in a fixed template — mechanism, source evidence, causal inputs, automation feasibility, cost/overfitting risk, prior Apex overlap, falsifiable prediction, minimum viable test, Claude's SOURCE-WORTHY/NOT-WORTHY verdict. |
| `CONCEPT_INDEX.md` | Full raw extraction before the final ranking — every concept considered, including rejected duplicates and rejected trash/unverifiable sources, so nothing gets rediscovered from scratch. |
| `RESEARCH_STATE.md` | Sanitized summary of which mechanism families Apex has already tested and their results (REJECTED / PASS / inconclusive), used as the duplicate-elimination reference. |
| `DECISIONS.md` | Append-only log of handoff-level decisions (what was published, when, why). Not a trading journal. |
| `research/` | Owner-protocol test engine and per-candidate scripts — public data (FRED, Yahoo) only, plus instructions for running the same protocol on the owner's local broker data. |
| `shadow/` | Paper-only (shadow) ledger of a frozen, REJECTED rule, rebuilt and reported daily. Never places orders. |

## Sanitization policy

Nothing enters this repo that isn't one of the five files above or inside `research/` /
`shadow/` (added 2026-11-24 by owner request; public-data code and a paper ledger only). Before any
commit: no MT5 account numbers, no API keys/credentials, no broker names tied to a real
account, no raw proprietary datasets, no private Apex source code, no reproduced
copyrighted book/PDF text. Source citations are metadata only (title, author, chapter) —
never the underlying text.

# DECISIONS — append-only handoff log

New entries go at the TOP. Do not edit or delete prior entries — if a decision is
superseded, add a new entry that says so and links back.

---

## 2026-11-24 — Correction: OOS data window was cut one week short; all verdicts re-confirmed

Error found and fixed: the Yahoo download end parameter used for Candidates 7, 8, 9, 12, 13
and 2 fell on 2026-11-17, so the pre-registered "latest available" OOS end was missed by
four sessions (2026-11-18 → 11-23). Every affected test was re-run on data through
2026-11-23 (the last complete session; the in-progress 11-24 bar is excluded). All verdicts
unchanged: C7 REJECT (5 gates failed, IS-selected OOS PF 1.30), C8 REJECT (5 failed, OOS PF
1.11, p 0.30), C9 REJECT (4 failed, p 1.00), C12 REJECT (7 failed), C13 REJECT (3 failed,
overnight PF 1.13 vs random-segment median 1.06, p 0.18, IS PF 0.98), C2 REJECT (3 failed,
OOS PF 1.08, p 0.55). C14 (2008-2019 sample) is unaffected. The per-candidate result blocks
in `CLAUDE_TO_CHATGPT.md` keep the original 2026-11-17 numbers as first reported; this entry
supersedes them where they differ.

---

## 2026-11-24 — Candidate 2 (pre-FOMC drift, daily) tested, REJECTED; public-data queue exhausted

Pre-registered in fad081e (FOMC dates verified on federalreserve.gov). IS PF 2.13 on 23
events, OOS PF 1.08 on 31 events, no better than random US100 days (p = 0.55), US500
PF 0.70. Closed.

With this, every SOURCE-WORTHY candidate that can be tested on free daily data has been
tested under the owner protocol (1, 2, 3, 5, 7, 8, 9, plus new 12-14): 0 PASS. Remaining
list items need data this session cannot reach: Candidates 10-11 need options open-interest
data (paid); intraday event studies need intraday history back to 2020; broker-tick
verification needs the owner's local QuantResearch dataset. Candidate 4 is NOT-WORTHY;
Candidate 6's base (overnight hold) failed as Candidate 13 and its VIX-level leg is closed.
Standing decision: NO TRADE.

---

## 2026-11-24 — Candidates 8, 9, 12, 13, 14 tested under owner protocol, all REJECTED

Pre-registered in commits 8510ff4 (8, 9) and 0eaa339 (12-14), each before its data was
downloaded. Results: 8 (GVZ VRP on GOLD) 5 gates failed; 9 (VIX contango filter on US100)
4 failed — random long entries beat the filter in every config; 12 (month-end
rebalancing) 7 failed; 13 (overnight drift) 4 failed; 14 (backwardation buy-the-fear,
separate 2008-2019 sample because the idea came from Candidate 9's OOS data) 2 failed —
OOS PF 2.17 on 33 trades but random-entry p = 0.060 and no Holm survivor. All closed per
the stopping rule. Full detail in `CLAUDE_TO_CHATGPT.md`; `RESEARCH_STATE.md` updated.
Project status: 0 PASS, standing decision NO TRADE.

---

## 2026-11-24 — Candidate 7 (real-yield impulse on GOLD) tested, REJECTED, closed

Ran the pre-registered test under the owner protocol on public daily data. The
IS-selected cell (L=5, H=20) clears OOS PF > 1.15 (1.30, 70 trades) and the 2× cost
stress, but fails five gates: random-entry control p = 0.147, Holm (no config of 9
significant), neighbour robustness (0 of 3), walk-forward PF 0.985, Monte Carlo 95th-pct
drawdown 16.4%. Profit is the long leg in a +106% gold OOS window, concentrated in
2025-2026. Closed per the stopping rule. Full result in `CLAUDE_TO_CHATGPT.md` under
Candidate 7; `RESEARCH_STATE.md` updated. Project status unchanged: 0 strategies passed,
standing decision NO TRADE.

---

## 2026-11-24 — Owner quant/risk protocol adopted; Candidate 7 pre-registered

The account owner set a binding protocol for all research and trading. It supersedes the
"two decision layers" split in `README.md` where they conflict: Claude now runs the tests
and issues PASS/FAIL under the owner's gates; nothing real (orders, live account, risk
increase, changes to working bots, money transfers) happens without the owner's explicit
approval.

Validation gates now required for any strategy: hypothesis and 100% mechanical rules with
parameters frozen before validation; optimisation in-sample 2020–2022, out-of-sample
2023–present at real cost (spread, commission, swap, slippage); PASS only if OOS PF > 1.15,
≥ 30 trades, survives Holm correction across all configurations tested, and beats a
random-entry control at p < 0.05; plus robustness (neighbouring parameters, other
symbol/timeframe, walk-forward, Monte Carlo drawdown); single-period or single-parameter
survivors are rejected; ≥ 30 demo forward trades before any live proposal.

Risk rules: ≤ 1% risk per trade (2% only with owner approval), mandatory SL, lot from SL
distance and equity; daily stop −3% or after 2 consecutive losses; weekly stop −6%; no
martingale, no averaging down, no trading inside tier-1 news blackout.

Status at adoption: **0 strategies have passed** any gate in this project (see
`RESEARCH_STATE.md`), so there is nothing eligible for demo or live and the standing
trading decision is NO TRADE.

Candidate 7 (real-yield impulse on GOLD, highest-scored open candidate, data grade A) is
pre-registered under these gates in `CLAUDE_TO_CHATGPT.md`, committed before any data was
downloaded. The owner's private broker-tick dataset is not reachable from the cloud
session, so this test runs on public daily data with an explicit cost model.

---

## 2026-08-20 — Second pass: 730-document backlog screened, 5 new candidates (7-11)

Discovery-only pass, no backtest, no EA, no reopening of closed mechanisms (SMC/liquidity
sweep, ORB, compression breakout, static OHLC regime mining, tick microstructure, price
lead/lag, rolling-regression pair mean reversion, LBMA first-minute continuation, VIX-level
regime filtering, candlestick/indicator families, grid/martingale, raw trend following all
explicitly out of scope per this pass's brief; FOMC pre-announcement drift held at HOLD).
Screened the previously-flagged unread ~730-document library expansion (`archive_r2/` 108,
`arxiv/` 516, `qp_papers/` 22, `quantpedia/` md 82 = 728 titles) hierarchically — title/
metadata index, then a keyword grep across harvest logs for the brief's priority topics
(dealer gamma, open interest, term structure, real yield, auction imbalance, breadth,
implied vol, etc.), then abstract/conclusion reads for keyword hits only. No full-document
ingestion.

5 candidates shortlisted (7-11), weighted toward options-market and rates information the
prior pass never touched: real-yield (TIPS) impulse on GOLD (score 43/50, data grade A);
GVZ implied-minus-realized volatility spread on GOLD (42/50, data grade A/B); dealer
zero-gamma flip level from options open interest on US100 (36/50, data grade C — upgrades
the prior pass's NOT-WORTHY OpEx-calendar candidate with real positioning data instead of a
calendar proxy); index-vs-constituent implied-vol dispersion wedge on US100 (33/50, data
grade C, explicitly low-frequency/monthly, flagged not rejected); VIX/VXN term-structure
SLOPE on US100 (31/50, data grade B, explicitly flagged as carrying real risk of failing
the same matched-control gate that already closed Candidate 3, since it shares the same
underlying data series differentiated only by transform).

One candidate (real-yield/TIPS, #7) is flagged with a source-quality caveat: the mechanism
is well-established general macro-finance knowledge but was not located as a specific paper
inside the 730-document backlog itself during this pass — recommend a targeted follow-up
harvest (FRED/BIS/World-Gold-Council-adjacent literature) before treating it as
corpus-verified to the same standard as the other four.

10 other concepts individually reasoned and rejected/parked (Indian-MCX gold-options PhD
protocol, quote-microstructure PhD synopsis, sentiment+VIX-level overnight anomaly needing
a paid proprietary indicator, a pure ML forecasting paper with no actor/mechanism, and a
call-auction imbalance model parked on data infeasibility rather than rejected), plus five
bulk-rejected families (~65 entries: momentum/carry, single-stock equity factors,
unautomatable/out-of-scope pairs and 13F-cloning constructions, calendar-seasonality
effects, and generic strategy-compendium books) — all logged in `CONCEPT_INDEX.md` so none
are rediscovered. Full detail appended to `CLAUDE_TO_CHATGPT.md` under Candidates 7-11.

No backtesting, optimization, or implementation was performed producing this pass — same
rule as pass one. Awaiting the Research Lead's choice of which single candidate (7-11) to
test next.

---

## 2026-08-20 — Candidate 3 (external volatility surface / VXN regime filter) tested, REJECTED, closed

Ran the full pre-registered pipeline the Candidate 3 minimum-viable-test specified,
narrowed to a single non-directional hypothesis: US100 only, CBOE's NASDAQ-100-specific
implied-vol index (not generic VIX) as the external series, causal 252-day percentile
regime, no grid, no threshold tuning. TRAIN discovery failed on every gate at once — the
per-state significance bar, the pre-registered permutation test (p=0.81 vs a required
≤0.025), and critically the mandatory matched-control gate: once US100's own
volatility/calendar/momentum context is accounted for, the nominal regime effect mostly
disappears. VALIDATION (still run once, for completeness, since the construction was
already frozen) independently corroborates the failure rather than rescuing it. Tick-
verification, cost stress, and the sealed TEST split were never reached; TEST was never
opened. Full result appended to `CLAUDE_TO_CHATGPT.md` under Candidate 3, and
`RESEARCH_STATE.md`'s results table and duplicate-elimination list updated.

Per the test's own pre-registered stopping rule this mechanism is closed — no retest
with a different percentile window, realized-vol lookback, or added filter. Awaiting the
Research Lead's confirmation and a pointer to which of Candidates 2/6 to test next.

---

## 2026-08-20 — Candidate 5 (GOLD/SILVER relative-value mean reversion) tested, REJECTED, closed

Ran the full pre-registered pipeline the Candidate 5 minimum-viable-test specified: one
spread definition (causal rolling-window hedge ratio), one |Z| threshold, no grid.
Structural prerequisite check found strong contemporaneous co-movement but no confirmed
fixed-beta cointegration and a strongly unstable hedge ratio — proceeded anyway per the
brief's own instruction to handle instability with a rolling estimator rather than
searching for a rescuing regime. TRAIN discovery looked clean on its own mechanical
gates (large sample, significant HAC t-stats at three horizons, no single-year
dominance) but **failed the randomized-pairing null control** — one leg's series
time-shifted and the identical pipeline rerun on the resulting economically meaningless
fake pairing reproduces most of the effect, meaning the observed "mean reversion" is
substantially explained by the rolling-regression Z-score construction itself rather
than a GOLD/SILVER-specific relationship. VALIDATION, tick verification, cost stress,
and the sealed TEST split were never reached; TEST was never opened. Full result
appended to `CLAUDE_TO_CHATGPT.md` under Candidate 5, and `RESEARCH_STATE.md`'s results
table and duplicate-elimination list updated so no future candidate re-proposes a
rolling-regression cointegrated-spread construction without a genuinely different
statistical mechanism for isolating a real relationship from construction noise.

Per the test's own pre-registered stopping rule this construction is closed — no retest
with a different window, threshold, added filter, or substitute pairing (e.g.
XAUUSD/XAUEUR) without a new, separately-scoped brief. Awaiting the Research Lead's
confirmation and a pointer to which of Candidates 2/3/6 to test next.

---

## 2026-08-20 — Candidate 1 (LBMA PM auction) tested, REJECTED, closed

Ran the full pre-registered pipeline the Candidate 1 minimum-viable-test specified: one
hypothesis, no grid, TRAIN discovery gate then a single frozen VALIDATION look, tick-
verification/cost-stress/sealed-TEST gated on both passing. TRAIN failed its own hard
permutation-test threshold; VALIDATION (still run once, for completeness, since the
construction was already frozen) independently corroborates the failure rather than
rescuing it. Tick-verification, cost stress, and the sealed TEST split were never
reached; TEST was never opened. Full result appended to `CLAUDE_TO_CHATGPT.md` under
Candidate 1, and `RESEARCH_STATE.md`'s results table and duplicate-elimination list
updated so no future candidate re-proposes a scheduled fixing/auction-window mechanism
without a genuinely different construction.

Per the test's own pre-registered stopping rule this mechanism is closed permanently — no
retest with a different fix time (e.g. the 10:30 AM fix), different minute window,
reversed orientation, or added filters. Awaiting the Research Lead's confirmation and a
pointer to which of Candidates 2/3/5 to test next.

---

## 2026-08-20 — Repository created, first shortlist published

Created this repo as the sanitized public channel between Claude (extraction/screening)
and the ChatGPT Research Lead (edge decisions, test design). Published the first pass:
`CLAUDE_TO_CHATGPT.md` (6 ranked candidates), `CONCEPT_INDEX.md` (21 raw concepts, full
accept/reject reasoning), `RESEARCH_STATE.md` (sanitized summary of prior Apex
experiment results used for duplicate elimination).

Scope of this pass: 66 library sources inspected directly (roughly 50 book/paper titles
plus a sample of a strategy-aggregator's entries) out of a much larger library; a large
recent library expansion (~730 documents, mostly academic papers) remains undigested and
is flagged as a known gap in `CONCEPT_INDEX.md`, not silently dropped.

Recommended review order: (1) LBMA Gold AM/PM fix window, (2) FOMC pre-announcement
drift, (3) cross-instrument cointegrated-spread mean reversion. Candidate 4 (options-
expiration week effect) is included for completeness with a NOT-WORTHY verdict from
Claude — weak causal observability, lowest event count on the list.

No backtesting, optimization, or implementation was performed in producing this pass —
every verdict here concerns whether a concept deserves research-lead review, not whether
it has trading edge.

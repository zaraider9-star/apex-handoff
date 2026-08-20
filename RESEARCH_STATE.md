# RESEARCH_STATE — sanitized summary of completed Apex experiments

Purpose: prevent any candidate in `CLAUDE_TO_CHATGPT.md` / `CONCEPT_INDEX.md` from
re-testing a mechanism already closed here under a new name. This is a results-only
summary — methodology and verdicts, no strategy source code, no account/broker detail,
no raw datasets.

Two source tiers in the underlying private research:
- **`research/` track (EXP001-013 + a cash-open ORB variant)** — the newest and most
  rigorous track: broker-accurate execution, TRAIN/VALIDATION/TEST splits, HAC t-stats,
  block permutation, matched controls, Benjamini-Hochberg FDR correction.
- **Legacy track** — older, still-canonical rejections using walk-forward + Monte Carlo
  + purged k-fold rather than the newer permutation/matched-control battery. 17 separate
  verdict write-ups.

## Foundation (methodology, not a strategy)

Broker-accurate execution: real bid/ask tick data, timestamp correction (the broker
server clock is DST-aware EET/EEST, not fixed UTC+3 — a bug independently re-discovered
and fixed multiple times across sessions), next-tick entry (no same-bar fill), a
tick-level verification pass alongside faster bar-level screening. Bar-level screening
was measured to be optimistic: once real ticks are used, many nominal TP outcomes
reverse to SL.

## `research/` track — EXP001-013

| ID | Hypothesis | Result | Mechanism family |
|---|---|---|---|
| EXP001 | Liquidity sweep → rejection → displacement | REJECTED — 0/324 configs PF≥1.20, tick-verification reverses every validation-set survivor | liquidity sweep / SMC |
| EXP002 | Session compression → breakout → continuation | FAIL (sample-size gate; construction flaw in the compression-ratio feature) | compression breakout |
| EXP003 | Historical-percentile compression breakout | REJECTED / family closed (same root construction issue as EXP002) | compression breakout |
| EXP004 | Opening drive momentum (London/NY first 15-45min) | FAIL, cleanly directional — no combo shows monotonic forward-return | opening-range momentum |
| EXP005 | Market-state edge map (15 causal features) | PASS as discovery study, no clean edge — best candidate fails block-permutation | momentum/vol/range-position discovery |
| EXP006 | Drift-adjusted re-test of EXP005's runner-up pattern | No survivor — edge fully explained by broad unconditional drift, not bucket-specific structure | momentum/efficiency/range-position |
| EXP007 | Tick microstructure (quote imbalance, path efficiency, intensity) | No survivor — every state's adjusted effect sits below a quarter of median spread | tick/quote microstructure |
| EXP008 | Multi-market opportunity scan (10 instruments) | Instrument-selection study, not a strategy — selected a primary and secondary instrument | n/a |
| EXP009 | Data foundation & integrity audit | PASS — canonical dataset, TRAIN/VAL/TEST split frozen | n/a — data engineering |
| EXP010 | Cash-open directional transfer (gap, pre-open drift) | No survivor — clean directional null | pre-open/gap directional transfer |
| EXP011 | Overnight-range sweep / failed auction | No survivor — single train-set survivor reverses sign on validation | overnight-range liquidity sweep |
| EXP012 | Cross-market relative-strength lead/lag (regression/beta construction) | No survivor — correctly-timed cross-market signal adds nothing beyond the instrument's own momentum | cross-market lead/lag |
| EXP013 | Regime-stability & walk-forward audit across EXP010-012 | 0 stable, 0 regime-dependent, most drift-dependent or noise; the large majority of hypotheses were "calendar-dominant" (calendar month explains more variance than any causal regime axis) | methodology audit — **recommends moving to a genuinely different information source** |
| Cash-open ORB + retest (fully executable spec) | Opening-range breakout+retest | FAIL at the training stage — best cell's t-stat sits below the multiple-testing floor; brute edge negative even before cost | opening-range breakout+retest |
| Execution/journaling infrastructure | Semi-manual trade-execution and journaling tooling | Deployed/verified; not a strategy test, no autonomous entry logic | n/a |
| LBMA PM auction (Candidate 1 test) | Modern (2015+ electronic) 15:00 London gold-fix first-minute direction → 3min continuation | REJECTED — fails its own pre-registered permutation-test threshold on TRAIN; VALIDATION corroborates rather than rescues (below-coin-flip continuation rate, single-month-concentrated effect); tick-verification/cost-stress/sealed-TEST never reached | scheduled-auction / fixing-time |
| GOLD/SILVER relative-value mean reversion (Candidate 5 test) | Causal rolling-window hedge-ratio spread, extreme Z-score → mean reversion | REJECTED — fixed-beta cointegration unconfirmed and hedge ratio strongly unstable; TRAIN discovery looked clean on its own gates but failed a randomized-pairing null (fake pairing reproduces most of the effect, p≈0.07-0.11 vs required ≤0.025) — effect substantially a rolling-regression construction artifact, not GOLD/SILVER-specific; VALIDATION/tick-verification/cost-stress/sealed-TEST never reached | cross-instrument cointegration / stat-arb |

**EXP013's recommendation is the single most load-bearing constraint on new candidates**:
static OHLC/session/cross-market-price mining is not justified by this audit — any
candidate that is just another OHLC-derived feature is pre-rejected by this finding.

## Legacy track (chronological, condensed)

| Family | Result |
|---|---|
| 158-factor gradient-boosted classifier | REJECTED — out-of-sample profit factor below coin-flip baseline; the extra features added zero information |
| CRT-style H1 sweep + M5 displacement + FVG | REJECTED — direction-reading has real information (56% win rate vs 41% random) but payoff geometry loses |
| Adaptive liquidity-grid EA (grid/martingale-adjacent) | REJECTED before implementation — brute profit factor 0.84-1.04 at a t=2.68 noise floor; the one nominally-profitable cell was a look-ahead bug |
| Terrain-measurement pass (spread/cost recalibration) | Established the real current spread regime (much tighter than a stale legacy backfill had implied); win-rate assumptions recalculated downward accordingly |
| Opening-range breakout (published parameter set) | Brute-edge t-stat negative — not a cost problem, a signal problem |
| Slow trend-following (time-series momentum, published parameter set) | Sharpe well below the promotion gate |
| 2×2 strategy/indicator combination grid | Nothing passes at real cost; nothing passes deflated-Sharpe/overfitting-probability gates even at near-zero cost |
| H1-level reclaim/sweep/engulf system, two instruments | REJECTED on both instruments; also surfaced a Monte-Carlo framework bug (permutation without replacement under compounding is order-invariant) |
| Candlestick patterns, hand-picked shortlist | Zero survivors |
| Candlestick patterns, full standard-library catalog | One nominal survivor, not promoted — fails cross-symbol/context re-test |
| Candlestick patterns + context filter (session/HTF-trend) | Zero survivors of 80 pre-registered tests; pattern-stacking confluence performs at coin-flip |
| Higher-timeframe research (H1-W1, 25 configs, 17yr history) | Zero promoted; the one near-miss fails a multiple-testing correction and is concentrated in a single regime |
| Liquidity-sweep + market-structure-shift system | REJECTED — out-of-sample profit factor 0.63, deflated Sharpe ≈ 0 |
| Sweep + fair-value-gap system | REJECTED — profit factor 0.49 at real cost, 0.81 even at half cost; also surfaced real implementation bugs (inverted gap check, wrong-side stop not caught, spread modeled far too small) |
| Spread-model correction + re-run of a 27-strategy book-derived family | Confirms spread was previously under-modeled; re-run at corrected cost: still zero profitable at any cost including zero |
| Trailing-stop trend-following (real tick data) | REJECTED — a real brute edge exists (survives at near-zero cost) but requires very high trade frequency; cost eats several multiples of the brute edge; the entry signal itself is indistinguishable from random |

## Prior book/code harvesting (referenced, not re-run in this pass)

- 104 mechanically-extracted rules from 28 books; 22 were new-vs-Apex and all 22 were
  implemented and tested: **0 of 22 profitable even at zero simulated cost**. Any
  candidate reducing to one of these 22 needs a genuinely different mechanism-level
  angle to be reconsidered.
- 56 rules harvested from open-source trading code repositories, used as background
  context only, not independently re-tested in this pass.

## Net effect on duplicate elimination

Any new candidate that reduces to one of the following is automatically **HIGH overlap**
and excluded without further review: liquidity-sweep→reversal (any variant); opening-
drive→continuation (any variant); overnight-gap→cash-open-direction; cross-market lead/
lag via correlation or regression beta; static price-state + regime filtering on OHLC
alone; candlestick/chart patterns in any form; moving-average/RSI/MACD/Stochastic/CCI
crossovers or extremes in any form; grid/martingale in any disguise; trailing-stop
trend-following on raw price momentum; COT/positioning data as a standalone entry signal;
time-series momentum or currency-carry cross-sectional trend; scheduled fixing/auction-
window first-minute direction → short continuation (LBMA-style, any fix time or minute
window on this construction); cross-instrument cointegrated-spread mean reversion via a
rolling-regression Z-score (GOLD/SILVER or any similarly-behaved pair) unless a new
candidate can name a mechanism to isolate real cointegration from the rolling-regression
construction's own mechanical mean-reversion — the randomized-pairing null this test
introduced is the standing bar any future variant must clear.

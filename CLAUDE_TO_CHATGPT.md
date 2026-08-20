# CLAUDE → CHATGPT RESEARCH LEAD — candidate shortlist

6 candidates (not padded to 10 — see `CONCEPT_INDEX.md` for the 21 raw concepts
considered and why 15 were cut). Claude's verdicts below are ONLY about whether a
concept deserves research-lead review, never about whether it has trading edge. No
backtest was run to produce any of this file. No numeric performance figure below is
fabricated — where a number appears it is either a source-cited statistic (labeled) or a
data/mechanism fact, never a projected return.

---

## CANDIDATE 1

### Mechanism
Gold has two scheduled, official daily benchmark auctions (LBMA Gold Price AM 10:30 /
PM 15:00 London) at which large physical and derivative positions are settled at one
clearing price. Market makers who must fill client orders at the fix price pre-hedge in
the minutes before it, concentrating one-directional flow into a narrow, clock-time window
— a mechanism independent of any technical pattern in GOLD's own bars.

### Source evidence
Book/source: academic FX-microstructure literature on the WM/Reuters 4pm fix (public
arXiv preprint, FX market microstructure and the fixing window)
Author: academic (FX microstructure literature)
Chapter/page: full paper (short)
Quality grade: A

### Source claim
For FX majors, the probability of an extreme intraday price move is materially elevated
in the minute before the 4pm London WM/Reuters fix versus a random minute — driven by
market makers pre-hedging fixing-order flow, not by any published news event.

### Claude interpretation
Gold has its OWN separate official fix (LBMA AM/PM), a different institution and clearing
mechanism than the FX WM/R fix the source paper studied. Whether gold's fix produces an
analogous pre-fix volatility/directional-flow signature is Claude's extrapolation, not
something this source paper measured — it is a plausible-by-analogy hypothesis, not a
transferred finding.

### Causal information available before entry
Clock time only (10:30 / 15:00 London, known in advance every trading day) — no price or
indicator input required to know the window is coming.

### Automation feasibility
HIGH — pure calendar/clock trigger, no external data feed needed beyond the tick feed
already in use.

### Data required
GOLD M1/tick data (already cached internally) for the minutes bracketing each fix time,
across the full available history.

### Expected holding horizon
Minutes (comparable to the source paper's ~1-minute pre-fix window through a short
post-fix decay).

### Expected gross movement
Rough conceptual scale only, no number fabricated: whatever a "moderately elevated vs.
baseline" probability of an extreme short move implies — smaller in absolute terms than
a session-level event, larger than an average random minute. Not quantified here.

### Main transaction-cost risk
A single-minute clock-time edge must clear the spread twice (entry+exit) inside a very
short window; GOLD's measured spread could easily exceed any fix-window edge if the edge
is FX-paper-sized, not gold-sized.

### Main overfitting risk
Only 2 fix times/day exist — a multi-year history still yields a moderate sample of
distinct fix events, but any threshold tuned on the same window used to discover the
effect (e.g. exact minute offset, exact "extreme move" definition) risks curve-fitting a
single narrow clock window with few independent degrees of freedom.

### Prior Apex overlap
NONE. No prior experiment tests a scheduled-auction/fixing-time mechanism. It is
explicitly the "auction-specific observable data" category that remains underexplored
per the prior regime-audit's own recommendation.

### Why it is NOT already disproven
A prior tick-microstructure experiment (EXP007) tested quote-pressure imbalance, path
efficiency, and intensity features on a regular 1-minute grid across the whole session —
it never conditioned on the specific LBMA fix clock times, and its features are generic
microstructure, not fix-specific. This is a different information source (a scheduled
external auction event), not a re-slice of that experiment's feature set.

### Falsifiable prediction
GOLD's realized volatility and/or directional persistence in the 5 minutes before 10:30
and 15:00 London is NOT statistically distinguishable from time-matched control minutes on
non-fix days (or other minutes) once the same HAC/permutation controls used previously are
applied.

### Minimum viable test
Single-hypothesis pre-registered test (not a grid): realized-vol ratio and mean signed
return in the fix-adjacent window vs. a matched-time-of-day control, HAC t-stat + block
permutation, reusing the existing frozen TRAIN/VALIDATION split. No SL/TP/EA yet —
discovery-study only, same shape as the prior market-state discovery studies.

### Verdict from Claude
SOURCE-WORTHY

### RESULT (tested 2026-08-20) — REJECT

Full pre-registered pipeline run exactly as scoped in the minimum-viable-test above,
modern (2015+ electronic auction) GOLD data, no grid, no threshold tuning, no retries.

**TRAIN** (n=222 eligible auction days): mean oriented continuation effect small and
positive, but the pre-registered gate failed on its one hard threshold — a 1000-rep
block permutation of auction-vs-placebo (14:00/16:00 London) identity puts the real
15:00 window's effect at roughly the 96th percentile of the null, short of the required
97.5th (p≈0.035 vs a ≤0.025 requirement). HAC t-stat and effect-vs-spread both landed
well under their preferred bars too (t≈0.9 vs a preferred ≥2; effect at roughly half a
contemporaneous spread vs a preferred >1x).

**VALIDATION** (n=74, frozen construction, run once regardless of the TRAIN result, for
completeness): sign nominally repeats but continuation rate actually falls to below
coin-flip and below TRAIN's own rate; the median event is negative; one of the two
placebo comparisons flips sign versus TRAIN; and the large majority of the whole
VALIDATION-period effect is concentrated in a single calendar month — the specific
"single-month-dominated" failure mode this test explicitly pre-registered as
non-waivable.

**Tick verification / cost stress / sealed TEST**: not reached — all three are
conditional on TRAIN+VALIDATION passing, per the pre-registered stage gates. TEST was
never opened.

**Exact reason for stopping**: TRAIN failed its own pre-registered discovery gate (hard
permutation threshold missed, both preferred numeric bars missed), and the one-time
VALIDATION check independently corroborates rather than rescues that failure (sign
technically repeats but every other diagnostic — win rate, median, one placebo
comparison, month-concentration — points the same way). Per this test's own pre-
registered stopping rule, the mechanism is closed: no retesting with a different fix
time, different minute window, reversed orientation, or added filters.

**Next action requested from ChatGPT Research Lead**: confirm closure of Candidate 1 (no
further variants), and indicate which of Candidates 2/3/5 (the next source-worthy,
non-overlapping candidates on this list) should be tested next.

---

## CANDIDATE 2

### Mechanism
FOMC meetings are pre-scheduled ~8 times/year; the equity risk premium compresses in the
hours before the announcement as uncertainty about the policy outcome resolves, producing
a documented pre-announcement drift that is present regardless of the announcement's
actual content. Gold (a rate-sensitive asset) and US100 (an equity index) both plausibly
carry an analogous pre-resolution drift, driven by the SAME macro calendar, not by either
instrument's own recent price action.

### Source evidence
Book/source: Quantpedia entry on the FOMC meeting effect in stocks, citing published
academic work on pre-FOMC announcement drift
Author: academic (cited papers), aggregated by Quantpedia
Chapter/page: full strategy entry
Quality grade: A

### Source claim
S&P 500 FOMC-meeting-day returns account for a disproportionate share of cumulative
market returns while being a small fraction of trading days; pre-FOMC returns in the 24h
before the announcement account for the large majority of the total equity premium
measured over a multi-year sample (source-cited statistics).

### Claude interpretation
The source studies US equities exclusively. Applying the same calendar-conditioning logic
to GOLD (rates-sensitive, historically reacts to Fed policy surprises) and to US100
(literally an equity index, closer fit to the source's own asset class than gold) is
Claude's extension — the magnitude, sign, and even existence of an analogous effect on
these two specific instruments at Apex's cost structure is unmeasured.

### Causal information available before entry
The FOMC meeting calendar is published months in advance by the Federal Reserve — pure
scheduling information, zero price/indicator dependency.

### Automation feasibility
HIGH — a fixed, low-maintenance calendar (8 dates/year) can be hardcoded/updated
manually, the same pattern already used internally for an existing macro-blackout
calendar.

### Data required
FOMC meeting/decision timestamps (public record, easy to source once and freeze); GOLD
and US100 bars already cached internally.

### Expected holding horizon
Hours (pre-announcement window through announcement, per the source's construction — could
also be tested holding only the pre-announcement leg to avoid the announcement's own
volatility spike).

### Expected gross movement
Not quantified here (no fabricated number) — conceptually, the source's own claim that a
disproportionate share of ALL equity returns cluster in this window suggests the
per-event magnitude is large relative to an average session, if it transfers at all.

### Main transaction-cost risk
Only 8 events/year — this is a LOW-FREQUENCY signal, well under the trade-count floor
normally required for cross-sectional validation internally, so per-event cost is a minor
concern but statistical power is the dominant constraint (see overfitting risk below).

### Main overfitting risk
8 events/year over even 5 years of history is only ~40 independent observations — a single
pre-registered hypothesis test is feasible, but ANY grid search over entry-window width,
holding period, or SL/TP would immediately overrun the sample's noise floor, and only
~40 events total are available at all.

### Prior Apex overlap
PARTIAL. A prior opening-drive experiment (EXP004) tested price-derived session-open
momentum, not a macro-calendar condition — different information source. The prior
regime-audit explicitly recommends "scheduled macro/economic-calendar events" as the next
information source to test, having found static OHLC/session mining exhausted. This
candidate is literally that suggested next step, materialized.

### Why it is NOT already disproven
No prior experiment conditions entry on the FOMC calendar specifically (a CPI-based
blackout filter is the only macro-calendar mechanism tested previously, and only as a
skip-day filter, not as a directional pre-announcement drift signal to trade).

### Falsifiable prediction
GOLD and/or US100 mean return in the pre-registered pre-FOMC window is NOT statistically
distinguishable from zero (or from a matched-time-of-day, non-FOMC-day control) once
block-permutation and matched-context controls analogous to prior experiments are applied.

### Minimum viable test
Single pre-registered hypothesis (pre-FOMC window return, GOLD and US100 separately, one
holding-period choice, no grid) using the existing frozen TRAIN/VALIDATION split
methodology. ~40 events over the available history — must be evaluated honestly as a
small-sample test from the start, not iterated into significance.

### Verdict from Claude
SOURCE-WORTHY

---

## CANDIDATE 3

### Mechanism
Realized/implied volatility that is NOT derived from GOLD or US100's own price history —
e.g. the VIX index level and its term structure (contango/backwardation) — reflects
aggregate market-wide risk appetite and can plausibly condition how GOLD/US100 respond to
their own local price moves (e.g. breakouts persisting more/less depending on whether
broad market volatility regime is calm or stressed), without being mathematically
reducible to any ATR/range/volatility feature computed from GOLD/US100's own bars.

### Source evidence
Book/source: Quantpedia entries on the volatility risk premium and on exploiting VIX
futures term structure, citing published academic work
Author: academic (cited papers), aggregated by Quantpedia
Chapter/page: full strategy entries
Quality grade: A (volatility risk premium) / B (VIX term structure — source itself flags
out-of-sample alpha decay)

### Source claim
The volatility risk premium is real and persistent per the cited in-sample study; the
VIX futures term structure (contango vs backwardation) has genuine forecast power for
subsequent VIX futures returns, though the source's own out-of-sample test shows decay.

### Claude interpretation
Neither source proposes using VIX as a REGIME FILTER for an unrelated instrument
(GOLD/US100) — both trade VIX derivatives directly. Claude's extension: use the VIX level/
term-structure state purely as an EXTERNAL CONDITIONING VARIABLE on GOLD/US100 entries
already otherwise defined (e.g. does a GOLD momentum signal work better/worse when VIX is
elevated vs. calm) — this reframes an options-trading strategy into a regime-filter for a
completely different, already-existing entry mechanism.

### Causal information available before entry
VIX index level, moving average, and term-structure slope at the time of the candidate
GOLD/US100 signal — all public, available before entry, causally prior (the conditioning
value used would be the last completed period's close).

### Automation feasibility
MEDIUM — VIX itself is not in the broker's default symbol list; requires an external data
feed (e.g. a free daily/intraday VIX API) merged by timestamp with the GOLD/US100 series
— an extra integration step, not a blocker.

### Data required
VIX (and optionally VIX futures term-structure) history matched to GOLD/US100's
timestamps; GOLD/US100 data already cached internally.

### Expected holding horizon
Same as whatever base signal is being conditioned (this is a filter, not a standalone
entry) — likely minutes to hours if layered onto an existing intraday construction.

### Expected gross movement
Not applicable as a standalone number — this is a regime CONDITION on an existing signal's
expected movement, not an independent movement claim.

### Main transaction-cost risk
None specific to this concept beyond whatever base strategy it filters — the VIX condition
itself only reduces trade frequency (acts as a gate), it doesn't add execution cost.

### Main overfitting risk
Choosing the VIX threshold/lookback (e.g. "VIX below its 20-day MA") after seeing which
threshold makes an existing signal look best is an easy, invisible form of double-dipping —
must be pre-registered independent of any GOLD/US100 result, or tested only as a genuinely
NEW discovery-study hypothesis (does VIX regime alone predict GOLD/US100 forward returns,
unconditional on any other signal) before ever being combined with one.

### Prior Apex overlap
NONE. All prior volatility features (EXP005/EXP006/EXP013) were built FROM GOLD or
US100's own bars (ATR, realized vol quintiles, intraday vol). No prior experiment ever
pulls in an external, non-price-derived volatility surface.

### Why it is NOT already disproven
The prior regime-audit's own recommendation explicitly names "an external volatility
surface not derivable from US100's own price" as one of the few genuinely new directions
left after finding static OHLC/session/cross-market mining exhausted. This candidate is
a direct, literal answer to that recommendation.

### Falsifiable prediction
GOLD/US100 forward returns conditioned on VIX regime (e.g. above/below its own trailing
MA) show no statistically distinguishable difference from the unconditional distribution,
once HAC/permutation controls are applied — i.e. VIX regime carries zero information about
GOLD/US100's own next-period behavior beyond what GOLD/US100's own recent volatility
already implies (this last clause is the critical control: a prior experiment already
showed that a "looks predictive" feature can be entirely explained by the instrument's own
drift/vol).

### Minimum viable test
Discovery-study only (same shape as the prior market-state discovery study): bucket
GOLD/US100 forward returns by VIX-regime tercile (unconditional on any entry rule), test
whether the bucket means differ from a matched-context control that already conditions on
GOLD/US100's OWN volatility quintile (to isolate whether VIX adds anything beyond what
local vol already captures — this is exactly the matched-control gate that killed a prior
experiment's nominal best candidate).

### Verdict from Claude
SOURCE-WORTHY

---

## CANDIDATE 4

### Mechanism
US100 (Apex's primary instrument) is a CFD tracking the NASDAQ-100 index, whose
constituent stocks have monthly-expiring listed options. Around the monthly (3rd-Friday)
expiration, option dealers unwind large delta/gamma hedging positions, which the academic
literature documents as producing abnormal weekly return patterns in the underlying index
driven by dealer positioning mechanics — a mechanism distinct from any price pattern in
US100's own bars.

### Source evidence
Book/source: Quantpedia entries on the option-expiration week effect and on dispersion
trading, citing published academic work
Author: academic (cited papers), aggregated by Quantpedia
Chapter/page: full strategy entries
Quality grade: A

### Source claim
Large-cap US equities' weekly returns over the option-expiration (3rd-Friday) week are
abnormally high relative to other weeks and to stocks with less option activity, linked to
delta-hedge rebalancing by option market makers as near-term options expire.

### Claude interpretation
The source studies individual large-cap US equities with active options, not index CFDs.
Whether the SAME dealer-hedging-unwind mechanism produces a measurable footprint in US100
(a CFD tracking an INDEX, where dealer flow is aggregated across the whole underlying
basket, not a single name) is Claude's extrapolation — plausible by the same economic
logic (NASDAQ-100 index options are among the most actively traded in the world) but
unmeasured for this specific instrument.

### Causal information available before entry
The monthly options-expiration calendar (3rd Friday of each month) is known far in
advance — pure calendar information, no price/indicator dependency for the DATE trigger.
(Note: the true causal driver — actual dealer gamma exposure — is NOT observable without
options open-interest data; only the calendar date is a usable proxy, see automation
note.)

### Automation feasibility
MEDIUM — the calendar trigger itself is trivial (hardcode the 3rd Friday of each month),
but the mechanism's actual strength depends on dealer gamma positioning that isn't
observable, so the signal being tested is a coarse calendar PROXY for the true causal
variable, not the variable itself.

### Data required
Monthly options-expiration calendar (trivial to construct/freeze); US100 bars already
cached internally.

### Expected holding horizon
Days (the "week" construction in the source paper) — could also be tested at a tighter
1-2 day window around the expiration date itself for an intraday-scalping-compatible
adaptation.

### Expected gross movement
Not quantified here — the source's own claim is a relative outperformance across a full
week, not a single-session magnitude; no number is transferable to intraday scale without
a fresh measurement.

### Main transaction-cost risk
Only 12 events/year (like FOMC) — LOW frequency relative to Apex's typical validation
floor; if adapted to a tighter multi-day window rather than weekly hold, transaction cost
of 12 trades/year is trivially small relative to any real effect, but so is statistical
power (see overfitting risk).

### Main overfitting risk
12 events/year is an even smaller sample than FOMC's 8/year — any parameter search
(window width, entry/exit timing within the week) will overrun the noise floor almost
immediately; this is the WEAKEST-powered candidate on this list purely on sample-size
grounds, independent of mechanism plausibility.

### Prior Apex overlap
PARTIAL. The prior regime-audit (EXP013) found that calendar month explains more
variance than any causal regime axis, treated as essentially a warning sign /
methodological artifact, NOT as a causally-motivated finding to build on. This candidate
proposes a specific, externally-motivated CAUSAL explanation (dealer gamma) for part of
that calendar-dominance, rather than treating monthly seasonality as a raw feature to
mine — a materially different framing, but touching the same raw observation.

### Why it is NOT already disproven
No prior experiment conditions on the options-expiration calendar specifically, nor
proposes a dealer-hedging-flow mechanism for any calendar effect found.

### Falsifiable prediction
US100's realized volatility and/or mean return in the 1-2 trading days around monthly
options expiration is NOT statistically distinguishable from a matched non-expiration-week
control, once controlled for the SAME calendar-month effect already flagged as dominant
(i.e. the effect must survive controlling for "it's just this month" to be attributable to
the expiration mechanism specifically, not to generic month-of-year seasonality).

### Minimum viable test
Single pre-registered hypothesis, discovery-study shape, with the explicit control
described above (expiration-week effect net of the existing calendar-month baseline) —
given only ~12 events/year, this should be evaluated as directionally informative at
best, not expected to individually clear a multiple-testing floor without pooling several
years.

### Verdict from Claude
NOT-WORTHY (documented for completeness; the combination of low event count, an
unobservable true causal driver, and partial overlap with an already-flagged and
methodologically suspect calendar-dominance finding makes this the weakest candidate on
the list — recommend deprioritizing unless Candidates 1-3/5/6 are exhausted)

---

## CANDIDATE 5

### Mechanism
Two economically linked instruments (e.g. GOLD priced in USD vs. GOLD priced in EUR, or
GOLD vs. SILVER) can temporarily diverge from their historical price ratio due to
instrument-specific noise (differential liquidity, momentary order-flow imbalance in one
leg only) while remaining fundamentally tied together (both are claims on the same
physical commodity, or currency-adjusted versions of the same asset) — creating a
mean-reverting SPREAD independent of either instrument's own directional trend.

### Source evidence
Book/source: Quantpedia entry on trading a commodity-pair spread (WTI-Brent), citing
published academic work and a Bollinger-Band spread-trading approach
Author: academic (cited papers), aggregated by Quantpedia
Chapter/page: full strategy entry
Quality grade: B (source itself flags "OOS back-test shows slightly negative performance
... alpha deteriorating")

### Source claim
A moving average of the spread between two cointegrated commodity benchmarks is a
workable mean-reversion signal: short the spread above its MA, long below, exit at MA
cross — profitable in- and out-of-sample in the cited paper, though the aggregator's own
confidence label flags OOS decay across the broader literature it aggregates.

### Claude interpretation
The source studies two crude-oil benchmark futures. The underlying MECHANISM (two
economically-linked instruments, cointegrated by fundamentals, temporarily diverging in
price ratio due to instrument-specific liquidity noise) is Claude's generalization to a
GOLD-family pair Apex's broker already offers — either GOLD/SILVER (both already in
Apex's symbol set and cached internally) or XAUUSD/XAUEUR (both already cached
internally). The WTI-Brent paper's specific parameters (moving-average window,
crude-oil-specific cost/liquidity) do not transfer; only the construction template does.

### Causal information available before entry
The real-time price ratio/spread between the two legs, computable from data already
present before any entry — no external data feed required.

### Automation feasibility
HIGH — both legs are already tradable at the same broker/terminal Apex already uses; no
new data source needed beyond what's already fetched for the primary/secondary
instruments.

### Data required
GOLD and SILVER bars, or XAUUSD and XAUEUR bars — either pairing is already cached
internally, no new fetch needed.

### Expected holding horizon
Not specified by the source at intraday scale (it used daily data) — would need fresh
determination; conceptually short (hours) if adapted to a shorter timeframe given the
mean-reversion framing implies fast convergence once the spread normalizes.

### Expected gross movement
Not quantified here — no number from the crude-oil source paper is transferable to a
gold-pair spread without independent measurement.

### Main transaction-cost risk
TWO legs means TWO spreads paid per round trip (open+close on both instruments) — the
cost hurdle is roughly double a single-instrument strategy's, a real structural risk given
Apex's own repeated finding that spread dominates edge on GOLD at intraday timeframes.

### Main overfitting risk
The specific spread-normalization window (the source's moving-average length) is a free
parameter that must be chosen once and frozen, not grid-searched — prior experiments have
repeatedly shown how easily a single-window-choice parameter degenerates into an
undeclared extra trial if tuned after seeing results.

### Prior Apex overlap
NONE on the specific construction. A prior cross-market experiment (EXP012) tested lead/
lag via a causal expanding-OLS regression beta (a DIFFERENT statistical construction —
predicting one series' RETURN from another's, not testing whether a RATIO/SPREAD between
two cointegrated instruments mean-reverts). GOLD/SILVER or XAUUSD/XAUEUR was never tested
as a cointegrated pair in any prior experiment.

### Why it is NOT already disproven
No prior session tests a spread/ratio mean-reversion construction between two
instruments — every cross-instrument test to date used a directional lead-lag/regression
framework, not a stat-arb/cointegration framework. Genuinely different statistical
mechanism, not just a different instrument pair.

### Falsifiable prediction
The GOLD/SILVER (or XAUUSD/XAUEUR) price ratio does NOT exhibit statistically significant
mean-reversion beyond what a matched-random-walk-pair control would produce, once tested
with a pre-registered normalization window and HAC/permutation controls analogous to
prior experiments' battery.

### Minimum viable test
Single pre-registered hypothesis (one spread definition, one normalization window, no
grid): does the spread's deviation from its own trailing mean predict the spread's own
forward change, TRAIN/VALIDATION split, matched-random-pair control as the null.

### Verdict from Claude
SOURCE-WORTHY

---

## CANDIDATE 6

### Mechanism
An overnight (or session-carrying) hold's expected return may depend on the broad
market's risk-appetite regime (external, not price-derived) rather than on GOLD/US100's
own overnight gap or pre-open drift (both already tested and rejected). If broad market
sentiment/volatility is calm, an overnight hold in a rate-sensitive or equity-index-
tracking instrument may behave differently than during a stressed regime — a distinct
conditioning variable from anything tested previously.

### Source evidence
Book/source: Quantpedia entry on market sentiment and an overnight anomaly, citing
published academic work
Author: academic (cited paper), aggregated by Quantpedia
Chapter/page: full strategy entry
Quality grade: A

### Source claim
Holding a major equity index overnight only when price is above its 20-day MA, a broad
volatility index is below its MA, and a proprietary sentiment indicator is above its MA
produces (per the source paper, source-reported) a strong risk-adjusted return in the
cited sample — explicitly presented by the source as an overlay/filter, not a standalone
system, and explicitly flagged as having "very high" transaction costs if traded on its
own.

### Claude interpretation
The source studies a specific US equity index proxy, with a proprietary sentiment
indicator Apex has no access to. Claude's extension: the CONSTRUCTION (condition an
overnight/session-carry hold on EXTERNAL, non-price-derived regime variables rather than
on the instrument's own recent price) is transferable to GOLD/US100 using publicly
available substitutes (a volatility index alone, or a gold-specific volatility proxy if
accessible) — but this drops the proprietary sentiment leg entirely, which the source's
own construction relies on for one-third of its filter, so the transferred version is a
materially weaker instrument than what was actually tested.

### Causal information available before entry
Volatility-index level/MA and (if a substitute is found) an external sentiment proxy,
both available before the overnight hold decision — same class of external data as
Candidate 3.

### Automation feasibility
MEDIUM — same external-data-integration requirement as Candidate 3, plus the added
complication that a genuine substitute for the proprietary sentiment leg may not exist
for free, meaning this candidate may only ever be testable as a partial-filter version of
the source's actual construction.

### Data required
Volatility-index history matched to GOLD/US100 timestamps (as Candidate 3); GOLD/US100's
own price relative to its trailing MA (already computable from cached data).

### Expected holding horizon
Overnight / one session (matches the source's construction directly).

### Expected gross movement
Not quantified here — no number from the source paper is transferable without
independent measurement on GOLD/US100.

### Main transaction-cost risk
The source paper ITSELF explicitly warns transaction costs would be "very high" for this
kind of overnight-timing strategy traded standalone — a direct, source-stated caution,
not just an Apex-side concern.

### Main overfitting risk
Three conditioning variables (price-vs-MA, vol-index-vs-MA, sentiment-vs-MA) each need a
lookback window choice — even dropping the sentiment leg, two remaining free parameters
is enough to invite an undeclared grid search if not frozen before any result is seen.

### Prior Apex overlap
PARTIAL. Two prior experiments (cash-open directional transfer and overnight-range
sweep) both tested the SAME session window (overnight/pre-open) but conditioned
exclusively on PRICE-DERIVED features (gap magnitude, pre-open drift, overnight-range
position, sweep/rejection classification) — never on an external, non-price-derived
regime variable. This candidate is explicitly the "genuinely different information
source, same session" case required to distinguish it from a straight re-test.

### Why it is NOT already disproven
Both prior experiments' own recommendations explicitly ask for "a materially different
hypothesis" or "materially different mechanism" to keep testing US100 overnight/cash-open
dynamics — an external volatility/sentiment regime filter is a different mechanism class
from both experiments' price-derived feature sets, not a retest of either.

### Falsifiable prediction
GOLD/US100's overnight (or session-carry) return conditioned on volatility-index regime
shows no statistically distinguishable difference from the UNCONDITIONAL overnight return
distribution already measured by the prior experiments, once matched-context controls are
applied.

### Minimum viable test
Discovery-study only: bucket the SAME overnight-return series the prior experiments
already built (reuse their frozen event tables where possible) by volatility-regime
tercile, test bucket-mean difference with HAC t-stat + block permutation, no SL/TP/EA.
This explicitly reuses prior infrastructure rather than rebuilding from scratch —
cheapest test on this list to run.

### Verdict from Claude
SOURCE-WORTHY

---

## Summary table (rank order as presented above)

| # | Candidate | Instrument(s) | Prior overlap |
|---|---|---|---|
| 1 | LBMA Gold AM/PM fix window | GOLD | NONE |
| 2 | FOMC pre-announcement drift | GOLD, US100 | PARTIAL (matches a prior experiment's own suggested next step) |
| 3 | External volatility surface (VIX) as regime filter | GOLD, US100 | NONE |
| 4 | Monthly options-expiration (OpEx) dealer-gamma week effect | US100 | PARTIAL (touches a prior calendar-dominance finding) |
| 5 | Cross-instrument cointegrated-spread mean reversion (GOLD/SILVER or XAUUSD/XAUEUR) | GOLD+SILVER or XAUUSD+XAUEUR | NONE (different statistical construction than prior cross-market work) |
| 6 | Overnight hold conditioned on external sentiment/VIX regime | GOLD, US100 | PARTIAL (same session as prior overnight experiments, different info source) |

## Prioritization scoring (0-5 each, /40 total; NOT a profitability score)

Dimensions: source quality, mechanism plausibility, causality, automation, data
availability, cost headroom, novelty vs. prior Apex work, falsifiability. Historical
profitability is explicitly NOT a scoring category (no backtest was run).

| # | Candidate | Source Q | Mechanism | Causality | Automation | Data avail. | Cost headroom | Novelty | Falsifiability | **Total /40** |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LBMA Gold fix window | 5 | 4 | 5 | 5 | 5 | 2 | 5 | 5 | **36** |
| 2 | FOMC pre-announcement drift | 5 | 4 | 5 | 5 | 4 | 4 | 5 | 4 | **36** |
| 3 | VIX regime filter | 4 | 3 | 4 | 3 | 3 | 3 | 5 | 4 | **29** |
| 5 | GOLD/SILVER or XAUUSD/XAUEUR spread mean reversion | 3 | 4 | 4 | 5 | 5 | 2 | 5 | 4 | **32** |
| 6 | Overnight VIX/sentiment-conditioned hold | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | **27** |
| 4 | OpEx dealer-gamma week effect | 4 | 3 | 2 | 3 | 3 | 4 | 3 | 3 | **25** |

Notes on low-scoring dimensions, so the numbers aren't read as opaque: Candidate 1 and 5
score low on Cost Headroom (2/5) because a 1-minute clock-time edge (1) and a two-legged
spread trade (5) both face spread costs that are large relative to the plausible edge size
at Apex's measured GOLD cost structure — this is the single biggest risk flagged in both
candidates' own "transaction-cost risk" fields, not a scoring inconsistency. Candidate 4
scores lowest overall specifically because Causality (2/5) is weak — the true driver
(dealer gamma exposure) is unobservable, only its calendar-date proxy is; this is also why
Claude's own verdict on #4 is NOT-WORTHY despite a real, cited mechanism.

## Recommendation — three to review first

1. **LBMA Gold AM/PM fix window** — zero prior overlap, high automation, directly
   answers the prior regime-audit's call for auction-specific data.
2. **FOMC pre-announcement drift** — literally the prior regime-audit's own suggested
   next step, cheapest to wire up (same pattern as an existing internal calendar-
   blackout mechanism).
3. **GOLD/SILVER or XAUUSD/XAUEUR cointegrated-spread mean reversion** — zero new data
   needed (both legs already cached), and it's a genuinely different statistical
   construction (cointegration) than the prior lead-lag/regression approach.

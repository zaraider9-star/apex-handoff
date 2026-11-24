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

### RESULT (tested 2026-08-20) — REJECT

Narrowed to a single pre-registered, non-directional test per the minimum-viable-test
above: US100 only (no GOLD, no generic VIX), CBOE's NASDAQ-100-specific implied-vol
index (FRED, public, no key) as the external series, causal 252-day percentile regime
(LOW/MID/HIGH terciles, no optimization), prior-day-close-only causality throughout.

**TRAIN** (n=297 days): no state's mean return clears |t|=1 (LOW t=0.12, MID t=-0.73,
HIGH t=0.89), 0/3 pass multiple-testing correction. HIGH-minus-LOW nominal effect
+14.6pts, but a 2000-rep block permutation puts the observed value at only the 59.5th
percentile of chance — required gate was the 97.5th (p≤0.025), missed by a wide margin
(actual p=0.81). **The mandatory matched-control gate fails outright**: pooling on
US100's own realized-volatility regime, calendar month, and prior-day return magnitude
shows that matched context alone already predicts roughly three-quarters of the nominal
HIGH-minus-LOW gap — once that's accounted for, no individual regime state is
distinguishable from its own matched context (all three land well inside the 2.5th-97.5th
percentile noise band).

**VALIDATION** (n=98, frozen construction, run once regardless of TRAIN's result, for
completeness — same choice made for Candidate 1): nominally same sign, but the thinnest
state has only 10 observations and the permutation test is, if anything, further from
significance than TRAIN (p=0.86). Independently confirms REJECT rather than rescuing it.

**Tick verification / cost stress / sealed TEST**: not reached — all conditional on
TRAIN+VALIDATION passing, per the pre-registered stage gates. TEST was never opened.

**Exact reason for stopping**: this is not a marginal single-threshold miss (cf.
Candidate 1) — TRAIN fails the permutation test, the matched-control gate, and the
per-state significance bar simultaneously, and VALIDATION independently corroborates.
Per this test's own pre-registered stopping rule, no percentile-window, realized-vol-
lookback, or filter variant was attempted.

**Next action requested from ChatGPT Research Lead**: confirm closure of Candidate 3 (a
same-shape retest with a different lookback/threshold would be an undeclared
multiple-testing exercise), and indicate which of Candidates 2/6 should be tested next.

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

### RESULT (tested 2026-08-20) — REJECT

Full pre-registered pipeline run exactly as scoped: causal rolling-window hedge ratio,
single |Z| threshold, no grid, no threshold tuning.

**Structural prerequisite (TRAIN)**: strong contemporaneous co-movement (R²≈0.92) but a
fixed-beta cointegration test does not confirm a stable long-run relationship (residual
fails to reject "no cointegration" at any conventional level), and the rolling hedge
ratio is strongly unstable across the training period (two independent stability tests
both reject a constant coefficient at p≈0). Proceeded to the causal rolling design
anyway — pre-registered exactly to handle a time-varying relationship, not a rescue of
the static test.

**TRAIN discovery** (n=549 extreme events, same event set scored at 1/5/10-day
horizons): looked clean in isolation — all three horizons show statistically significant
oriented mean-reversion (HAC t between ~5 and ~7), rising convergence frequency with
horizon, both extreme directions positive, no single-year dominance, and the study's own
orientation-permutation test passes comfortably.

**Null/control — decisive, reverses the verdict.** A matched non-extreme-day control
passes easily. But a randomized-pairing null (one leg's price series randomly
time-shifted, full pipeline rerun on this economically meaningless fake pairing, several
hundred repetitions) reproduces most of the "real" effect at every horizon — the true
pairing's result does not clear the pre-registered significance bar against this null
(p roughly 0.07-0.11 across horizons, vs a required ≤0.025), and at the longest horizon
the real effect doesn't even clear the null distribution's own 95th percentile. A
rolling-refit regression Z-score is mechanically mean-reverting for almost any two
similarly-behaved price series — this candidate's apparent edge does not clear that
bar.

**VALIDATION / tick verification / cost stress / sealed TEST**: not reached — all
conditional on the TRAIN discovery gate passing, per the pre-registered stage gates.
TEST was never opened.

**Exact reason for stopping**: TRAIN's discovery gate requires the real hypothesis to
beat its own null controls, and it fails the randomized-pairing control at every
horizon tested — triangulated by the independent structural-prerequisite finding
(fixed-beta cointegration unconfirmed, hedge ratio unstable). Per this test's own
pre-registered stopping rule: no retuning of the window/threshold, no added filter, no
rescue attempt.

**Next action requested from ChatGPT Research Lead**: confirm closure of Candidate 5 (no
further variants — e.g. do not retest with XAUUSD/XAUEUR as a substitute pairing without
a new, separately-scoped brief), and indicate which of Candidates 2/3/6 should be tested
next.

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

---

# SECOND PASS — 2026-08-20 — 730-document backlog, options/positioning/macro focus

Scope: the ~730-document library expansion flagged as unread in the first pass (`archive_r2/`
108 files, `arxiv/` 516 files, `qp_papers/` 22 files, `quantpedia/` md 82 files) was screened
hierarchically — folder listing → harvest-log title index → grep for priority-topic keywords
(gamma, dealer, open interest, skew, term structure, breadth, real yield, auction imbalance,
etc.) → abstract/conclusion read only for keyword hits → deeper read only for survivors. No
full-document ingestion. Objective for this pass: mechanisms using information NOT reducible
to the traded instrument's own OHLC, weighted toward options positioning, index internals,
macro-surprise, and gold-specific external data; scored for opportunity frequency (2-3/week+
preferred) rather than the prior pass's scheduled-auction/regime-filter framing.

New scoring rubric for Candidates 7-11 (per this pass's brief, /50 not /40 — do not compare
directly to Candidates 1-6's /40 scores above): Source quality, Economic mechanism, New
information, Causality, Automation, Data accessibility, Opportunity frequency, Expected cost
headroom, Falsifiability, Novelty vs Apex — each 0-5. Historical/claimed profit explicitly
excluded from scoring, same rule as pass one.

---

## CANDIDATE 7

**Mechanism:** Gold pays no yield; its opportunity cost is the real (inflation-adjusted)
interest rate. When real yields fall unexpectedly, the opportunity cost of holding
non-yielding gold falls and real-money/macro allocators are incentivized to add gold
exposure; when real yields rise unexpectedly, the reverse. This is a rates/opportunity-cost
relationship, not a price pattern.

**Economic actor:** Real-money macro funds, central-bank reserve managers, systematic
macro/CTA funds that size positions off rate-sensitive relative value.

**Forced/incentivized behavior:** Portfolio rebalancing driven by an opportunity-cost
calculus versus the risk-free real rate — mechanical in aggregate even though any single
fund's trigger is discretionary.

**Observable signal:** Day-over-day change (or level vs. trailing MA) in the 10-Year
Treasury Inflation-Indexed real yield.

**Instrument:** GOLD (secondary).

**Expected frequency:** Daily (the underlying series updates once per trading day).

**Holding horizon:** Session to multi-day.

**Exact external/new information:** Real (inflation-adjusted) Treasury yield level/change —
a rates series, not derivable from GOLD's own OHLC.

**Data source:** FRED series DFII10 (10-Year Treasury Inflation-Indexed Security, Constant
Maturity); alternative causal construction from DGS10 (nominal) minus T10YIE (breakeven
inflation), both also FRED. Free, no key.

**Data access A/B/C/D:** A.

**Automation feasibility:** HIGH — a single daily numeric pull, no scraping or auth. Exact
publication timestamp vs. GOLD's session close must be verified before treating the value
as causally available pre-trade (flagged under failure mode).

**Cost risk:** Low relative to a daily-holding-period signal; the binding constraint is
statistical power (see failure mode), not transaction cost.

**Main failure mode:** (1) Publication-lag risk — must confirm the exact FRED release
timestamp is causally prior to the GOLD session it's meant to condition, or the test will
have an invisible look-ahead leak. (2) The gold/real-yield relationship is well documented
at multi-week/multi-month macro horizons; at daily granularity it may be far noisier and
may not clear a meaningful signal-to-cost bar.

**Prior Apex overlap:** NONE. No prior experiment used a rates/yield-derived series — all
volatility/regime work (including the already-closed Candidate 3) used price-derived or
implied-volatility series, never an interest-rate series.

**Why genuinely different:** A fundamentally different information CLASS (interest-rate /
opportunity-cost data), not another threshold, indicator, or timeframe on price or
volatility.

**Source citation:** General macro-finance literature on gold's negative sensitivity to real
yields (e.g. the "gold vs. real rates" relationship widely documented in central-bank and
market-research literature). Honesty flag: this specific mechanism was NOT located as a
paper inside the 730-document backlog during this pass — it is carried in from general
domain knowledge, not from a source physically inspected this session. Recommend a targeted
follow-up harvest (FRED/BIS/World Gold Council-adjacent literature) before treating the
source-quality score below as equivalent to a corpus-verified candidate.

**Falsifiable prediction:** GOLD's next-session return shows no statistically distinguishable
relationship to the prior session's real-yield change, once matched-controlled against
GOLD's own trend/volatility context.

**Minimum clean test:** Single pre-registered regression/bucket test — GOLD forward return
vs. lagged real-yield daily change — TRAIN/VALIDATION split, HAC t-stat + block permutation,
matched-control against GOLD's own momentum/vol regime (same control discipline that closed
Candidate 3).

**Score /50:** Source quality 2, Economic mechanism 5, New information 5, Causality 4,
Automation 5, Data accessibility 5, Opportunity frequency 3, Cost headroom 4, Falsifiability
5, Novelty vs Apex 5 — **43/50**.

### PRE-REGISTRATION (2026-11-24, owner protocol) — written and committed BEFORE any data was downloaded

Governing protocol: the owner's quant protocol adopted 2026-11-24 (see `DECISIONS.md`).
Everything below is frozen; nothing may be changed after data is seen. Any gate failure =
REJECT and this construction is closed (no retest with other lookbacks, thresholds,
filters, or substitute real-yield series).

**Hypothesis.** A fall in the US 10-Year real yield predicts a positive GOLD return over
the following days (and a rise, a negative one), through lagged opportunity-cost
rebalancing by allocators. Direction is fixed by the mechanism, never fitted.

**Data (public, daily).** FRED `DFII10` (10Y TIPS constant-maturity real yield); FRED `DFF`
(effective fed funds, swap model only); XAUUSD daily OHLC; XAGUSD daily OHLC
(cross-symbol check only). Source hosts and download date recorded in the result.

**Signal.** `dRY_L(t) = DFII10(t) − DFII10(t−L)` over DFII10 observations. Position
direction `d = −sign(dRY_L)`; `dRY_L = 0` → no trade.

**Timing (anti-look-ahead).** A DFII10 value dated *t* is treated as known only at GOLD's
daily close of the first gold trading day strictly after *t*. Entry = that close. This
deliberately gives up one day of signal freshness so that the release-time question
(Treasury end-of-day curve vs. FRED next-morning post) cannot leak. A "same-day close"
variant is reported as a diagnostic only and is NOT eligible for PASS.

**Trade mechanics.** One position at a time (non-overlapping). Exit at the close after H
gold trading days, or at SL. SL = 2.0 × ATR(14, Wilder, through entry day) from entry. From
the first day after entry: if the open gaps beyond SL → exit at the open; else if the
day's range touches SL → exit at SL (worst case, no intrabar optimism). No TP; the time
exit is the profit exit. Result per trade recorded in R = PnL / (entry − SL distance).

**Costs (per trade, real-cost model, stated assumptions).** GOLD: $0.50/oz round trip
(spread + commission + slippage). SILVER: $0.03/oz round trip. Swap per calendar night
held, on notional: long pays (DFF + 2.0%)/360, short receives (DFF − 2.0%)/360 (negative
when DFF < 2%, i.e. short also pays). Cost stress: all costs ×2.

**In-sample optimisation (2020-01-01 → 2022-12-31).** Grid L ∈ {1, 5, 20} × H ∈ {1, 5, 20}
= 9 configs. Selected config = highest IS net PF among configs with ≥30 IS trades.

**Out-of-sample (2023-01-01 → latest available).** All 9 configs evaluated once.

**PASS — every gate required, on the IS-selected config:**
- G1 OOS net PF > 1.15
- G2 OOS trades ≥ 30
- G3 Random-entry control: 10,000 simulations with the same number of long and short
  trades, same H and SL rule, random non-overlapping entry days inside OOS;
  p = (1 + #{PF_sim ≥ PF_real}) / 10,001; require p < 0.05
- G4 Holm step-down over the G3 p-values of all 9 configs, family α = 0.05; the selected
  config must remain significant
- G5 Neighbour robustness: immediate grid neighbours (adjacent L or H) — ≥ 2/3 of them with
  OOS net PF > 1.0
- G6 Cross-symbol: identical frozen config on XAGUSD, OOS net PF > 1.0
- G7 Anchored walk-forward: for each OOS year (2023, 2024, 2025, 2026 YTD) re-select the
  config on all data from 2020-01-01 to the prior year end, trade that year;
  concatenated walk-forward net PF > 1.10
- G8 Monte Carlo drawdown: 10,000 bootstrap resamples of the OOS R-sequence at 1%
  fixed-fractional risk; 95th-percentile max drawdown ≤ 15%
- G9 Cost stress: OOS net PF at 2× costs > 1.0

**Diagnostics (reported, not gating).** HAC (Newey-West) t-stat on per-trade net returns;
long-only / short-only split; PF by calendar year; same-day-close timing variant.

**Ex-ante expectation (recorded before data, not a result).** Low probability of PASS. The
gold–real-yield link is mainly contemporaneous (priced the same day), and it is widely
reported to have weakened from 2022 as central-bank buying decoupled gold from real rates —
the OOS window sits entirely inside that period. A lagged daily rule may have nothing left.

### RESULT (tested 2026-11-24) — REJECT

Run exactly as pre-registered (commit 217ce3a precedes every data download). Data: FRED
`DFII10`, `DFF`; GOLD/SILVER daily OHLC from Yahoo Finance via the GLD / SLV ETFs
(spot-tracking, no futures-roll gaps), with GC=F / SI=F closes used only to convert the
$/oz cost model into a fraction of notional. Substitution reason: the pre-registered
XAUUSD/XAGUSD source (Stooq) now blocks automated download behind a JavaScript check.
GOLD data 2019-01-02 → 2026-11-17. Implementation details the pre-registration left
open, fixed before the run: PF measured in R (matches 1%-risk sizing), re-entry allowed at
the exit-day close, cost stress = spread ×2 and swap markup ×2. 10,000 simulations per
random control, fixed seed.

**All 9 configs, OOS 2023-01-01 → 2026-11-17 (net PF in R, random-entry p):**
L1/H1 0.83 (p 0.89) · L1/H5 1.19 (0.14) · L1/H20 0.88 (0.81) · L5/H1 0.92 (0.51) ·
L5/H5 0.93 (0.61) · **L5/H20 1.30 (0.15)** · L20/H1 0.87 (0.71) · L20/H5 0.96 (0.44) ·
L20/H20 0.97 (0.45). Holm (m=9): no config significant. 6 of 9 configs lose OOS.

**IS-selected config L=5, H=20** (IS PF 1.31, 53 trades):

| Gate | Value | |
|---|---|---|
| G1 OOS PF > 1.15 | 1.30 | pass |
| G2 OOS trades ≥ 30 | 70 | pass |
| G3 random-entry p < 0.05 | 0.147 | **FAIL** |
| G4 Holm-significant | no | **FAIL** |
| G5 neighbours PF > 1.0 (≥ 2/3) | 0.88 / 0.97 / 0.93 — 0 of 3 | **FAIL** |
| G6 XAGUSD OOS PF > 1.0 | 1.13 | pass |
| G7 walk-forward PF > 1.10 | 0.985 | **FAIL** |
| G8 MC 95th-pct max DD ≤ 15% | 16.4% | **FAIL** |
| G9 2× cost PF > 1.0 | 1.19 | pass |

**Diagnostics.** HAC t = 1.27. Long leg PF 2.66 (31 trades), short leg PF 0.55 (39) —
inside an OOS window where GOLD rose +106%. By year: 2023 PF 0.77, 2024 0.84, 2025 1.68,
2026 2.87 — the whole OOS profit comes from the last two years of the bull leg. The
fresher same-day-timing variant is worse (PF 0.77), the opposite of what a real
information effect would show.

**Exact reason for stopping.** The nominal OOS PF of 1.30 is a single isolated parameter
cell riding gold's drift: it does not beat random entries with the same long/short mix
(p = 0.147), no config survives Holm, all three grid neighbours lose, anchored
walk-forward loses, and the profit sits in 2025-2026 only. This is exactly the
"passes on one parameter set / one period" pattern the protocol rejects. Per the
pre-registered stopping rule the construction is closed: no retest with other lookbacks,
thresholds, filters, holding periods, or substitute real-yield series (breakeven-derived,
5Y TIPS, etc.).

---

## CANDIDATE 8

**Mechanism:** Options writers on gold (via GLD-referenced options, captured by CBOE's Gold
ETF Volatility Index, GVZ) systematically price implied volatility above what subsequently
realizes, compensating them for tail/crash risk — a documented volatility risk premium.
The GAP between GVZ (forward-looking, options-market-implied) and GOLD's own trailing
realized volatility is a persistent, time-varying premium that widens/narrows with
institutional hedging demand — an externally sourced (options-market) signal about current
fear/complacency specifically in gold, not derivable from GOLD's own ATR/range features.

**Economic actor:** Gold-options market makers and institutional hedgers buying downside
protection (mining companies, ETF authorized participants, macro funds).

**Forced/incentivized behavior:** Persistent hedging demand for gold puts bids implied vol
above what later realizes; sharp widenings/collapses in that spread reflect shifts in
institutional hedging urgency, not gold's own price action.

**Observable signal:** GVZ level minus GOLD's trailing N-day realized volatility (the
variance/volatility risk-premium spread), or GVZ's own trend/percentile as a simpler proxy.

**Instrument:** GOLD (secondary — but directly the named priority topic for this
instrument).

**Expected frequency:** GVZ is disseminated with both a real-time intraday value and a
daily settlement; daily-close use is straightforward, intraday use needs a live feed.

**Holding horizon:** Session to a few days.

**Exact external/new information:** Options-market-implied gold volatility (GVZ) — not
derivable from GOLD's own OHLC/ATR.

**Data source:** CBOE Gold ETF Volatility Index (GVZ), free historical daily data at
cboe.com's index-data pages.

**Data access A/B/C/D:** A/B — free historical daily download; real-time intraday
dissemination would need a market-data vendor beyond MT5.

**Automation feasibility:** HIGH for a daily-close version; MEDIUM if a real-time intraday
GVZ feed is required.

**Cost risk:** Low at daily granularity; unmeasured whether the signal clears GOLD's spread
if used as a same-day trigger rather than a slower regime filter.

**Main failure mode:** GVZ is derived from GLD (a US-listed equity-options market) with its
own liquidity/positioning dynamics that may only loosely track the COMEX/spot gold Apex
actually trades — a basis-risk failure mode distinct from ordinary signal noise.

**Prior Apex overlap:** NONE. All prior volatility work used either GOLD/US100's own
price-derived volatility or the already-closed NASDAQ-vol level/percentile regime
(Candidate 3) — never a gold-specific options-implied series, and never an
implied-minus-realized SPREAD construction.

**Why genuinely different:** Gold-specific (not the already-rejected NASDAQ-vol
construction), and uses the SPREAD (variance risk premium) rather than a raw level or
percentile — the exact differentiated construction the closed Candidate-3 test's own
language named as clearing the bar ("genuine options-positioning data").

**Source citation:** Quantpedia "Volatility Risk Premium Effect" (aggregating Coval &
Shumway, "Expected Option Returns," and related peer-reviewed sources) — grade A,
"Confidence: Strong" per the aggregator's own label.

**Falsifiable prediction:** GOLD's forward realized volatility and/or directional return
show no statistically distinguishable relationship to the current GVZ-minus-realized-vol
spread, once matched-controlled against GOLD's own recent volatility/momentum.

**Minimum clean test:** Single pre-registered bucket/regression test — GVZ-minus-realized
spread (daily) vs. GOLD forward return and forward realized vol — TRAIN/VALIDATION split,
HAC + permutation, matched-control on GOLD's own volatility regime (same control structure
that closed Candidate 3).

**Score /50:** Source quality 4, Economic mechanism 4, New information 5, Causality 4,
Automation 4, Data accessibility 4, Opportunity frequency 3, Cost headroom 4, Falsifiability
5, Novelty vs Apex 5 — **42/50**.

### PRE-REGISTRATION (2026-11-24, owner protocol) — committed BEFORE GVZ/VXN/NDX data was downloaded

Honesty note: GOLD prices (GLD) were already used in the Candidate 7 test; the implied-vol
series and all US100 data have not been downloaded yet. Same engine, gates G1-G9, cost
model, SL rule, timing lag, random-entry control, Holm family (m = 9), walk-forward, Monte
Carlo and stopping rule as the Candidate 7 pre-registration, except where stated below.

**Hypothesis.** Volatility-risk-premium compensation (Bollerslev-Tauchen-Zhou direction):
when gold's option-implied volatility is unusually far above its realized volatility, the
premium for bearing gold risk is unusually high and subsequent GOLD returns are higher;
unusually low premium → lower returns. Direction fixed by the mechanism.

**Data.** FRED `GVZCLS` (CBOE Gold ETF Volatility Index, daily close); GLD daily OHLC
(as in Candidate 7); FRED `DFF`. Cross-symbol: FRED `VXNCLS` + Yahoo `^NDX`
(fallback `VIXCLS` if `VXNCLS` is unavailable).

**Signal.** RV_N(t) = stdev of the last N daily log returns of the instrument's close ×
√252 × 100. VRP(t) = implied(t) − RV_N(t). z(t) = (VRP(t) − mean) / stdev over the
trailing 252 VRP observations. Direction d = sign(z). Signal dated t is first tradable at
the close of the next trading day.

**Grid (IS 2020-2022).** N ∈ {10, 21, 63} × H ∈ {1, 5, 20} = 9 configs; selection = highest
IS net PF in R with ≥ 30 IS trades.

**G6 cross-symbol (replaces silver).** Identical frozen N, H on US100 with VXN as the
implied series; OOS net PF > 1.0. US100 cost model: 2.0 index points round trip; swap
long pays (DFF + 2.5%)/360, short receives (DFF − 2.5%)/360 per calendar night.

### RESULT (tested 2026-11-24) — REJECT

Run exactly as pre-registered (commit 8510ff4 precedes the GVZ/VXN/NDX downloads). Data:
FRED `GVZCLS`, `VXNCLS`, `DFF`; Yahoo GLD (2018-01-02 → 2026-11-17, 2018 start for
indicator warm-up), `^NDX`. Engine shared with Candidate 7 and verified to reproduce
Candidate 7's numbers exactly before this run.

**OOS net PF in R (random-entry p), all 9 configs:** N10/H1 0.97 (0.41) · **N10/H5 1.08
(0.36)** · N10/H20 0.79 (0.92) · N21/H1 1.13 (0.017) · N21/H5 1.27 (0.10) · N21/H20 1.07
(0.55) · N63/H1 0.95 (0.27) · N63/H5 1.02 (0.29) · N63/H20 1.18 (0.23). Holm (m=9): none
significant.

**IS-selected N=10, H=5** (IS PF 1.33, 162 trades): G1 OOS PF 1.08 **FAIL** · G2 215
trades pass · G3 p = 0.363 **FAIL** · G4 Holm **FAIL** · G5 neighbours 1.27 / 0.97 / 0.79
**FAIL** · G6 US100 (VXN) PF 1.04 pass · G7 walk-forward PF 1.12 pass · G8 MC 95% DD 22.4%
**FAIL** · G9 2× cost PF 1.02 pass. HAC t = −0.13. Long leg PF 1.43, short leg 0.69; by
year 0.76 / 1.09 / 2.02 / 0.66 — one good year (2025).

N21/H1 has the lowest nominal p (0.017), but it was not IS-selected (IS PF 0.92) and
fails Holm (would need p ≤ 0.0056). Picking it after seeing OOS would be data snooping;
not eligible. Construction closed per the stopping rule.

---

## CANDIDATE 9

**Mechanism:** The VIX/VXN futures term-structure SLOPE (not level) encodes the market's
risk-neutral expectation of near-term volatility mean-reversion plus a variance risk
premium. Per the cited source, the slope has documented forecast power for subsequent
volatility-derivative returns. Persistent backwardation coincides with acute stress (forced
de-risking/hedge demand), persistent contango with calm/complacent markets — a state that
could plausibly condition how US100 responds to its own price signals.

**Economic actor:** Volatility-derivatives dealers and hedgers (asset managers buying
protection, funds selling vol for premium) whose aggregate positioning shapes the curve.

**Forced/incentivized behavior:** Dealers must roll and rebalance vega/variance exposure
along the curve; the resulting curve SHAPE reflects forward risk pricing, independent of
any single actor's directional view.

**Observable signal:** NASDAQ-linked implied-vol term-structure slope (front vs. longer-dated
tenor); if a NASDAQ-specific futures curve isn't available, the broader VIX term structure
as a market-wide risk-appetite proxy.

**Instrument:** US100 (primary).

**Expected frequency:** Daily state at minimum; more frequent if futures settlement data is
used.

**Holding horizon:** As a filter on an existing signal — same duration as the base rule; as
a standalone bet, multi-day.

**Exact external/new information:** Term-structure SLOPE of an external, non-US100-derived
volatility index — not level, not derived from US100's own bars.

**Data source:** CBOE VIX/VXN index levels and VX futures settlement prices — free at
cboe.com's index-data and public futures-settlement pages.

**Data access A/B/C/D:** B — free, no key, but assembling a genuine futures-implied term
structure (not just the spot index level) is real engineering, and a NASDAQ-specific
futures curve for VXN may not exist publicly, forcing reliance on the broader VIX curve as
a compromise proxy.

**Automation feasibility:** MEDIUM — needs an external feed merged by timestamp; no
scraping/auth for the free CBOE downloads.

**Cost risk:** None added as a filter; unmeasured as a standalone signal.

**Main failure mode:** This is the candidate most exposed to the already-closed Candidate-3
finding. If slope information correlates heavily with LEVEL (which Candidate 3 already
showed carries ~zero incremental signal once matched-controlled against US100's own
vol/momentum context), the slope construction risks failing the SAME matched-control gate
for the SAME underlying reason — both ultimately reflect the same broad-market volatility
regime. Must be tested with the identical matched-control discipline used to close
Candidate 3, not assumed to pass on construction novelty alone.

**Prior Apex overlap:** PARTIAL. Candidate 3 (VXN level/percentile regime) is closed. This
is a materially different statistical object (slope vs. level — the exact variant the
closed test's own language named as the standing bar a future candidate must clear), but
shares the same underlying data series and the same closure risk.

**Why genuinely different:** Explicitly the differentiated construction named as acceptable
by the closed test's own stopping-rule language.

**Source citation:** Quantpedia "Exploiting Term Structure of VIX Futures" (Simon &
Campasano, EFMA conference paper) — grade A/B, source itself flags out-of-sample alpha
decay.

**Falsifiable prediction:** US100 forward return/volatility conditioned on the term-structure
slope shows no statistically distinguishable difference from the unconditional distribution
once matched-controlled against US100's own volatility/momentum context (identical control
structure to the closed Candidate-3 test).

**Minimum clean test:** Single pre-registered discovery test, slope (not level) as the
conditioning variable, reusing the same TRAIN/VALIDATION infrastructure and matched-control
gate from the closed Candidate-3 test.

**Score /50:** Source quality 4, Economic mechanism 3, New information 3, Causality 3,
Automation 3, Data accessibility 3, Opportunity frequency 3, Cost headroom 3, Falsifiability
4, Novelty vs Apex 2 — **31/50**.

### PRE-REGISTRATION (2026-11-24, owner protocol) — committed BEFORE VIX/VIX3M/NDX data was downloaded

Same engine, gates G1-G9, SL rule, timing lag, random-entry control, Holm family (m = 9),
walk-forward, Monte Carlo and stopping rule as the Candidate 7 pre-registration, except
where stated below. Must clear the same bar that closed Candidate 3 — here that bar is the
random-entry control with matched trade count, since the rule is long/flat.

**Hypothesis.** VIX futures-curve shape as a risk-appetite state: in contango (front
implied vol below 3-month implied vol) dealers and hedgers price calm and US100 earns its
drift; in backwardation (acute stress, forced de-risking) the drift is not paid. Rule is
long/flat: long US100 only in contango, flat in backwardation. No short leg (not tested,
not to be added later).

**Data.** FRED `VIXCLS`, `VXVCLS` (CBOE S&P 500 3-Month Volatility Index), `DFF`; Yahoo
`^NDX` daily OHLC. Cross-symbol: Yahoo `^GSPC`.

**Signal.** ratio(t) = VIX(t) / VIX3M(t); S_M(t) = mean of the last M ratios. d = +1 if
S_M(t) < 1.0, else 0. The 1.0 boundary is the definition of contango vs backwardation,
not a fitted threshold. Signal dated t is first tradable at the close of the next
trading day.

**Grid (IS 2020-2022).** M ∈ {1, 5, 10} × H ∈ {1, 5, 20} = 9 configs; selection = highest
IS net PF in R with ≥ 30 IS trades.

**Costs.** US100: 2.0 index points round trip; US500 (G6): 0.6 points round trip; swap
long pays (DFF + 2.5%)/360 per calendar night. Cost stress: points ×2, markup ×2.

**Random-entry control.** All trades long (matched count), random non-overlapping entry
days inside OOS — tests whether the contango timing beats buying US100 at random.

**G6 cross-symbol.** Identical frozen M, H on US500 (`^GSPC`); OOS net PF > 1.0.

### RESULT (tested 2026-11-24) — REJECT

Run exactly as pre-registered (commit 8510ff4 precedes the VIX/VIX3M/NDX downloads).
Data: FRED `VIXCLS`, `VXVCLS`, `DFF`; Yahoo `^NDX`, `^GSPC` (2018-01-02 → 2026-11-17).
Contango share of days 2020-2026: 92.8%.

**OOS net PF in R (random-entry p), all 9 configs:** M1: 1.10 / 1.32 / 1.59 (p 1.00 /
1.00 / 0.94) · M5: 1.10 / 1.36 / 1.53 (1.00 / 1.00 / 0.95) · M10: 1.09 / 1.34 / 1.58
(1.00 / 1.00 / 0.90) for H = 1 / 5 / 20. Every config loses to random long entries.

**IS-selected M=5, H=1** (IS PF 0.99 — no config was profitable in-sample): G1 OOS PF
1.10 **FAIL** · G2 932 trades pass · G3 p = 1.000 **FAIL** · G4 Holm **FAIL** · G5
neighbours pass · G6 US500 PF 1.05 pass · G7 walk-forward PF 1.39 pass · G8 MC 95% DD
16.9% **FAIL** · G9 2× cost PF 1.05 pass. US100 buy-and-hold over OOS: +148.6%.

**Reason for stopping.** The OOS PFs above 1 are US100's drift: random long entries with
the same trade count do better than contango timing in all 9 configs (median random PF
above the strategy's in every cell). The filter adds no value. Closed per the stopping
rule.

**Observation, not a result.** p = 1.000 means the ~7% of days the filter skips
(backwardation) were followed by above-average US100 returns in 2023-2026 — consistent
with "buy the fear" rebounds. The idea came from looking at OOS data, so it cannot be
validated on 2023-2026. It is logged only; a valid test needs data not yet seen (forward
demo, or a separately pre-registered test on a sample untouched for this hypothesis).

---

## CANDIDATE 10

**Mechanism:** Options market makers who are net SHORT gamma (large open interest
concentrated below spot) must hedge WITH the market's direction — buying as price rises,
selling as it falls — mechanically amplifying moves. When net LONG gamma (large OI
concentrated above spot, common near large expiry strikes), dealers hedge AGAINST the
market's direction, dampening moves and often "pinning" price near large strikes. The
aggregate NDX/QQQ options open-interest-by-strike distribution — not merely the OpEx
calendar date used in the already-shortlisted Candidate 4 — determines an approximate
"zero-gamma" price level whose CROSSING is the actual causal trigger, not the date alone.

**Economic actor:** Options market makers/dealers holding large NDX/QQQ options inventories.

**Forced/incentivized behavior:** Mechanical delta-hedging forced by dealers' own risk
mandates, independent of any market view — the cleanest "forced trade" mechanism found in
this pass.

**Observable signal:** US100/QQQ price relative to an estimated zero-gamma flip level,
computed from published options open interest by strike/expiry.

**Instrument:** US100 (primary).

**Expected frequency:** The flip level itself updates on the OpEx cycle (weekly/monthly),
but price crossing it can happen intraday, plausibly several times/week — closer to target
frequency than the pure calendar-date version.

**Holding horizon:** Hours to a few days (regime persists roughly until the next large OI
rebalancing).

**Exact external/new information:** Options OPEN INTEREST by strike/expiry — genuine
positioning data, neither price nor a calendar date.

**Data source:** OCC (Options Clearing Corporation) daily volume/open-interest reports
(public); CBOE end-of-day options data; QQQ/NDX options chains from a free-tier vendor.

**Data access A/B/C/D:** C — publicly available in principle, but assembling a full
strike-level OI snapshot and estimating a dealer-gamma profile is real data engineering, not
a single CSV pull; genuine intraday updates likely require a paid options-data vendor.

**Automation feasibility:** MEDIUM — the calendar-only version (Candidate 4) is trivial; this
upgrade requires a real pipeline (daily OI ingestion, standard options-pricing-based
dealer-gamma approximation per strike).

**Cost risk:** Standard intraday spread exposure at a flip-level crossing; not structurally
elevated.

**Main failure mode:** The "zero-gamma flip" estimate is a MODEL, not a direct observation —
dealers' net position sign by strike isn't disclosed, only aggregate OI is, so the sign/
magnitude of dealer exposure is inferred, a real methodological assumption that could be
wrong. Also: options OI is naturally available per-underlying (QQQ/NDX specifically) while
Apex trades US100 as a CFD tracking the whole index — a basis-risk gap between the proxy
and the actual options-referenced instrument.

**Prior Apex overlap:** PARTIAL — directly upgrades the already-shortlisted-but-NOT-WORTHY
Candidate 4 (OpEx calendar week effect), whose own stated weakness was "the true driver,
dealer gamma exposure, isn't directly observable; only the calendar date is usable as a
proxy." This candidate proposes closing exactly that gap with real OI data.

**Why genuinely different:** Replaces a calendar-date PROXY with actual options-positioning
data — the single most causally load-bearing upgrade found this pass, and a direct hit on
the brief's dealer-gamma-exposure priority.

**Source citation:** Same academic base as Candidate 4 — Stivers & Sun, "Returns and Option
Activity over the Option-Expiration Week for S&P 100 Stocks" (cited by Quantpedia's
option-expiration-week-effect entry), whose own "fundamental reason" section states the
mechanism explicitly: "Hedge rebalancing by option market makers... is the main reason for
the abnormal stock's returns."

**Falsifiable prediction:** US100 realized volatility and directional persistence show no
statistically distinguishable difference above vs. below the estimated zero-gamma flip
level, once matched-controlled against calendar month (to isolate this from the
already-flagged generic calendar-dominance artifact).

**Minimum clean test:** Build the OI-derived flip-level estimate for a modest pilot window
(not full history) as a discovery-only exercise — bucket US100 forward realized-vol/return
by above/below-flip state, HAC + permutation, matched-control on calendar month.

**Score /50:** Source quality 4, Economic mechanism 5, New information 5, Causality 3,
Automation 2, Data accessibility 2, Opportunity frequency 4, Cost headroom 3, Falsifiability
4, Novelty vs Apex 4 — **36/50**.

---

## CANDIDATE 11

**Mechanism:** NASDAQ-100 index options price in a correlation-risk premium — the index's
implied volatility trades rich relative to a volume/weight-blended implied volatility of its
mega-cap constituents, because option writers demand compensation for correlation risk (the
risk that constituent returns move together in a crash). The SIZE of that wedge (implied
index correlation vs. realized/historical correlation) reflects how "crowded" or "dispersed"
institutional positioning is across the index's small number of dominant mega-cap names —
directly the "mega-cap concentration / constituent dispersion" mechanism named in the brief.

**Economic actor:** Index-options dealers and volatility funds running systematic dispersion
trades (short index vol, long single-name vol, or the reverse).

**Forced/incentivized behavior:** Dealers price and rebalance the correlation-risk premium
as a function of realized cross-constituent correlation and belief dispersion; large swings
in the premium reflect real rebalancing flow, not discretionary judgment.

**Observable signal:** NDX/QQQ implied volatility minus a weight-blended implied volatility
of the top mega-cap constituents (an implied-correlation proxy).

**Instrument:** US100 (primary), via its dominant constituents.

**Expected frequency:** LOW per the source's own construction (monthly rebalance) — flagged
explicitly, per the brief's own rule, rather than rejected outright for frequency.

**Holding horizon:** Monthly as tested by the source; a daily/intraday reframing (does the
wedge predict US100's next-day realized vol or directional persistence, rather than running
the full dispersion trade) is a plausible but unmeasured extension.

**Exact external/new information:** Cross-sectional options-market implied volatility (index
vs. constituents) — genuinely different from any single-series price or volatility feature
tested to date.

**Data source:** Individual mega-cap equity options implied volatility (CBOE delayed
quotes, free tier) plus NDX/QQQ index options implied volatility (CBOE, free tier).

**Data access A/B/C/D:** C — each leg is individually quotable via free delayed data, but
assembling and weighting several constituents' IV consistently, and maintaining the mapping
as index weights change, is real ongoing engineering.

**Automation feasibility:** MEDIUM — deterministic once the pipeline exists; the pipeline
itself (multi-leg options IV collection + weighting) is nontrivial.

**Cost risk:** Not evaluated at intraday granularity (source uses monthly rebalancing);
unmeasured whether a daily/intraday reframing changes the cost picture.

**Main failure mode:** NDX's true weighting includes far more names than a handful of
mega-caps; using only the largest names as a proxy for "the index's constituent volatility"
is itself an approximation that could miss the dispersion the mechanism claims to capture.

**Prior Apex overlap:** NONE — no prior experiment has used cross-sectional single-name
options data; prior "breadth"/"internals"-adjacent ideas were parked as data-infeasible
(see rejected-concepts list, pass one, breadth-confirmation entry).

**Why genuinely different:** Options-market, cross-sectional, correlation-risk-premium
construction — none of these three elements (options data, cross-sectional, correlation
premium) has been tested in any form before.

**Source citation:** Quantpedia "Dispersion Trading" (Buraschi, Trojani, Vedolin,
"Equilibrium Index and Single-Stock Volatility Risk Premia"; Driessen, Maenhout, Vilkov,
"Option-Implied Correlations and the Price of Correlation Risk") — grade A, "Confidence:
Strong."

**Falsifiable prediction:** US100's forward realized volatility/return shows no
statistically distinguishable relationship to the index-vs-constituent implied-vol wedge,
once matched-controlled against US100's own volatility/momentum context.

**Minimum clean test:** Single pre-registered discovery test using a small, frozen
constituent basket (top-N by index weight, fixed before any result is seen) — bucket US100
forward vol/return by wedge tercile, HAC + permutation, matched-control.

**Score /50:** Source quality 4, Economic mechanism 4, New information 5, Causality 3,
Automation 2, Data accessibility 2, Opportunity frequency 1, Cost headroom 3, Falsifiability
4, Novelty vs Apex 5 — **33/50**.

---

## Second-pass summary table (rank order by /50 score)

| # | Candidate | Instrument | Data access | Freq. | Score /50 |
|---|---|---|---|---|---|
| 7 | Real-yield (TIPS) impulse → GOLD allocator flow | GOLD | A | Daily | **43** |
| 8 | GVZ implied-minus-realized vol spread | GOLD | A/B | Daily | **42** |
| 10 | Dealer zero-gamma flip level (options OI) | US100 | C | Several/week | **36** |
| 11 | Index-vs-constituent implied-vol dispersion wedge | US100 | C | Monthly | **33** |
| 9 | VIX/VXN term-structure slope | US100 | B | Daily | **31** |

## Rejected/parked concepts, this pass (logged so they aren't rediscovered)

- **Gold options vs. gold futures, Indian MCX** (archive_r2 PDF) — a PhD research
  *protocol* (no results yet), Indian MCX market, no falsifiable rule. REJECTED — no
  operational content.
- **"Essays in market microstructure — information content of quotes"** (archive_r2 PDF,
  PhD dissertation synopsis) — generic order-driven-market quote theory. REJECTED — HIGH
  overlap with the already-closed tick/quote-microstructure experiment; no gold/index-
  specific mechanism.
- **Market sentiment + overnight anomaly** (Quantpedia) — its VIX leg is a LEVEL/MA
  condition (same construction as the closed Candidate 3), and one-third of its filter
  relies on a proprietary paid sentiment indicator. REJECTED — no genuinely new,
  accessible information source once the paid leg is dropped.
- **"On options-driven realized volatility forecasting"** (arXiv, rough-volatility +
  deep-learning HAR-RV model) — a pure forecasting-accuracy paper, no actor/mechanism
  (fails the brief's own WHO/WHY standard). REJECTED as a standalone candidate; kept as
  supporting evidence that option-implied volatility carries genuine incremental
  information (relevant background for Candidate 8, not an independent candidate).
- **"Clearing price distributions in call auctions"** (arXiv 1904.07583) — a real
  order-flow-imbalance model for opening/closing auctions, matching the brief's auction-
  imbalance priority exactly, but real-time NASDAQ-100-constituent auction-imbalance data
  (Nasdaq's Net Order Imbalance Indicator) is not confirmed freely accessible. PARKED
  (data infeasibility, not overlap) — re-check Nasdaq NOII free-tier access before
  reviving.
- **Option-expiration (OpEx) week effect, generic calendar-only form** — already logged
  as shortlisted Candidate 4 in pass one; not re-counted as new here. Candidate 10 is the
  positioning-data upgrade of this same concept.
- **~15 of the 82 Quantpedia entries**: time-series/asset-class/currency/commodity
  momentum, carry, and term-structure families — HIGH overlap, matches the already-closed
  duplicate-elimination list (TSMOM, FX carry, commodity term structure). Bulk REJECTED.
- **~25 of the 82 Quantpedia entries**: single-stock equity factors (accrual anomaly,
  asset-growth effect, R&D-expenditure effect, net-payout-yield, short-interest effect,
  earnings-announcement premium, etc.) — wrong instrument class entirely (Apex trades
  GOLD/US100, not single-name equities). Bulk REJECTED, out-of-scope-instrument.
- **Pairs-trading-with-stocks/country-ETFs, 13F alpha-cloning, soccer-club-stock
  arbitrage** — out-of-scope instruments or unautomatable lag (13F filings are
  quarterly). Bulk REJECTED.
- **Calendar-seasonality Quantpedia entries** (turn-of-month, January effect, pre-holiday
  effect, payday anomaly, Ramadan effect) — squarely "another session/another calendar
  bucket" on OHLC, the exact pattern the research-state's calendar-dominance finding
  already warns against. Bulk REJECTED per the brief's own anti-duplication rule.
- **Generic strategy-compendium books** (`151-trading-strategies`, `51-trading-strategies`,
  Wilder *New Concepts*, Pring *On Market Momentum*, Stridsman *Trading Systems That
  Work*) — indicator/pattern-catalog families, HIGH overlap with the already-closed
  indicator-catalog and candlestick audits. Bulk REJECTED, no new angle found.

---

# THIRD PASS — 2026-11-24 — owner protocol, public daily data

Candidates 12-14 are new mechanisms not in `CONCEPT_INDEX.md` or the closed list. All three
are pre-registered here and committed BEFORE their new data series (IEF, QQQ, SPY, and
pre-2018 index/VIX history) were downloaded. Same engine, cost models, SL rule
(2×ATR(14)), timing lag, random-entry control (10,000 sims), Holm family per candidate,
Monte Carlo and stopping rule as Candidate 7, except where stated.

Project-level multiplicity note: each candidate gets its own Holm family. Across the
project many candidates are tested, so a single PASS is still provisional until the
≥ 30-trade demo forward test, which is the final out-of-sample arbiter under the owner
protocol.

## CANDIDATE 12 — Month-end balanced-fund rebalancing flow (US100 / US500)

**Mechanism.** Pension and balanced funds holding fixed stock/bond weights rebalance at
month-end. When stocks have outperformed bonds month-to-date they must sell equities into
the month-end close; when stocks have underperformed they must buy. Forced, calendar-timed
flow conditioned on an external variable (bond returns), not pure seasonality.
**Source.** General market-microstructure literature on pension rebalancing flows (e.g.
recent academic work on predictable month-end equity returns from rebalancing). Honesty
flag: not located in the project library; carried in from general domain knowledge, same
caveat as Candidate 7.

**Signal.** spread(t) = S&P 500 (`^GSPC`) month-to-date price return − IEF month-to-date
total return (Yahoo adjusted close), both from the prior month's last close to close t.
Entry at the close of the trading day k days before the month's last trading day, using
spread measured through the close of the day before entry; d = −sign(spread) if
|spread| > τ, else no trade. Exit H = k days later = the month's last-trading-day close (or
SL). The final, incomplete month in the data is excluded.

**Grid (IS 2020-2022).** τ ∈ {0%, 1%, 2%} × k ∈ {1, 3, 5} = 9 configs (H = k). Selection:
highest IS net PF in R with ≥ 30 IS trades. OOS 2023-01-01 → latest. Gates G1-G9 as in
Candidate 7. Traded instrument US100 (`^NDX`); G6 = US500 (`^GSPC`).

## CANDIDATE 13 — Overnight drift (US100 / US500)

**Mechanism.** A documented concentration of US equity-index returns in the overnight
(close → next open) segment rather than the trading session (e.g. Cliff-Cooper-Gulen on
day/night return differences; NY Fed staff work on the overnight drift in index futures),
attributed to overnight inventory/hedging-demand imbalances. Base mechanism of Candidate 6,
without the closed VIX-level conditioning. Not in the closed list (EXP010/EXP011 studied
gap direction and overnight-range sweeps, not the overnight holding premium).

**Rule.** Long at each trading day's close, exit at the next trading day's open. No
parameters → no optimisation, Holm m = 1. Prices: QQQ (US100) and SPY (US500) open/close
(actual traded prints; the `^NDX` index open is partly stale). Costs: US100 2.0 points /
US500 0.6 points round trip on the index level, swap per calendar night as before
(weekends = 3 nights). SL 2×ATR(14) fixes R; an open beyond SL exits at the open (same
price).

**Gates.** G1 OOS PF > 1.15 · G2 ≥ 30 trades · G3/G4 control: 10,000 sims, each day
independently assigned at random (p = 0.5) to the overnight segment or the following
intraday segment (open → close, same SL rule, spread cost, no swap); p = share of sims with
PF ≥ real, require p < 0.05 · G5 (no parameter neighbours) replaced by: ≥ 3 of 4 OOS
calendar years with PF > 1.0 · G6 US500 OOS PF > 1.0 · G7 (no parameters to walk forward)
replaced by: IS 2020-2022 PF > 1.0 · G8 MC 95% DD ≤ 15% · G9 2× cost PF > 1.0.

## CANDIDATE 14 — Backwardation "buy the fear" on US100 (separate sample)

**Origin and deviation, stated up front.** This hypothesis came from the Candidate 9
observation (2023-2026), so 2020-2026 is contaminated for it and cannot be used as
validation. Protocol deviation (sample dates only): IS 2008-01-01 → 2013-12-31,
OOS 2014-01-01 → 2019-12-31, a period not examined for this hypothesis (2018-2019 index
prices were loaded only as indicator warm-up for Candidates 8-9; no conditioned statistic
was computed on them). All gates otherwise identical. A PASS here is still provisional
until the demo forward test.

**Mechanism.** VIX above VIX3M (backwardation) marks forced de-risking and hedge demand;
risk premia are temporarily elevated, so subsequent US100 returns are higher.

**Rule.** d = +1 (long) if S_M(t) = mean of the last M VIX/VIX3M ratios > 1.0, else flat.
Signal dated t tradable at the next day's close. Grid M ∈ {1, 5, 10} × H ∈ {1, 5, 20}.
Walk-forward years 2014-2019. G6 = US500. 2020-2026 results reported for information only
(contaminated, not gating).

## THIRD PASS — RESULTS (tested 2026-11-24)

Data downloaded after commit 0eaa339: Yahoo `IEF`, `QQQ`, `SPY`, `^NDX`, `^GSPC`
(2007-01-03 → 2026-11-17, adjusted close used only for IEF's total return); FRED `DFF`,
`VIXCLS`, `VXVCLS` from 2007. Engine re-verified against Candidate 7 after generalisation.

### Candidate 12 — REJECT (7 of 9 gates failed)

OOS net PF in R (random p) for τ = 0 / 1% / 2%: H1 2.35 (0.008) / 2.62 (0.006) / 1.94
(0.055) · H3 1.30 / 1.44 / 1.37 · H5 0.88 / 0.91 / 0.84. IS-selected τ=1%, k=H=5 (IS PF
1.40): OOS PF 0.91, p = 0.42, neighbours 0.88 / 0.84 / 1.44, US500 0.89, walk-forward 0.60,
2× cost 0.84; only G2 (34 trades) and G8 (DD 7.9%) pass. The H=1 cells look strong OOS
but were the worst in-sample (IS PF 0.76 and 0.47) — a sign flip between periods, and
neither clears Holm (p 0.006 vs required ≤ 0.0056). Selecting them after seeing OOS would be
data snooping. Closed.

### Candidate 13 — REJECT (4 of 9 gates failed)

972 OOS nights. Overnight PF 1.11 vs intraday 1.04, random-segment median 1.07; control
p = 0.27. Years 0.98 / 1.33 / 1.20 / 0.95 (2 of 4 > 1); IS 2020-2022 PF 0.98. Passes US500
(1.02), MC DD (10.5%), 2× cost (1.03). HAC t = 1.30. The overnight premium is not
distinguishable from random segment choice at CFD cost. Closed.

### Candidate 14 — REJECT (2 of 9 gates failed) — closest result in the project so far

Sample 2008-2019 as pre-registered. Backwardation share of days: 15.8% IS, 8.0% OOS.
OOS (2014-2019) net PF in R (random p): M1 1.24 (0.18) / 1.62 (0.18) / 2.17 (0.060) ·
M5 1.21 / 1.23 / 1.74 · M10 1.62 / 2.67 / 2.73 for H = 1 / 5 / 20. No config Holm-significant.

IS-selected M=1, H=20 (IS PF 1.34, 41 trades):

| Gate | Value | |
|---|---|---|
| G1 OOS PF > 1.15 | 2.17 | pass |
| G2 OOS trades ≥ 30 | 33 | pass |
| G3 random-entry p < 0.05 | 0.060 | **FAIL** |
| G4 Holm-significant | no | **FAIL** |
| G5 neighbours | 1.74 / 1.62 | pass |
| G6 US500 OOS PF | 2.40 (32 trades) | pass |
| G7 walk-forward PF | 2.33 | pass |
| G8 MC 95% DD | 9.5% | pass |
| G9 2× cost PF | 2.02 | pass |

HAC t = 3.11; every OOS year profitable (PF 3.84 / 1.73 / 1.49 / one trade / 1.44 / 1.82);
win rate 54.5%, avg win 2.03R, avg loss −1.12R. Contaminated 2020-2026 period (information
only): 28 trades, PF 1.24.

**Reason for REJECT.** Random long entries in the same 2014-2019 window have a median PF
of 1.27 (US100 +145% over the period); 6% of random sims reach PF ≥ 2.17, above the 5%
limit, and no config survives Holm. With only 33 trades the test lacks the power to
separate the timing effect from the bull-market drift. Per the stopping rule the
construction is closed: no re-test with other M/H, thresholds, filters, or periods.

**Owner-decision option (not a trade, no capital).** The only clean way to learn more is
data nobody has seen: log the frozen M=1/H=20 signal going forward as a paper shadow
record. That record would be a new test with its own pre-registration; it does not
qualify the strategy for demo or live under the protocol.

## CANDIDATE 2 — PRE-REGISTRATION (2026-11-24, owner protocol, daily construction)

Committed BEFORE any FOMC-conditioned statistic was computed. Honesty note: the price
series (`^NDX`, `^GSPC`, GLD) were already downloaded for other tests; no statistic
conditioned on FOMC dates has been computed on them.

**Events.** Regularly scheduled FOMC statement days (second meeting day), verified against
federalreserve.gov meeting calendars: 2020 Jan 29, Apr 29, Jun 10, Jul 29, Sep 16, Nov 5,
Dec 16 (the cancelled Mar 17-18 meeting and the unscheduled Mar 2/15 meetings excluded);
2021 Jan 27, Mar 17, Apr 28, Jun 16, Jul 28, Sep 22, Nov 3, Dec 15; 2022 Jan 26, Mar 16,
May 4, Jun 15, Jul 27, Sep 21, Nov 2, Dec 14; 2023 Feb 1, Mar 22, May 3, Jun 14, Jul 26,
Sep 20, Nov 1, Dec 13; 2024 Jan 31, Mar 20, May 1, Jun 12, Jul 31, Sep 18, Nov 7, Dec 18;
2025 Jan 29, Mar 19, May 7, Jun 18, Jul 30, Sep 17, Oct 29, Dec 10; 2026 Jan 28, Mar 18,
Apr 29, Jun 17, Jul 29, Sep 16, Oct 28. IS 2020-2022 = 23 events, OOS 2023-2026 = 31.

**Rule (no free parameters, fixed by the source).** Long US100 at the close of the trading
day before the statement day, exit at the statement-day close (or SL 2×ATR(14)). The
calendar is published in advance, so no signal lag is needed. Costs and swap as US100 model.

**Gates.** G1 OOS PF > 1.15 · G2 OOS trades ≥ 30 · G3/G4 random-entry control: 31 random
non-overlapping 1-day long trades inside OOS, 10,000 sims, p < 0.05 (Holm m = 1) ·
G5' neighbour: 2-day variant (entry two trading days before, same exit) OOS PF > 1.0 ·
G6 US500 OOS PF > 1.0 · G7' IS 2020-2022 PF > 1.0 · G8 MC 95% DD ≤ 15% · G9 2× cost PF > 1.0.
GOLD (GLD) with the same rule reported as a diagnostic only.

### CANDIDATE 2 — RESULT (tested 2026-11-24) — REJECT (3 of 8 gates failed)

IS 2020-2022: 23 events, PF 2.13. OOS 2023-2026: 31 events, PF 1.08 (G1 **FAIL**), random
1-day long entries median PF 1.15, p = 0.554 (G3/G4 **FAIL**), US500 PF 0.70 (G6 **FAIL**).
Passes: 31 trades, 2-day variant 1.19, IS PF > 1, MC DD 4.5%, 2× cost 1.05. HAC t = 0.36,
mean net +6.4 bp per event. By year 1.39 / 1.05 / 3.28 / 0.40. GOLD diagnostic PF 1.36
(31 events, not gating). The strong IS result does not carry into OOS and the drift is no
better than a random US100 day — consistent with published evidence that the pre-FOMC
drift faded after the mid-2010s. Closed per the stopping rule.

### CANDIDATE 14 — SHADOW (paper) PRE-REGISTRATION (2026-11-24, owner-approved)

Paper only — no orders, no demo, no capital. Purpose: collect data nobody has seen. Does not
change Candidate 14's REJECT verdict.

**Rule (frozen, IS-selected config M=1, H=20).** Long US100 at a session's close when the
latest FRED VIX/VIX3M daily close ratio dated strictly before that session is > 1.0. SL =
entry − 2×ATR(14, Wilder, `^NDX` daily). Exit at SL (gap beyond SL → open) or at the close
20 sessions after entry. One position at a time; re-entry allowed at the exit-session close.
Costs: 2.0 index points round trip, swap long (DFF + 2.5%)/360 per calendar night.
**Owner risk rules applied** (unlike the backtest engine): after 2 consecutive losses no
new entry that session; realized −3% in a session or −6% in an ISO week blocks new
entries; 1% risk per trade; entries at the 16:00 New York close sit outside tier-1 release
windows.

**Implementation check.** `shadow/run_shadow.py` replayed on 2014-2019 reproduces 31 of the
33 backtest trades to 1e-6 R; the other 2 are delayed one session by the 2-loss rule
(replay PF 2.20 vs backtest 2.17).

**Start.** Flat; first eligible session 2026-11-24. The ledger is rebuilt from the start on
every run (stateless) and committed with a daily report (`shadow/STATUS.md`,
`shadow/reports/`, `shadow/ledger.csv`).

**Evaluation (pre-registered).** At 30 closed shadow trades: PF > 1.15 AND a random-entry
control on the shadow period (same method, matched trade count) at p < 0.05 → eligible to
be proposed to the owner for a demo forward test. Otherwise closed for good. Interim reports
carry no decision weight. Expected pace from history: ~5 trades/year (33 in 2014-2019, 28
in 2020-2026), so 30 trades ≈ 5-7 years.

---

# FOURTH PASS — 2026-11-24 — intraday, real bid/ask

## CANDIDATE 15 — End-of-day hedging-demand momentum (US100 / US500) — PRE-REGISTRATION

Committed BEFORE any intraday data was downloaded (the Dukascopy feed was not yet reachable
when this was written).

**Mechanism.** Option dealers who are short gamma, and leveraged/inverse ETFs that must
rebalance to their daily multiple, trade in the direction of the day's move near the cash
close; the resulting flow makes the return from the previous close to late afternoon
predict the last-30-minute return (Baltussen, Da, Lammers & Martens, "Hedging demand and
market intraday momentum", Journal of Financial Economics 2021; related: Gao, Han, Li &
Zhou, "Market intraday momentum", JFE 2018). Source quality A (peer-reviewed), carried from
general literature, not located in the project library. Prior overlap: PARTIAL with EXP004
(opening-drive momentum) — different trigger (whole-day move into a forced end-of-day flow),
different window (close, not open).

**Data.** Dukascopy minute BID and ASK candles: `USATECHIDXUSD` (US100), `USA500IDXUSD`
(US500), UTC timestamps converted to New York time; trading calendar = sessions present in
Yahoo `^NDX` daily data; daily ATR(14, Wilder) from Yahoo `^NDX` / `^GSPC` through the prior
session. Early-close sessions excluded by a fixed pattern (Friday after Thanksgiving;
Dec 24 and Jul 3 when Monday-Thursday), consistent with NYSE calendars confirmed for
2023-2026.

**Signal.** P_prev = mid close of the 15:59 New York minute of the previous session.
At entry time T, r = mid close of minute T−1 / P_prev − 1. If |r| > τ: d = sign(r).
**Fills (real spread).** Long enters at the ASK close of minute T−1, short at the BID close;
long exits at the BID close of the 15:59 minute, short at the ASK close; plus slippage 0.5
point (US100) / 0.15 point (US500) per side. No swap (intraday).
**SL.** 0.5 × daily ATR(14) from the entry price, checked minute by minute on the side the
position would close at (gap beyond SL at a minute's open → exit at that open). R = net PnL /
SL distance.

**Grid (IS 2020-2022).** τ ∈ {0, 0.25%, 0.5%} × T ∈ {15:00, 15:30} = 6 configs; selection =
highest IS net PF in R with ≥ 30 IS trades. OOS 2023-01-01 → latest complete session.

**Gates (all required, IS-selected config).** G1 OOS PF > 1.15 · G2 ≥ 30 OOS trades · G3
random-entry control: 10,000 sims, same number of long and short trades, same T and exit,
placed on random OOS sessions, p < 0.05 · G4 Holm over the 6 configs' G3 p-values · G5 ≥ 2/3
of grid neighbours with OOS PF > 1.0 · G6 US500 same frozen config OOS PF > 1.0 · G7
anchored yearly walk-forward PF > 1.10 · G8 MC 95th-pct DD ≤ 15% at 1% risk · G9 cost
stress (spread paid ×2, slippage ×2) PF > 1.0. Any failure = REJECT, construction closed.

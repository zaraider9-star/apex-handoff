# CONCEPT INDEX — raw extraction before final ranking

Every concept considered during this extraction pass, before the duplicate-elimination
and ranking steps that produced `CLAUDE_TO_CHATGPT.md`. Rawer than that file on purpose —
rejected concepts stay visible with a one-line reason so they aren't rediscovered later.
Grouped by mechanism family. Source citations are metadata only (title/author, or a
public identifier like an arXiv ID / Quantpedia entry name) — never reproduced text.

## A. Auction / scheduled institutional flow (new information-source class)

1. **LBMA Gold AM/PM fix window** — gold's own twice-daily official benchmark auction
   concentrates institutional flow into a narrow window, by analogy with a documented
   effect around the FX 4pm WM/Reuters fix (academic microstructure paper, grade A). NONE
   overlap with prior Apex work. → SHORTLISTED.
2. **FOMC pre-announcement drift** — scheduled monetary-policy calendar event; drift
   concentrated in the hours BEFORE the announcement (Quantpedia, grade A). NONE overlap
   (prior opening-drive work tested price-derived momentum, not a macro-calendar
   condition). → SHORTLISTED.
3. **Monthly index options-expiration (OpEx) week** — dealer delta-hedge rebalancing
   around index options expiry (Quantpedia, grade A, equities-specific). PARTIAL overlap
   with a prior finding that calendar month explains more variance than any causal
   regime — but that prior work never tested *why*; this gives a specific causal driver.
   → SHORTLISTED (flagged MEDIUM automation feasibility — the true driver, dealer gamma
   exposure, isn't directly observable; only the calendar date is usable as a proxy).

## B. External volatility surface / positioning proxy (new information-source class)

4. **VIX level / term structure as an external regime filter** — volatility NOT derived
   from the traded instrument's own price (Quantpedia, grade A/B). NONE overlap — all
   prior volatility features were computed from the instrument's own bars. →
   SHORTLISTED.
5. **Synthetic lending-rate / aggregate short-selling-cost proxy** predicts next-day
   equity-index direction (Quantpedia, grade A). Genuinely new information source
   (positioning, not price). REJECTED for this shortlist — no accessible free data feed;
   the source data requires a paid subscription. Kept here so it isn't rediscovered
   without first checking data access.
6. **Overnight-hold conditioned on an external sentiment/volatility gauge** rather than
   on price-derived overnight-gap features (Quantpedia, grade A). PARTIAL overlap (same
   session window as prior overnight work) but a different INFORMATION SOURCE (external
   vol+sentiment vs. price-derived gap/pre-open features). → SHORTLISTED, flagged
   explicitly as partial overlap requiring justification.

## C. Cross-instrument statistical arbitrage (distinct construction from prior work)

7. **Cointegrated-spread mean reversion** — a commodity-pair spread-trading template
   (Quantpedia, grade B, source itself reports OOS decay) adapted to a precious-metals or
   FX-cross pair Apex already has data for. Distinct statistical construction from prior
   cross-market work (which used a regression-beta/lead-lag test, not a mean-reverting-
   spread test). NONE overlap on the specific construction. → SHORTLISTED.
8. **Index-breadth participation-ratio confirmation** (grade B source) — a different
   signal than plain price correlation. Interesting but requires index-constituent
   breadth data Apex doesn't have cached; parked as a REJECT for now on data
   infeasibility, not merged into #7.
9. **FX carry trade / dollar carry / currency momentum** (Quantpedia, grade A/B) —
   genuinely different info source (interest-rate differentials) but REJECTED: the
   broker's FX universe is far short of what the cross-sectional construction needs, and
   the core mechanism is the same family as time-series momentum and COT positioning,
   both already rejected in prior work.
10. **Time-series momentum / commodity momentum / commodity term structure**
    (Quantpedia ×3, grade A) — HIGH overlap, time-series momentum already tested and
    rejected; commodity term structure needs a futures curve the broker doesn't provide.
    REJECTED.

## D. Price-pattern / indicator families (near-total overlap with prior work)

11. Liquidity sweep + rejection + displacement (many variants across the library:
    spike-and-climax, Wyckoff spring/upthrust, smart-money-concept sweep+fair-value-gap,
    structural break-of-structure/change-of-character) — HIGH overlap, five separate
    prior experiments all REJECTED on this exact family. REJECTED, no new angle found.
12. Opening-range breakout / opening-drive continuation (multiple library variants) —
    HIGH overlap, three separate prior experiments all REJECTED. REJECTED.
13. Candlestick reversal patterns, any variant — HIGH overlap, a three-round pattern
    audit (204→463→80 tests) killed the entire standard candlestick-pattern catalog plus
    context filters. REJECTED.
14. Moving-average/RSI/Stochastic/MACD/CCI crossovers or extremes or divergence,
    Bollinger squeeze (dozens of library instances) — HIGH overlap, an indicator-catalog
    audit plus a dedicated crossover study plus 22 previously-tested new book-derived
    rules already cover this exhaustively. REJECTED.
15. Trend/DMI/ADX-filtered swing systems — HIGH overlap, same indicator-catalog family;
    two live trend-following bots already independently rejected at real cost. REJECTED.
16. Grid/martingale/scale-down averaging (multiple historical and modern variants) —
    HIGH overlap, a prior grid-EA experiment was REJECTED before implementation on the
    exact same mean-reversion-grid mechanism. REJECTED — several of these sources are
    also grade D specifically for recommending this.
17. Trailing-stop trend-following on raw momentum — HIGH overlap, already tested: a real
    brute edge exists but needs very high trade frequency, cost eats it, and the entry
    signal itself is indistinguishable from random. REJECTED.

## E. Discretionary / unmeasurable (rejected on the automation criterion, not overlap)

18. "Beautiful"/"clean" pattern-quality judgments (multiple library sources) — REJECTED,
    the task's own screening criteria explicitly exclude discretionary-interpretation
    concepts unless translatable into deterministic rules, and none of these sources
    provide one.
19. Smart-money-vs-retail volume-divergence indicator (older academic paper, grade C) —
    REJECTED, needs true traded volume the platform doesn't provide for FX/CFD
    instruments (only a tick-count proxy), and the paper's own evidence base is thin.
20. Trader-level order-flow lead-lag networks (academic paper, grade A source) —
    REJECTED for data infeasibility only (the mechanism itself is sound) — no retail
    account can access trader-level positioning data. Kept here in case a data source is
    ever found.
21. Deep reinforcement-learning forex agent (academic paper, grade C) — REJECTED, the
    source's own zero-spread/equal-bid-ask assumption is disqualifying, and a simpler
    feature-based ML experiment already run internally scored below coin-flip after real
    cost — a more complex model is a worse starting bet, not a better one.

## Tally

- Concepts extracted: **21**
- Rejected as duplicate of a prior Apex family: **11** (#9-#17)
- Rejected for poor source/evidence or data infeasibility: **5** (#5, #8, #19, #20, #21)
- Rejected for discretion/unmeasurability: **1** (#18)
- Carried to the final shortlist (`CLAUDE_TO_CHATGPT.md`): **6** (#1, #2, #3, #4, #6, #7)

## Source-quality distribution (library inspection pass)

66 distinct sources were inspected directly this pass (spanning roughly 50 book/paper
titles plus a sample of aggregator entries). Grades score the evidence and mechanism
quality of the source itself, independent of whether a strategy derived from it has
already failed in Apex.

| Grade | Count | Meaning |
|---|---|---|
| A — high quality | 15 | Clear mechanism, falsifiable claims, credible methodology, often with source-reported statistics |
| B — useful | 15 | Plausible mechanism, usable definitions, limited empirical evidence |
| C — weak/unverified | 24 | Anecdotal or recycled-default-indicator content, codeable but no backtest evidence |
| D — trash/do not use | 12 | No falsifiable rule, martingale/averaging-down actively recommended, or pure historical/marketing narrative with zero operational content |

The 12 grade-D sources were historical-narrative or marketing material with no
operational content, or material actively recommending martingale/averaging-down/
simultaneous buy-and-sell hedging as a way to guarantee profit — none were force-graded
up regardless of length or fame, and none contributed a usable concept.

A known gap, carried forward rather than silently dropped: a large recent library
expansion (roughly 730 additional documents, mostly academic papers and a strategy-
research aggregator) has not yet been digested/summarized and is largely unread. A
future pass should process that backlog — weighted toward macro/volatility/carry/
commodity topics, the areas most likely to contain a genuinely new information source —
before mining it for candidates.

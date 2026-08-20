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

---

# SECOND PASS — 2026-08-20 — 730-document backlog screen

Coverage this pass: the previously-flagged unread ~730-document expansion
(`archive_r2/` 108 files, `arxiv/` 516 files, `qp_papers/` 22 files, `quantpedia/` md 82
files) screened hierarchically — folder/title index, harvest-log grep for priority
keywords (gamma, dealer, open interest, skew, term structure, breadth, real yield, auction
imbalance, etc.), abstract/conclusion read for keyword hits, deeper read only for
survivors. No full-document ingestion; no backtest run.

## F. Rates / macro-surprise (NEW information source class)

22. **Real-yield (TIPS) impulse as GOLD's opportunity-cost driver** — 10Y real Treasury
    yield (FRED DFII10, grade A/free data, general macro-finance literature not located
    inside this pass's corpus — flagged honestly). NONE overlap — no prior experiment used
    a rates/yield series. → SHORTLISTED (Candidate 7).

## G. Gold-specific options-market information (NEW information source class)

23. **GVZ (CBOE Gold ETF Volatility Index) implied-minus-realized volatility spread** —
    options-market-implied gold volatility vs. GOLD's own trailing realized vol (Quantpedia
    volatility-risk-premium-effect, grade A). NONE overlap — prior work never used a
    gold-specific options-implied series nor an implied-minus-realized spread. →
    SHORTLISTED (Candidate 8).

## H. Index-options positioning / internals (NEW information source class, upgrades a
    prior calendar-only proxy)

24. **VIX/VXN term-structure SLOPE (contango/backwardation) as a US100 regime filter** —
    Quantpedia exploiting-term-structure-of-vix-futures (Simon & Campasano, grade A/B,
    self-reports OOS decay). PARTIAL overlap — same underlying data series as the closed
    Candidate 3 (VXN level/percentile), differentiated by using the curve SLOPE rather than
    level, the exact variant the closed test's own language named as clearing the bar. Real
    risk this fails the identical matched-control gate for the identical underlying reason.
    → SHORTLISTED with explicit overlap-risk flag (Candidate 9).
25. **Dealer zero-gamma flip level from published options open interest** — upgrades the
    already-shortlisted-but-NOT-WORTHY OpEx calendar-week candidate (#3 in the prior pass)
    by replacing the calendar-date PROXY with actual OI-derived positioning data (Stivers &
    Sun via Quantpedia option-expiration-week-effect, grade A). PARTIAL overlap (same
    underlying mechanism as the existing candidate) but closes its explicitly stated data
    gap. → SHORTLISTED (Candidate 10).
26. **Index-vs-constituent implied-volatility dispersion wedge (correlation risk premium)**
    — NDX/QQQ implied vol vs. mega-cap constituent implied vol (Quantpedia
    dispersion-trading, citing Buraschi/Trojani/Vedolin and Driessen/Maenhout/Vilkov, grade
    A). NONE overlap — no prior experiment used cross-sectional single-name options data.
    LOW frequency (monthly per source), flagged not rejected. → SHORTLISTED (Candidate 11).

## Rejected/parked this pass (compact, so not rediscovered)

27. Gold options vs. gold futures, Indian MCX (archive_r2 PDF, `sgng.14881`) — PhD research
    *protocol* only (no results), wrong market (MCX not COMEX/spot). REJECTED, no
    operational content.
28. "Essays in market microstructure — information content of quotes" (archive_r2 PDF,
    `sgng.9997`) — generic order-driven-market quote theory, PhD dissertation synopsis.
    REJECTED, HIGH overlap with the closed tick/quote-microstructure experiment (EXP007),
    no gold/index-specific mechanism.
29. Market sentiment + overnight anomaly (Quantpedia) — VIX leg is a LEVEL/MA condition
    (same construction as closed Candidate 3); one-third of the filter needs a proprietary
    paid sentiment indicator (Brain Market Sentiment). REJECTED, no new accessible info
    source once the paid leg is dropped.
30. "On options-driven realized volatility forecasting" (arXiv, rough-vol + deep-learning
    HAR-RV model) — pure forecasting-accuracy paper, no WHO/WHY actor mechanism. REJECTED
    as standalone (fails criterion 7's mechanism standard); kept as supporting evidence for
    #23 only.
31. "Clearing price distributions in call auctions" (arXiv 1904.07583) — real order-flow-
    imbalance auction model, matches the brief's auction-imbalance priority exactly, but
    real-time NASDAQ-100-constituent imbalance data (Nasdaq NOII) not confirmed freely
    accessible. PARKED (data infeasibility, not overlap) — re-check before reviving.
32. ~15 Quantpedia entries: time-series/asset-class/currency/commodity momentum and carry
    families — HIGH overlap with the already-closed duplicate-elimination list (TSMOM, FX
    carry, commodity term structure). Bulk REJECTED.
33. ~25 Quantpedia entries: single-stock equity factors (accrual anomaly, asset-growth
    effect, R&D-expenditure effect, net-payout-yield, short-interest effect, earnings-
    announcement premium, etc.) — wrong instrument class (Apex trades GOLD/US100, not
    single-name equities). Bulk REJECTED, out-of-scope-instrument.
34. Pairs-trading-with-stocks/country-ETFs, 13F alpha-cloning, soccer-club-stock arbitrage
    — out-of-scope instruments or unautomatable lag (13F is quarterly). Bulk REJECTED.
35. Calendar-seasonality Quantpedia entries (turn-of-month, January effect, pre-holiday
    effect, payday anomaly, Ramadan effect) — "another calendar bucket" on OHLC, exactly
    what the calendar-dominance finding already warns against. Bulk REJECTED per the
    brief's own anti-duplication rule.
36. Generic strategy-compendium books (`151-trading-strategies`, `51-trading-strategies`,
    Wilder *New Concepts in Technical Trading Systems*, Pring *On Market Momentum*,
    Stridsman *Trading Systems That Work*) — indicator/pattern-catalog families, HIGH
    overlap with the closed indicator-catalog and candlestick audits. Bulk REJECTED.

## Tally, second pass

- Concepts extracted: **15** (#22-36)
- Carried to shortlist: **5** (#22, #23, #24, #25, #26 → Candidates 7-11)
- Rejected/parked, individually reasoned: **5** (#27-31)
- Rejected, bulk (grouped by family): **5 groups, ~65 individual entries** (#32-36)
- Documents screened this pass: 728 titles/metadata indexed (108 archive_r2 + 516 arxiv +
  22 qp_papers + 82 quantpedia); abstract/conclusion read for ~14 keyword-hit survivors;
  full read for none (all resolved at abstract/conclusion depth). ~444 documents from the
  PRE-existing (pass-one) library remain covered only by the pass-one 66-source spot
  inspection, not re-read this pass.

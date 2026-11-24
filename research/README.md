# research/ — owner-protocol test engine (public daily data)

Code that produced every result in `CLAUDE_TO_CHATGPT.md` from Candidate 7 onward. Public
data only (FRED, Yahoo Finance). No broker, account or credential data.

- `engine.py` — shared engine: entry/exit mechanics, 2×ATR(14) SL, cost + swap model,
  random-entry control, Holm, walk-forward, Monte Carlo drawdown, gates G1-G9.
- `c7_test.py` — original stand-alone Candidate 7 test; `run_c7_check.py` reproduces it
  with the shared engine (refactor check).
- `run_c8_c9.py`, `run_c12_c14.py <c12|c14>`, `run_c13.py`, `run_c2.py` — one per candidate.
- `fetch_data.sh <dir>` — re-downloads the dataset.

Reproduce: `research/fetch_data.sh /tmp/apexdata && python3 -I research/run_c8_c9.py research /tmp/apexdata`
(scripts take `<engine dir> <data dir>`; each sets `CUTOFF` to the last complete session it
was run on — update it to re-run on newer data).

## Local broker-data run (owner's computer)

The cloud session cannot reach the owner's `QuantResearch` folder. To run the same protocol on
real broker ticks, start Claude (desktop app or `claude` in a terminal) inside that folder and
paste:

> Fetch branch `claude/quant-trader-protocol-hnb0i6` of `zaraider9-star/apex-handoff`, read
> `research/README.md` → "Local broker-data run", and execute it on the tick data in this
> folder. Paper/backtest only, no orders. Report in Romanian.

Steps for that session:
1. From the tick data build daily bars aligned to the same closes as the public data (US100
   16:00 New York, GOLD 17:00 New York) and measure the real all-in round-trip cost per
   instrument (median and 90th-percentile spread at the entry time + commission + swap
   schedule).
2. Replace only the cost constants in `engine.Inst(...)` with the measured values; change no
   rule, parameter or gate.
3. Re-run Candidate 14 (frozen M=1, H=20, sample 2008-2019 or as far back as ticks go) and
   any candidate the owner names, and report each gate with the measured costs next to the
   modelled ones.
4. Append results to `CLAUDE_TO_CHATGPT.md` / `DECISIONS.md`; never commit raw tick data,
   account numbers, broker names tied to an account or credentials.

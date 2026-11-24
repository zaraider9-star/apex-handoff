"""Candidate 2 — FOMC pre-announcement drift, daily construction, as pre-registered (commit fad081e)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23"); E.DFF_NAME = "DFF07"

FOMC = pd.to_datetime("""2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split())


def entries(inst, before):
    sig = np.zeros(len(inst.dates), dtype=int)
    for d in FOMC:
        if d > inst.dates[-1]: continue
        k = inst.dates.get_loc(d)  # statement day must be a trading day
        sig[k - before] = 1
    return sig


us100 = E.Inst("US100", "NDX07", "NDX07", 2.0, 0.025)
us500 = E.Inst("US500", "GSPC07", "GSPC07", 0.6, 0.025)
gold = E.Inst("GOLD", "GLD18", "GCF18", 0.50, 0.02)
LAST = us100.dates[-1]
t1 = E.outcome_table(us100, 1)
OOS = E.run(us100, entries(us100, 1), t1, E.OOS0, LAST)
IS = E.run(us100, entries(us100, 1), t1, E.IS0, E.IS1)
p, med = E.random_control(us100, OOS, t1, E.OOS0, LAST)
nb = E.run(us100, entries(us100, 2), E.outcome_table(us100, 2), E.OOS0, LAST)
x5 = E.run(us500, entries(us500, 1), E.outcome_table(us500, 1), E.OOS0, us500.dates[-1])
st = E.run(us100, entries(us100, 1), E.outcome_table(us100, 1, 2.0, 2.0), E.OOS0, LAST)
gd = E.run(gold, entries(gold, 1), E.outcome_table(gold, 1), E.OOS0, gold.dates[-1])
dd = E.mc_dd(OOS.R)
print("==================== CANDIDATE 2 — pre-FOMC drift, US100 (daily) ====================")
print(f"IS n={len(IS)} PF={E.pf(IS.R):.3f} | OOS n={len(OOS)} PF={E.pf(OOS.R):.3f} | random median PF {med:.3f}")
g = {
    "G1 OOS PF > 1.15": (E.pf(OOS.R), E.pf(OOS.R) > 1.15),
    "G2 OOS trades >= 30": (len(OOS), len(OOS) >= 30),
    "G3/G4 random-entry p < 0.05 (m=1)": (p, p < 0.05),
    "G5' 2-day variant PF > 1.0": (E.pf(nb.R), E.pf(nb.R) > 1.0),
    "G6 US500 OOS PF > 1.0": (E.pf(x5.R), E.pf(x5.R) > 1.0),
    "G7' IS PF > 1.0": (E.pf(IS.R), E.pf(IS.R) > 1.0),
    "G8 MC 95% maxDD <= 15%": (dd, dd <= 0.15),
    "G9 2x cost PF > 1.0": (E.pf(st.R), E.pf(st.R) > 1.0),
}
for k, (v, ok) in g.items():
    print(f"  {'PASS' if ok else 'FAIL'}  {k}: {round(v, 3) if isinstance(v, float) else v}")
print("VERDICT:", "PASS" if all(ok for _, ok in g.values()) else "REJECT", f"({sum(not ok for _, ok in g.values())} gates failed)")
print(f"  HAC t {E.hac_t(OOS.net):.2f} | WR {np.mean(OOS.R>0):.3f} | sumR {OOS.R.sum():.2f} | mean net ret {OOS.net.mean()*1e4:.1f} bp")
for y, t in OOS.groupby(OOS.date.dt.year):
    print(f"  {y}: n={len(t)} PF={E.pf(t.R):.3f}")
print(f"  GOLD diagnostic: n={len(gd)} PF={E.pf(gd.R):.3f}")

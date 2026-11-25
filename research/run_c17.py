"""Candidate 17 — even-week FOMC-cycle premium on US100, as pre-registered (commit 83bafd1).
Usage: python3 -I research/run_c17.py <research dir> <data dir>   (needs NDX07, GSPC07 .json and DFF10 .csv)"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-24"); E.DFF_NAME = "DFF10"
# Scheduled statement days: 2019 boundary meetings, the Candidate 2 list (federalreserve.gov), 2026-12-09 boundary.
F2 = pd.to_datetime("""2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split())
FOMC = sorted(set(pd.to_datetime(["2019-10-30", "2019-12-11"])) | set(F2) | {pd.Timestamp("2026-12-09")})
SHIFTS, HS = [-1, 0, 1], [4, 5, 6]


def entry_days(inst, s, weeks=(0, 2, 4, 6)):
    out = []
    for d, dn in zip(FOMC[:-1], FOMC[1:]):
        if d > inst.dates[-1]: break
        j = inst.dates.get_loc(d)
        jn = inst.dates.get_loc(dn) if dn <= inst.dates[-1] else len(inst.dates) + int(np.busday_count(inst.dates[-1].date(), dn.date()))
        for w in weeks:
            e = j + 5 * w - 2 + s
            if e < jn - 2 + s and e < len(inst.dates): out.append(e)
    return out


def dirser(s, inst, H, weeks=(0, 2, 4, 6)):
    v = np.zeros(len(inst.dates), dtype=int)
    for e in entry_days(inst, s, weeks):
        if e >= 1: v[e - 1] = 1  # value dated the session before e -> engine enters at the close of e
    return pd.Series(v, index=inst.dates)


if __name__ == "__main__":
    us100 = E.Inst("US100", "NDX07", "NDX07", 2.0, 0.025)
    us500 = E.Inst("US500", "GSPC07", "GSPC07", 0.6, 0.025)
    res, out = E.evaluate("CANDIDATE 17 — even-week FOMC-cycle premium, long US100", us100, dirser, SHIFTS, HS, us500, dirser,
                          pname="s", uses_H=True)
    s, H = out["sel"] if out else (0, 5)
    tab = E.outcome_table(us100, H); LAST = us100.dates[-1]
    print("NOT GATING (OOS):")
    for nm, wk in [("week 0 only", (0,)), ("weeks 2,4,6", (2, 4, 6)), ("odd weeks 1,3,5", (1, 3, 5))]:
        for lab, d0, d1 in [("IS", E.IS0, E.IS1), ("OOS", E.OOS0, LAST)]:
            t = E.run(us100, E.to_entries(us100, dirser(s, us100, H, wk)), tab, d0, d1)
            print(f"  {nm} {lab}: n={len(t)} PF={E.pf(t.R):.3f} sumR={t.R.sum():.2f}")

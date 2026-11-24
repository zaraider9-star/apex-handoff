"""Candidate 13 — overnight drift, as pre-registered (commit 0eaa339)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23"); E.DFF_NAME = "DFF07"


def segments(etf, idx_name, pts, markup, cost_mult=1.0, mk_mult=1.0):
    inst = E.Inst(etf, etf, idx_name, pts, markup)  # cost = pts / index level
    n = len(inst.c); rows = []
    for i in range(14, n - 1):
        p0 = inst.c[i]; dist = E.SL_ATR * inst.atr[i]
        t0, t1 = inst.dates[i], inst.dates[i + 1]
        nights = (t1 - t0).days
        rs = inst.dff_cum.loc[t1 - pd.Timedelta(days=1)] - inst.dff_cum.loc[t0 - pd.Timedelta(days=1)]
        swap = -(rs + markup * mk_mult * nights) / 360.0
        on = (inst.o[i + 1] - p0) / p0 - cost_mult * inst.cost[i] + swap  # open beyond SL exits at open anyway
        q0 = inst.o[i + 1]; dist2 = E.SL_ATR * inst.atr[i]; sl = q0 - dist2
        px = sl if inst.l[i + 1] <= sl else inst.c[i + 1]
        idr = (px - q0) / q0 - cost_mult * inst.cost[i]
        rows.append((t0, on / (dist / p0), idr / (dist2 / q0)))
    return pd.DataFrame(rows, columns=["date", "R_on", "R_id"]).set_index("date")


def window(df, a, b):
    return df[(df.index >= a) & (df.index <= b)]


def control_p(df):
    g = E.rng(); real = E.pf(df.R_on)
    pick = g.random((E.NSIM, len(df))) < 0.5
    R = np.where(pick, df.R_on.to_numpy()[None, :], df.R_id.to_numpy()[None, :])
    gp = np.where(R > 0, R, 0).sum(1); gl = np.where(R < 0, -R, 0).sum(1)
    sims = gp / gl
    return (1 + np.sum(sims >= real)) / (E.NSIM + 1), float(np.median(sims))


q = segments("QQQ07", "NDX07", 2.0, 0.025)
s = segments("SPY07", "GSPC07", 0.6, 0.025)
q2 = segments("QQQ07", "NDX07", 2.0, 0.025, 2.0, 2.0)
IS = window(q, E.IS0, E.IS1); OOS = window(q, E.OOS0, q.index[-1])
p, med = control_p(OOS)
yrs = {y: E.pf(t.R_on) for y, t in OOS.groupby(OOS.index.year)}
dd = E.mc_dd(OOS.R_on)
print("==================== CANDIDATE 13 — overnight drift, US100 (QQQ) ====================")
print(f"OOS {OOS.index[0].date()}..{OOS.index[-1].date()}  n={len(OOS)}  overnight PF {E.pf(OOS.R_on):.3f} | intraday PF {E.pf(OOS.R_id):.3f} | random-segment median PF {med:.3f}")
g = {
    "G1 OOS PF > 1.15": (E.pf(OOS.R_on), E.pf(OOS.R_on) > 1.15),
    "G2 trades >= 30": (len(OOS), len(OOS) >= 30),
    "G3/G4 random-segment p < 0.05 (m=1)": (p, p < 0.05),
    "G5' >= 3 of 4 OOS years PF > 1": ({k: round(v, 3) for k, v in yrs.items()}, sum(v > 1 for v in yrs.values()) >= 3),
    "G6 US500 (SPY) OOS PF > 1.0": (E.pf(window(s, E.OOS0, s.index[-1]).R_on), E.pf(window(s, E.OOS0, s.index[-1]).R_on) > 1.0),
    "G7' IS 2020-2022 PF > 1.0": (E.pf(IS.R_on), E.pf(IS.R_on) > 1.0),
    "G8 MC 95% maxDD <= 15%": (dd, dd <= 0.15),
    "G9 2x cost PF > 1.0": (E.pf(window(q2, E.OOS0, q2.index[-1]).R_on), E.pf(window(q2, E.OOS0, q2.index[-1]).R_on) > 1.0),
}
for k, (v, ok) in g.items():
    print(f"  {'PASS' if ok else 'FAIL'}  {k}: {round(v, 3) if isinstance(v, float) else v}")
print("VERDICT:", "PASS" if all(ok for _, ok in g.values()) else "REJECT", f"({sum(not ok for _, ok in g.values())} gates failed)")
print(f"  HAC t overnight R {E.hac_t(OOS.R_on):.2f} | mean R/night {OOS.R_on.mean():.4f} | sumR {OOS.R_on.sum():.2f} | intraday sumR {OOS.R_id.sum():.2f}")

"""Candidate 16 — implied-correlation (dispersion wedge) premium on US100, as pre-registered (commit 72298a1).
Usage: python3 -I research/run_c16.py <research dir> <data dir>
Data dir needs FRED VXNCLS10, VIXCLS10, VXVCLS10, VXAPLCLS10, VXGOGCLS10, VXAZNCLS10, VXGSCLS10, VXIBMCLS10,
DFF10 (.csv, from 2007) and Yahoo NDX07, GSPC07 (.json) — see research/README.md."""
import sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-24"); E.DFF_NAME = "DFF10"
K, HS = [0.5, 1.0, 1.5], [5, 10, 20]


def implied_corr(index, names):
    df = pd.concat([E.fred(index)] + [E.fred(n) for n in names], axis=1, join="inner").dropna()
    return (df.iloc[:, 0] / df.iloc[:, 1:].mean(axis=1)) ** 2


def zscore(s, n=252):
    return ((s - s.rolling(n).mean()) / s.rolling(n).std()).dropna()


z100 = zscore(implied_corr("VXNCLS10", ["VXAPLCLS10", "VXGOGCLS10", "VXAZNCLS10"]))
z500 = zscore(implied_corr("VIXCLS10", ["VXAPLCLS10", "VXGOGCLS10", "VXAZNCLS10", "VXGSCLS10", "VXIBMCLS10"]))

# G0 — duplicate gate on signals only, IS 2020-2022, before any return is computed
vxn = E.fred("VXNCLS10"); prank = vxn.rolling(252).apply(lambda x: (x <= x[-1]).mean(), raw=True).dropna()
vix, vxv = E.fred("VIXCLS10"), E.fred("VXVCLS10"); bw = (pd.concat([vix, vxv], axis=1, join="inner").dropna()
                                                     .pipe(lambda d: d.iloc[:, 0] / d.iloc[:, 1]) > 1.0)
isz = z100[(z100.index >= E.IS0) & (z100.index <= E.IS1)]
j = pd.concat([isz, prank], axis=1, join="inner").dropna()
rho = spearmanr(j.iloc[:, 0], j.iloc[:, 1]).correlation
on = isz[isz > 1.0].index; share = bw.reindex(on).fillna(False).mean() if len(on) else 0.0
print(f"z100 {z100.index[0].date()}..{z100.index[-1].date()} | z500 {z500.index[0].date()}..{z500.index[-1].date()}")
print(f"G0 Spearman(z, VXN 252d pct rank) IS = {rho:.3f} (limit 0.70) | backwardation share of k=1.0 IS signal days = "
      f"{share:.3f} of {len(on)} (limit 0.50) | share of IS days with z>0.5/1.0/1.5: "
      f"{(isz > .5).mean():.3f}/{(isz > 1).mean():.3f}/{(isz > 1.5).mean():.3f}")
if rho > 0.70 or share > 0.50:
    print("G0 FAIL — duplicate of Candidate 3/14 construction; closed without reading returns."); sys.exit(0)
print("G0 PASS")

us100 = E.Inst("US100", "NDX07", "NDX07", 2.0, 0.025)
us500 = E.Inst("US500", "GSPC07", "GSPC07", 0.6, 0.025)
sig = lambda z: (lambda k, inst: (z > k).astype(int))
E.evaluate("CANDIDATE 16 — implied-correlation premium, long US100", us100, sig(z100), K, HS, us500, sig(z500), pname="k")

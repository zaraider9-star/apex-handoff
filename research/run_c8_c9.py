"""Candidates 8 and 9, exactly as pre-registered (commit 8510ff4)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23")

gold = E.Inst("GOLD", "GLD18", "GCF18", 0.50, 0.02)
us100 = E.Inst("US100", "NDX", "NDX", 2.0, 0.025)
us500 = E.Inst("US500", "GSPC", "GSPC", 0.6, 0.025)
IMPLIED = {"GOLD": E.fred("GVZCLS"), "US100": E.fred("VXNCLS")}


def vrp_dir(N, inst):
    c = inst.close_series()
    rv = np.log(c).diff().rolling(N).std() * np.sqrt(252) * 100
    iv = IMPLIED[inst.name]
    j = pd.concat([iv, rv], axis=1, join="inner").dropna()
    vrp = j.iloc[:, 0] - j.iloc[:, 1]
    z = (vrp - vrp.rolling(252).mean()) / vrp.rolling(252).std()
    return np.sign(z).dropna()


vix, vix3m = E.fred("VIXCLS"), E.fred("VXVCLS")
ratio = pd.concat([vix, vix3m], axis=1, join="inner").dropna()
ratio = ratio.iloc[:, 0] / ratio.iloc[:, 1]


def ts_dir(M, inst):
    s = ratio.rolling(M).mean().dropna()
    return (s < 1.0).astype(int)


print(f"contango share of days 2020-2026: {(ratio['2020':] < 1).mean():.3f}")
E.evaluate("CANDIDATE 8 — GVZ volatility risk premium on GOLD", gold, vrp_dir, [10, 21, 63], [1, 5, 20], us100, vrp_dir, pname="N")
E.evaluate("CANDIDATE 9 — VIX/VIX3M contango long/flat on US100", us100, ts_dir, [1, 5, 10], [1, 5, 20], us500, ts_dir, pname="M")

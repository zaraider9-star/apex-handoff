"""Candidates 12 (month-end rebalancing) and 14 (backwardation buy-the-fear), as pre-registered (commit 0eaa339)."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23"); E.DFF_NAME = "DFF07"
which = sys.argv[3]

us100 = E.Inst("US100", "NDX07", "NDX07", 2.0, 0.025)
us500 = E.Inst("US500", "GSPC07", "GSPC07", 0.6, 0.025)

if which == "c12":
    def adj(name):
        j = json.load(open(f"{E.D}/{name}.json"))["chart"]["result"][0]
        idx = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York").normalize().tz_localize(None)
        s = pd.Series(j["indicators"]["adjclose"][0]["adjclose"], index=idx).dropna()
        return s[~s.index.duplicated(keep="last")]

    def mtd(s):
        per = s.index.to_period("M")
        prev = s.groupby(per).last().shift(1)
        return s / prev.reindex(per).to_numpy() - 1

    spx = E.yahoo("GSPC07")["close"]; ief = adj("IEF07")
    spread = pd.concat([mtd(spx), mtd(ief)], axis=1, join="inner").dropna()
    spread = spread.iloc[:, 0] - spread.iloc[:, 1]

    def me_dir(tau, inst, k):
        dates = inst.dates
        per = dates.to_period("M")
        last_idx = pd.Series(np.arange(len(dates)), index=dates).groupby(per).max()
        last_idx = last_idx.iloc[:-1]  # final incomplete month excluded
        out = pd.Series(0, index=dates, dtype=int)
        sp = spread.reindex(dates, method="ffill")
        for me in last_idx.to_numpy():
            e = me - k
            if e - 1 < 0: continue
            v = sp.iloc[e - 1]
            if np.isnan(v) or abs(v) <= tau: continue
            out.iloc[e - 1] = int(-np.sign(v))
        return out

    print(f"spread stats 2020-2026: mean {spread['2020':].mean():+.4f} sd {spread['2020':].std():.4f}")
    E.evaluate("CANDIDATE 12 — month-end rebalancing flow, US100", us100, me_dir, [0.0, 0.01, 0.02], [1, 3, 5], us500, me_dir, pname="tau", uses_H=True)

if which == "c14":
    vix, vxv = E.fred("VIXCLS07"), E.fred("VXVCLS07")
    r = pd.concat([vix, vxv], axis=1, join="inner").dropna(); ratio = r.iloc[:, 0] / r.iloc[:, 1]
    bw = lambda M, inst: (ratio.rolling(M).mean().dropna() > 1.0).astype(int)
    E.IS0, E.IS1 = pd.Timestamp("2008-01-01"), pd.Timestamp("2013-12-31")
    E.OOS0, E.OOS1 = pd.Timestamp("2014-01-01"), pd.Timestamp("2019-12-31")
    E.WF_YEARS = [2014, 2015, 2016, 2017, 2018, 2019]
    print(f"backwardation share of days: 2008-13 {(ratio['2008':'2013'] > 1).mean():.3f}  2014-19 {(ratio['2014':'2019'] > 1).mean():.3f}")
    res, out = E.evaluate("CANDIDATE 14 — backwardation buy-the-fear, US100 (2008-2019)", us100, bw, [1, 5, 10], [1, 5, 20], us500, bw, pname="M")
    if out:
        M, H = out["sel"]
        t = E.run(us100, E.to_entries(us100, bw(M, us100)), E.outcome_table(us100, H), pd.Timestamp("2020-01-01"), us100.dates[-1])
        print(f"  INFO ONLY (contaminated 2020-2026): n={len(t)} PF={E.pf(t['R']):.3f}")

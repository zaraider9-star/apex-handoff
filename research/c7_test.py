"""Candidate 7 — real-yield impulse on GOLD. Implements the pre-registration in
CLAUDE_TO_CHATGPT.md (commit 217ce3a) exactly. Run: python3 -I c7_test.py <data_dir>"""
import json, sys, math
import numpy as np, pandas as pd
import statsmodels.api as sm

D = sys.argv[1]
RNG = np.random.default_rng(20261124)
NSIM = 10_000
LS, HS = [1, 5, 20], [1, 5, 20]
IS0, IS1 = pd.Timestamp("2020-01-01"), pd.Timestamp("2022-12-31")
OOS0 = pd.Timestamp("2023-01-01")
SL_ATR, MARKUP = 2.0, 0.02


def yahoo(name):
    j = json.load(open(f"{D}/{name}.json"))["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    idx = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York").normalize().tz_localize(None)
    df = pd.DataFrame({k: q[k] for k in ["open", "high", "low", "close"]}, index=idx).dropna()
    return df[~df.index.duplicated(keep="last")].sort_index()


def fred(name):
    s = pd.read_csv(f"{D}/{name}.csv", index_col=0, parse_dates=True).iloc[:, 0]
    return pd.to_numeric(s, errors="coerce").dropna()


ry, dff = fred("DFII10"), fred("DFF")


class Inst:
    def __init__(self, etf, fut, usd_per_oz):
        p = yahoo(etf)
        lvl = yahoo(fut)["close"].reindex(p.index, method="ffill")
        self.dates = p.index
        self.o, self.h, self.l, self.c = (p[k].to_numpy() for k in ["open", "high", "low", "close"])
        self.cost = (usd_per_oz / lvl).to_numpy()  # round-trip cost as fraction of notional
        tr = np.maximum(self.h - self.l, np.maximum(abs(self.h - np.r_[np.nan, self.c[:-1]]), abs(self.l - np.r_[np.nan, self.c[:-1]])))
        tr[0] = self.h[0] - self.l[0]
        atr = np.full(len(tr), np.nan); atr[13] = tr[:14].mean()
        for i in range(14, len(tr)):
            atr[i] = (atr[i - 1] * 13 + tr[i]) / 14
        self.atr = atr
        dffc = dff.reindex(pd.date_range(dff.index[0], self.dates[-1] + pd.Timedelta(days=40))).ffill()
        self.dff_cum = pd.Series(np.cumsum(dffc.to_numpy() / 100.0), index=dffc.index)  # sum of daily rates


def signal(inst, L, same_day=False):
    """direction for an entry at the close of each gold day, using DFII10 obs strictly before that day."""
    dry = (ry - ry.shift(L)).dropna()
    pos = dry.index.searchsorted(inst.dates, side="right" if same_day else "left") - 1
    s = np.where(pos >= 0, -np.sign(dry.to_numpy()[np.clip(pos, 0, None)]), 0.0)
    return s.astype(int)


def outcome_table(inst, H, cost_mult=1.0, markup=MARKUP):
    """For every day i and direction d: (R, net_ret, exit_index). exit = -1 if not completable."""
    n = len(inst.c)
    R = np.full((2, n), np.nan); NET = np.full((2, n), np.nan); X = np.full((2, n), -1, dtype=int)
    for di, d in enumerate([1, -1]):
        for i in range(n):
            if np.isnan(inst.atr[i]) or i + H >= n:
                continue
            p0 = inst.c[i]; dist = SL_ATR * inst.atr[i]; sl = p0 - d * dist
            px, x = inst.c[i + H], i + H
            for k in range(i + 1, i + H + 1):
                if d == 1 and inst.o[k] <= sl: px, x = inst.o[k], k; break
                if d == -1 and inst.o[k] >= sl: px, x = inst.o[k], k; break
                if d == 1 and inst.l[k] <= sl: px, x = sl, k; break
                if d == -1 and inst.h[k] >= sl: px, x = sl, k; break
            gross = d * (px - p0) / p0
            t0, t1 = inst.dates[i], inst.dates[x]
            nights = (t1 - t0).days
            rate_sum = inst.dff_cum.loc[t1 - pd.Timedelta(days=1)] - inst.dff_cum.loc[t0 - pd.Timedelta(days=1)] if nights > 0 else 0.0
            swap = (-(rate_sum + markup * nights) if d == 1 else (rate_sum - markup * nights)) / 360.0
            net = gross - cost_mult * inst.cost[i] + swap
            NET[di, i] = net; R[di, i] = net / (dist / p0); X[di, i] = x
    return R, NET, X


def run(inst, sig, tab, d0, d1):
    """Non-overlapping trades with entry dates in [d0, d1] and exit inside [d0, d1]."""
    R, NET, X = tab
    i = int(inst.dates.searchsorted(d0)); end = int(inst.dates.searchsorted(d1, side="right")) - 1
    tr = []
    while i <= end:
        d = sig[i]
        if d != 0:
            di = 0 if d == 1 else 1
            x = X[di, i]
            if x < 0 or x > end:
                break
            tr.append((inst.dates[i], d, R[di, i], NET[di, i], x - i))
            i = x  # re-entry allowed at the exit-day close
            continue
        i += 1
    return pd.DataFrame(tr, columns=["date", "dir", "R", "net", "dur"])


def pf(x):
    x = np.asarray(x); g, l = x[x > 0].sum(), -x[x < 0].sum()
    return np.inf if l == 0 else g / l


def random_control(inst, trades, tab, d0, d1):
    R, _, X = tab
    i0 = int(inst.dates.searchsorted(d0)); end = int(inst.dates.searchsorted(d1, side="right")) - 1
    N = len(trades); dirs = trades["dir"].to_numpy()
    slack = max((end - i0) - int(trades["dur"].sum()), 0)
    gaps = np.floor(RNG.dirichlet(np.ones(N + 1), NSIM) * slack).astype(int)
    perm = np.argsort(RNG.random((NSIM, N)), axis=1); dmat = dirs[perm]
    cur = np.full(NSIM, i0); gp = np.zeros(NSIM); gl = np.zeros(NSIM); alive = np.ones(NSIM, bool)
    for k in range(N):
        cur = cur + gaps[:, k]
        di = np.where(dmat[:, k] == 1, 0, 1)
        ok = alive & (cur <= end)
        cc = np.clip(cur, 0, len(inst.c) - 1)
        x = X[di, cc]; r = R[di, cc]
        ok &= (x >= 0) & (x <= end)
        alive &= ok
        r = np.where(ok, r, 0.0)
        gp += np.where(r > 0, r, 0); gl += np.where(r < 0, -r, 0)
        cur = np.where(ok, x, cur)
    sims = np.where(gl > 0, gp / np.where(gl > 0, gl, 1), np.inf)
    real = pf(trades["R"])
    return (1 + np.sum(sims >= real)) / (NSIM + 1), np.median(sims)


def holm(pvals, alpha=0.05):
    order = np.argsort(pvals); m = len(pvals); rej = np.zeros(m, bool)
    for k, j in enumerate(order):
        if pvals[j] <= alpha / (m - k): rej[j] = True
        else: break
    return rej


def hac_t(x, H):
    x = np.asarray(x)
    if len(x) < 5: return np.nan
    lags = max(1, int(4 * (len(x) / 100) ** (2 / 9)))
    m = sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(m.tvalues[0])


def mc_dd(Rs, risk=0.01):
    Rs = np.asarray(Rs); b = RNG.choice(Rs, (NSIM, len(Rs)), replace=True)
    eq = np.cumprod(1 + risk * b, axis=1); eq = np.hstack([np.ones((NSIM, 1)), eq])
    dd = 1 - eq / np.maximum.accumulate(eq, axis=1)
    return np.percentile(dd.max(axis=1), 95)


gold = Inst("GLD", "GCF", 0.50)
silver = Inst("SLV", "SIF", 0.03)
LAST = gold.dates[-1]
print(f"data: gold {gold.dates[0].date()}..{LAST.date()}  DFII10 {ry.index[0].date()}..{ry.index[-1].date()}")

tabs = {H: outcome_table(gold, H) for H in HS}
sigs = {L: signal(gold, L) for L in LS}
rows = []
for L in LS:
    for H in HS:
        ist = run(gold, sigs[L], tabs[H], IS0, IS1)
        oos = run(gold, sigs[L], tabs[H], OOS0, LAST)
        p, med = random_control(gold, oos, tabs[H], OOS0, LAST)
        rows.append(dict(L=L, H=H, is_n=len(ist), is_pf=pf(ist["R"]), oos_n=len(oos), oos_pf=pf(oos["R"]),
                         oos_pf_ret=pf(oos["net"]), p_rand=p, rand_med_pf=med, oos_sumR=oos["R"].sum(), hac_t=hac_t(oos["net"], H)))
res = pd.DataFrame(rows)
res["holm_sig"] = holm(res["p_rand"].to_numpy())
pd.set_option("display.width", 200)
print("\nALL 9 CONFIGS (PF in R, net of costs):\n", res.round(3).to_string(index=False))

elig = res[res.is_n >= 30]
sel = elig.loc[elig.is_pf.idxmax()]
L, H = int(sel.L), int(sel.H)
print(f"\nIS-selected config: L={L} H={H}  (IS PF {sel.is_pf:.3f}, n={int(sel.is_n)})")
oos = run(gold, sigs[L], tabs[H], OOS0, LAST)

# neighbours
li, hi = LS.index(L), HS.index(H)
nb = [(LS[a], HS[b]) for a, b in [(li - 1, hi), (li + 1, hi), (li, hi - 1), (li, hi + 1)] if 0 <= a < 3 and 0 <= b < 3]
nb_pf = [float(res[(res.L == a) & (res.H == b)].oos_pf.iloc[0]) for a, b in nb]
# cross symbol
stab = outcome_table(silver, H); ssig = signal(silver, L)
s_oos = run(silver, ssig, stab, OOS0, silver.dates[-1])
# walk-forward
wf = []
for Y in [2023, 2024, 2025, 2026]:
    best, bpf = None, -1
    for l2 in LS:
        for h2 in HS:
            t = run(gold, sigs[l2], tabs[h2], IS0, pd.Timestamp(f"{Y-1}-12-31"))
            if len(t) >= 30 and pf(t["R"]) > bpf: best, bpf = (l2, h2), pf(t["R"])
    t = run(gold, sigs[best[0]], tabs[best[1]], pd.Timestamp(f"{Y}-01-01"), min(pd.Timestamp(f"{Y}-12-31"), LAST))
    wf.append(t); print(f"  WF {Y}: selected L={best[0]} H={best[1]} -> n={len(t)} PF={pf(t['R']):.3f}")
wf = pd.concat(wf)
# cost stress
st = run(gold, sigs[L], outcome_table(gold, H, cost_mult=2.0, markup=2 * MARKUP), OOS0, LAST)
dd95 = mc_dd(oos["R"])

g = {
    "G1 OOS PF > 1.15": (pf(oos["R"]), pf(oos["R"]) > 1.15),
    "G2 OOS trades >= 30": (len(oos), len(oos) >= 30),
    "G3 random-entry p < 0.05": (float(sel.p_rand), sel.p_rand < 0.05),
    "G4 Holm-significant (m=9)": (bool(sel.holm_sig), bool(sel.holm_sig)),
    "G5 neighbours PF>1 >= 2/3": (dict(zip(map(str, nb), np.round(nb_pf, 3))), np.mean(np.array(nb_pf) > 1.0) >= 2 / 3),
    "G6 XAGUSD OOS PF > 1.0": (pf(s_oos["R"]), pf(s_oos["R"]) > 1.0),
    "G7 walk-forward PF > 1.10": (pf(wf["R"]), pf(wf["R"]) > 1.10),
    "G8 MC 95% maxDD <= 15%": (dd95, dd95 <= 0.15),
    "G9 2x cost PF > 1.0": (pf(st["R"]), pf(st["R"]) > 1.0),
}
print("\nGATES (selected config):")
for k, (v, ok) in g.items():
    print(f"  {'PASS' if ok else 'FAIL'}  {k}: {v if not isinstance(v, float) else round(v, 3)}")
print("VERDICT:", "PASS" if all(ok for _, ok in g.values()) else "REJECT")

print("\nDIAGNOSTICS (selected config, OOS):")
print(f"  HAC t (net ret) {hac_t(oos['net'], H):.2f} | sum R {oos['R'].sum():.2f} | WR {np.mean(oos['R']>0):.3f} | avgWin {oos.R[oos.R>0].mean():.3f}R avgLoss {oos.R[oos.R<0].mean():.3f}R")
for d, nm in [(1, "long"), (-1, "short")]:
    t = oos[oos.dir == d]; print(f"  {nm}: n={len(t)} PF={pf(t['R']):.3f}")
for y, t in oos.groupby(oos.date.dt.year):
    print(f"  {y}: n={len(t)} PF={pf(t['R']):.3f} sumR={t.R.sum():.2f}")
sd = run(gold, signal(gold, L, same_day=True), tabs[H], OOS0, LAST)
print(f"  same-day-timing variant (not PASS-eligible): n={len(sd)} PF={pf(sd['R']):.3f}")
ist = run(gold, sigs[L], tabs[H], IS0, IS1)
print(f"  IS: n={len(ist)} PF={pf(ist['R']):.3f} | drift check: gold buy&hold OOS {gold.c[-1]/gold.c[gold.dates.searchsorted(OOS0)]-1:+.1%}")

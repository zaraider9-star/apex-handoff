"""Shared test engine implementing the owner-protocol pre-registration (gates G1-G9).
Identical mechanics to c7_test.py; signals are passed in as dated direction series."""
import json
import numpy as np, pandas as pd
import statsmodels.api as sm

NSIM = 10_000
IS0, IS1 = pd.Timestamp("2020-01-01"), pd.Timestamp("2022-12-31")
OOS0 = pd.Timestamp("2023-01-01")
OOS1 = None
WF_YEARS = [2023, 2024, 2025, 2026]
DFF_NAME = "DFF"
CUTOFF = None  # last complete session to include (drops an in-progress bar)
SL_ATR = 2.0
D = None  # data dir, set by caller


def rng():
    return np.random.default_rng(20261124)


def yahoo(name):
    j = json.load(open(f"{D}/{name}.json"))["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    idx = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York").normalize().tz_localize(None)
    df = pd.DataFrame({k: q[k] for k in ["open", "high", "low", "close"]}, index=idx).dropna()
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df if CUTOFF is None else df[df.index <= CUTOFF]


def fred(name):
    s = pd.read_csv(f"{D}/{name}.csv", index_col=0, parse_dates=True).iloc[:, 0]
    return pd.to_numeric(s, errors="coerce").dropna()


class Inst:
    def __init__(self, name, price, level, cost_units, markup):
        p = yahoo(price)
        lvl = yahoo(level)["close"].reindex(p.index, method="ffill")
        self.name, self.markup = name, markup
        self.dates = p.index
        self.o, self.h, self.l, self.c = (p[k].to_numpy() for k in ["open", "high", "low", "close"])
        self.cost = (cost_units / lvl).to_numpy()
        pc = np.r_[np.nan, self.c[:-1]]
        tr = np.maximum(self.h - self.l, np.maximum(abs(self.h - pc), abs(self.l - pc))); tr[0] = self.h[0] - self.l[0]
        atr = np.full(len(tr), np.nan); atr[13] = tr[:14].mean()
        for i in range(14, len(tr)):
            atr[i] = (atr[i - 1] * 13 + tr[i]) / 14
        self.atr = atr
        dff = fred(DFF_NAME)
        dffc = dff.reindex(pd.date_range(dff.index[0], self.dates[-1] + pd.Timedelta(days=40))).ffill()
        self.dff_cum = pd.Series(np.cumsum(dffc.to_numpy() / 100.0), index=dffc.index)
        self._tabs = {}

    def close_series(self):
        return pd.Series(self.c, index=self.dates)


def to_entries(inst, dirser, same_day=False):
    """Map a dated direction series onto entry days: use the last value dated strictly before the entry day."""
    dirser = dirser.dropna()
    pos = dirser.index.searchsorted(inst.dates, side="right" if same_day else "left") - 1
    v = dirser.to_numpy()
    return np.where(pos >= 0, v[np.clip(pos, 0, None)], 0).astype(int)


def outcome_table(inst, H, cost_mult=1.0, markup_mult=1.0):
    key = (H, cost_mult, markup_mult)
    if key in inst._tabs:
        return inst._tabs[key]
    n = len(inst.c); mk = inst.markup * markup_mult
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
            rs = inst.dff_cum.loc[t1 - pd.Timedelta(days=1)] - inst.dff_cum.loc[t0 - pd.Timedelta(days=1)] if nights > 0 else 0.0
            swap = (-(rs + mk * nights) if d == 1 else (rs - mk * nights)) / 360.0
            net = gross - cost_mult * inst.cost[i] + swap
            NET[di, i] = net; R[di, i] = net / (dist / p0); X[di, i] = x
    inst._tabs[key] = (R, NET, X)
    return inst._tabs[key]


def run(inst, sig, tab, d0, d1):
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
            i = x
            continue
        i += 1
    return pd.DataFrame(tr, columns=["date", "dir", "R", "net", "dur"])


def pf(x):
    x = np.asarray(x)
    if len(x) == 0: return np.nan
    g, l = x[x > 0].sum(), -x[x < 0].sum()
    return np.inf if l == 0 else g / l


def random_control(inst, trades, tab, d0, d1, R_=None):
    g = rng()
    R, _, X = tab
    i0 = int(inst.dates.searchsorted(d0)); end = int(inst.dates.searchsorted(d1, side="right")) - 1
    N = len(trades)
    if N == 0: return 1.0, np.nan
    dirs = trades["dir"].to_numpy()
    slack = max((end - i0) - int(trades["dur"].sum()), 0)
    gaps = np.floor(g.dirichlet(np.ones(N + 1), NSIM) * slack).astype(int)
    dmat = dirs[np.argsort(g.random((NSIM, N)), axis=1)]
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
    return (1 + np.sum(sims >= pf(trades["R"]))) / (NSIM + 1), float(np.median(sims))


def holm(p, alpha=0.05):
    order = np.argsort(p); m = len(p); rej = np.zeros(m, bool)
    for k, j in enumerate(order):
        if p[j] <= alpha / (m - k): rej[j] = True
        else: break
    return rej


def hac_t(x):
    x = np.asarray(x)
    if len(x) < 5: return np.nan
    lags = max(1, int(4 * (len(x) / 100) ** (2 / 9)))
    return float(sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags}).tvalues[0])


def mc_dd(Rs, risk=0.01):
    Rs = np.asarray(Rs); b = rng().choice(Rs, (NSIM, len(Rs)), replace=True)
    eq = np.hstack([np.ones((NSIM, 1)), np.cumprod(1 + risk * b, axis=1)])
    return float(np.percentile((1 - eq / np.maximum.accumulate(eq, axis=1)).max(axis=1), 95))


def evaluate(title, inst, dir_fn, P, HS, cross_inst, cross_dir_fn, pname="P", uses_H=False):
    """dir_fn(p, inst) -> dated direction series. Runs IS selection, all 9 OOS configs and gates G1-G9."""
    print(f"\n==================== {title} ====================")
    LAST = inst.dates[-1] if OOS1 is None else min(inst.dates[-1], OOS1)
    CLAST = cross_inst.dates[-1] if OOS1 is None else min(cross_inst.dates[-1], OOS1)
    print(f"data: {inst.name} {inst.dates[0].date()}..{inst.dates[-1].date()} | IS {IS0.date()}..{IS1.date()} OOS {OOS0.date()}..{LAST.date()}")
    call = (lambda f, p, ins, H: f(p, ins, H)) if uses_H else (lambda f, p, ins, H: f(p, ins))
    _c = {}
    class _S(dict):
        def __getitem__(self, k):  # k = (p, H)
            if k not in _c: _c[k] = to_entries(inst, call(dir_fn, k[0], inst, k[1]))
            return _c[k]
    sigs = _S()
    rows = []
    for p in P:
        for H in HS:
            tab = outcome_table(inst, H)
            ist = run(inst, sigs[(p, H)], tab, IS0, IS1); oos = run(inst, sigs[(p, H)], tab, OOS0, LAST)
            pr, med = random_control(inst, oos, tab, OOS0, LAST)
            rows.append(dict(**{pname: p}, H=H, is_n=len(ist), is_pf=pf(ist["R"]), oos_n=len(oos), oos_pf=pf(oos["R"]),
                             p_rand=pr, rand_med_pf=med, oos_sumR=oos["R"].sum(), hac_t=hac_t(oos["net"])))
    res = pd.DataFrame(rows); res["holm_sig"] = holm(res["p_rand"].to_numpy())
    pd.set_option("display.width", 200)
    print(res.round(3).to_string(index=False))
    elig = res[res.is_n >= 30]
    if elig.empty:
        print("VERDICT: REJECT (no config with >=30 IS trades)"); return res, None
    sel = elig.loc[elig.is_pf.idxmax()]; p, H = sel[pname], int(sel.H)
    p = type(P[0])(p)
    print(f"IS-selected: {pname}={p} H={H} (IS PF {sel.is_pf:.3f}, n={int(sel.is_n)})")
    tab = outcome_table(inst, H); oos = run(inst, sigs[(p, H)], tab, OOS0, LAST)
    pi, hi = P.index(p), HS.index(H)
    nb = [(P[a], HS[b]) for a, b in [(pi - 1, hi), (pi + 1, hi), (pi, hi - 1), (pi, hi + 1)] if 0 <= a < len(P) and 0 <= b < len(HS)]
    nb_pf = [float(res[(res[pname] == a) & (res.H == b)].oos_pf.iloc[0]) for a, b in nb]
    c_oos = run(cross_inst, to_entries(cross_inst, call(cross_dir_fn, p, cross_inst, H)), outcome_table(cross_inst, H), OOS0, CLAST)
    wf = []
    for Y in WF_YEARS:
        best, bpf = None, -1
        for p2 in P:
            for h2 in HS:
                t = run(inst, sigs[(p2, h2)], outcome_table(inst, h2), IS0, pd.Timestamp(f"{Y-1}-12-31"))
                if len(t) >= 30 and pf(t["R"]) > bpf: best, bpf = (p2, h2), pf(t["R"])
        if best is None: continue
        t = run(inst, sigs[best], outcome_table(inst, best[1]), pd.Timestamp(f"{Y}-01-01"), min(pd.Timestamp(f"{Y}-12-31"), LAST))
        wf.append(t); print(f"  WF {Y}: {pname}={best[0]} H={best[1]} -> n={len(t)} PF={pf(t['R']):.3f}")
    wf = pd.concat(wf) if wf else pd.DataFrame(columns=["R"])
    st = run(inst, sigs[(p, H)], outcome_table(inst, H, 2.0, 2.0), OOS0, LAST)
    dd95 = mc_dd(oos["R"]) if len(oos) else 1.0
    g = {
        "G1 OOS PF > 1.15": (pf(oos["R"]), pf(oos["R"]) > 1.15),
        "G2 OOS trades >= 30": (len(oos), len(oos) >= 30),
        "G3 random-entry p < 0.05": (float(sel.p_rand), sel.p_rand < 0.05),
        "G4 Holm-significant (m=9)": (bool(sel.holm_sig), bool(sel.holm_sig)),
        "G5 neighbours PF>1 >= 2/3": (dict(zip(map(str, nb), np.round(nb_pf, 3))), np.mean(np.array(nb_pf) > 1.0) >= 2 / 3),
        f"G6 {cross_inst.name} OOS PF > 1.0": ((len(c_oos), pf(c_oos["R"])), pf(c_oos["R"]) > 1.0),
        "G7 walk-forward PF > 1.10": (pf(wf["R"]), pf(wf["R"]) > 1.10),
        "G8 MC 95% maxDD <= 15%": (dd95, dd95 <= 0.15),
        "G9 2x cost PF > 1.0": (pf(st["R"]), pf(st["R"]) > 1.0),
    }
    print("GATES:")
    for k, (v, ok) in g.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}: {round(v, 3) if isinstance(v, float) else v}")
    verdict = "PASS" if all(ok for _, ok in g.values()) else "REJECT"
    print("VERDICT:", verdict, f"({sum(not ok for _, ok in g.values())} gates failed)")
    print("DIAGNOSTICS (OOS, selected):")
    if len(oos):
        print(f"  HAC t {hac_t(oos['net']):.2f} | sumR {oos.R.sum():.2f} | WR {np.mean(oos.R>0):.3f} | avgWin {oos.R[oos.R>0].mean():.3f}R avgLoss {oos.R[oos.R<0].mean():.3f}R")
        for d, nm in [(1, "long"), (-1, "short")]:
            t = oos[oos.dir == d]
            if len(t): print(f"  {nm}: n={len(t)} PF={pf(t['R']):.3f}")
        for y, t in oos.groupby(oos.date.dt.year):
            print(f"  {y}: n={len(t)} PF={pf(t['R']):.3f} sumR={t.R.sum():.2f}")
    sd = run(inst, to_entries(inst, call(dir_fn, p, inst, H), same_day=True), tab, OOS0, LAST)
    print(f"  same-day timing (not PASS-eligible): n={len(sd)} PF={pf(sd['R']):.3f}")
    i0 = inst.dates.searchsorted(OOS0); i1 = inst.dates.searchsorted(LAST, side="right") - 1
    print(f"  buy&hold OOS {inst.c[i1]/inst.c[i0]-1:+.1%}")
    return res, dict(sel=(p, H), gates=g, verdict=verdict, oos=oos)

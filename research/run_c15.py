"""Candidate 15 — end-of-day hedging-demand momentum, as pre-registered (commit 55874e1).
Usage: python3 -I research/run_c15.py <research dir> <daily data dir> <duka root> [div_US100 div_US500]"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E, duka
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23")
ROOT = sys.argv[3]
DIV = {"US100": float(sys.argv[4]) if len(sys.argv) > 4 else 1000.0, "US500": float(sys.argv[5]) if len(sys.argv) > 5 else 1000.0}
TAUS, TS = [0.0, 0.0025, 0.005], ["15:00", "15:30"]
SPECS = {"US100": ("USATECHIDXUSD", "NDX07", 0.5), "US500": ("USA500IDXUSD", "GSPC07", 0.15)}
IS0, IS1, OOS0 = pd.Timestamp("2020-01-01"), pd.Timestamp("2022-12-31"), pd.Timestamp("2023-01-01")


def early_close(d):
    if d.month == 11 and d.weekday() == 4 and 23 <= d.day <= 29:  # Friday after the 4th Thursday
        return True
    return (d.month, d.day) in [(12, 24), (7, 3)] and d.weekday() <= 3


def daily_atr(px):
    h, l, c = px.high.to_numpy(), px.low.to_numpy(), px.close.to_numpy()
    pc = np.r_[np.nan, c[:-1]]
    tr = np.maximum(h - l, np.maximum(abs(h - pc), abs(l - pc))); tr[0] = h[0] - l[0]
    atr = np.full(len(tr), np.nan); atr[13] = tr[:14].mean()
    for i in range(14, len(tr)):
        atr[i] = (atr[i - 1] * 13 + tr[i]) / 14
    return pd.Series(atr, index=px.index)


def simulate(b, a, e, xk, dirn, dist, slip, mult):
    """Fill at minute e close (ask for long / bid for short), exit at minute xk close or SL; returns R."""
    hs_e = (a.c[e] - b.c[e]) / 2; hs_x = (a.c[xk] - b.c[xk]) / 2
    if dirn == 1:
        ent = a.c[e] + (mult - 1) * hs_e + mult * slip; sl = ent - dist; ex = None
        for m in range(e + 1, xk + 1):
            if b.o[m] <= sl: ex = b.o[m] - (mult - 1) * hs_e - mult * slip; break
            if b.l[m] <= sl: ex = sl - (mult - 1) * hs_e - mult * slip; break
        if ex is None: ex = b.c[xk] - (mult - 1) * hs_x - mult * slip
    else:
        ent = b.c[e] - (mult - 1) * hs_e - mult * slip; sl = ent + dist; ex = None
        for m in range(e + 1, xk + 1):
            if a.o[m] >= sl: ex = a.o[m] + (mult - 1) * hs_e + mult * slip; break
            if a.h[m] >= sl: ex = sl + (mult - 1) * hs_e + mult * slip; break
        if ex is None: ex = a.c[xk] + (mult - 1) * hs_x + mult * slip
    return dirn * (ex - ent) / ent / (dist / ent)


def build(name):
    sym, yname, slip = SPECS[name]
    px = E.yahoo(yname); atr = daily_atr(px)
    sess = [d for d in px.index if d >= pd.Timestamp("2019-12-02")]
    rows, prev, calib = [], None, []
    for j, d in enumerate(sess):
        day = duka.load_day(ROOT, sym, d, DIV[name])
        if day is None:
            prev = None; continue
        ix = day["BID"].index.intersection(day["ASK"].index)
        b = {k: day["BID"].loc[ix, k].to_numpy() for k in "ohlc"}; a = {k: day["ASK"].loc[ix, k].to_numpy() for k in "ohlc"}
        b, a = type("S", (), b), type("S", (), a)
        hm = np.array(ix.strftime("%H:%M")); dt_ny = np.array(ix.date)
        sel = np.where((hm == "15:59") & (dt_ny == d.date()))[0]
        cur = dict(b=b, a=a, k=sel[0] if len(sel) else None)
        if cur["k"] is not None:
            calib.append((d, (b.c[cur["k"]] + a.c[cur["k"]]) / 2, px.close.loc[d]))
        if prev is not None and prev["k"] is not None and cur["k"] is not None and not early_close(d):
            p_prev = (prev["b"].c[prev["k"]] + prev["a"].c[prev["k"]]) / 2
            dist = 0.5 * atr.iloc[px.index.get_loc(d) - 1]
            for T in TS:
                tm1 = (pd.Timestamp(f"2000-01-01 {T}") - pd.Timedelta(minutes=1)).strftime("%H:%M")
                e = np.where((hm == tm1) & (dt_ny == d.date()))[0]
                xk = cur["k"]
                if not len(e) or xk <= e[0]: continue
                e = e[0]; mid = (b.c[e] + a.c[e]) / 2
                rows.append(dict(date=d, T=T, r=mid / p_prev - 1, spread=a.c[e] - b.c[e],
                                 RL=simulate(b, a, e, xk, 1, dist, slip, 1), RS=simulate(b, a, e, xk, -1, dist, slip, 1),
                                 RL2=simulate(b, a, e, xk, 1, dist, slip, 2), RS2=simulate(b, a, e, xk, -1, dist, slip, 2)))
        prev = cur
    cal = pd.DataFrame(calib, columns=["date", "duka_mid_1559", "yahoo_close"]).set_index("date")
    return pd.DataFrame(rows), cal


def trades(df, tau, T, d0, d1, stress=False):
    x = df[(df["T"] == T) & (df.date >= d0) & (df.date <= d1) & (df.r.abs() > tau)].copy()
    x["dir"] = np.sign(x.r).astype(int)
    x["R"] = np.where(x.dir == 1, x.RL2 if stress else x.RL, x.RS2 if stress else x.RS)
    return x


def control(df, t, T, d0, d1):
    pool = df[(df["T"] == T) & (df.date >= d0) & (df.date <= d1)]
    RL, RS = pool.RL.to_numpy(), pool.RS.to_numpy(); n = len(t); nl = int((t.dir == 1).sum())
    g = E.rng(); real = E.pf(t.R); hits = 0; meds = []
    for _ in range(E.NSIM):
        pick = g.choice(len(pool), n, replace=False); dirs = np.r_[np.ones(nl), -np.ones(n - nl)]; g.shuffle(dirs)
        R = np.where(dirs == 1, RL[pick], RS[pick]); gp, gl = R[R > 0].sum(), -R[R < 0].sum()
        s = gp / gl if gl > 0 else np.inf; hits += s >= real; meds.append(s)
    return (1 + hits) / (E.NSIM + 1), float(np.median(meds))


if __name__ == "__main__":
    data = {k: build(k) for k in SPECS}
    for k, (df, cal) in data.items():
        rel = (cal.duka_mid_1559 / cal.yahoo_close - 1)
        print(f"{k}: sessions with signal rows {df.date.nunique()} | Duka 15:59 mid vs Yahoo close: median {rel.median():+.4%}, "
              f"p95 abs {rel.abs().quantile(.95):.4%} | median spread {df.spread.median():.2f} pts")
    us100, us500 = data["US100"][0], data["US500"][0]
    LAST = us100.date.max()
    rows = []
    for tau in TAUS:
        for T in TS:
            it = trades(us100, tau, T, IS0, IS1); ot = trades(us100, tau, T, OOS0, LAST)
            p, med = control(us100, ot, T, OOS0, LAST)
            rows.append(dict(tau=tau, T=T, is_n=len(it), is_pf=E.pf(it.R), oos_n=len(ot), oos_pf=E.pf(ot.R), p_rand=p, rand_med=med, hac_t=E.hac_t(ot.R)))
    res = pd.DataFrame(rows); res["holm"] = E.holm(res.p_rand.to_numpy())
    print("\n==================== CANDIDATE 15 — end-of-day hedging momentum, US100 ====================")
    print(f"IS {IS0.date()}..{IS1.date()} OOS {OOS0.date()}..{LAST.date()}")
    print(res.round(3).to_string(index=False))
    el = res[res.is_n >= 30]; s = el.loc[el.is_pf.idxmax()]; tau, T = float(s.tau), s["T"]
    print(f"IS-selected: tau={tau} T={T} (IS PF {s.is_pf:.3f}, n={int(s.is_n)})")
    ot = trades(us100, tau, T, OOS0, LAST)
    ti = TAUS.index(tau); nb = [(TAUS[ti + k], T) for k in (-1, 1) if 0 <= ti + k < 3] + [(tau, [x for x in TS if x != T][0])]
    nb_pf = [float(res[(res.tau == a) & (res["T"] == bT)].oos_pf.iloc[0]) for a, bT in nb]
    x5 = trades(us500, tau, T, OOS0, us500.date.max())
    wf = []
    for Y in [2023, 2024, 2025, 2026]:
        best, bpf = None, -1
        for t2 in TAUS:
            for T2 in TS:
                t = trades(us100, t2, T2, IS0, pd.Timestamp(f"{Y-1}-12-31"))
                if len(t) >= 30 and E.pf(t.R) > bpf: best, bpf = (t2, T2), E.pf(t.R)
        t = trades(us100, best[0], best[1], pd.Timestamp(f"{Y}-01-01"), min(pd.Timestamp(f"{Y}-12-31"), LAST)); wf.append(t)
        print(f"  WF {Y}: tau={best[0]} T={best[1]} -> n={len(t)} PF={E.pf(t.R):.3f}")
    wf = pd.concat(wf); st = trades(us100, tau, T, OOS0, LAST, stress=True); dd = E.mc_dd(ot.R)
    g = {"G1 OOS PF > 1.15": (E.pf(ot.R), E.pf(ot.R) > 1.15), "G2 OOS trades >= 30": (len(ot), len(ot) >= 30),
         "G3 random-entry p < 0.05": (float(s.p_rand), s.p_rand < 0.05), "G4 Holm (m=6)": (bool(s.holm), bool(s.holm)),
         "G5 neighbours PF>1 >= 2/3": (dict(zip(map(str, nb), np.round(nb_pf, 3))), np.mean(np.array(nb_pf) > 1) >= 2 / 3),
         "G6 US500 OOS PF > 1.0": ((len(x5), E.pf(x5.R)), E.pf(x5.R) > 1.0), "G7 walk-forward PF > 1.10": (E.pf(wf.R), E.pf(wf.R) > 1.10),
         "G8 MC 95% DD <= 15%": (dd, dd <= 0.15), "G9 2x cost PF > 1.0": (E.pf(st.R), E.pf(st.R) > 1.0)}
    print("GATES:")
    for k, (v, ok) in g.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}: {round(v, 3) if isinstance(v, float) else v}")
    print("VERDICT:", "PASS" if all(ok for _, ok in g.values()) else "REJECT", f"({sum(not ok for _, ok in g.values())} gates failed)")
    print(f"  WR {np.mean(ot.R > 0):.3f} | avgWin {ot.R[ot.R > 0].mean():.3f}R avgLoss {ot.R[ot.R < 0].mean():.3f}R | sumR {ot.R.sum():.2f}")
    for d, nm in [(1, "long"), (-1, "short")]:
        t = ot[ot.dir == d]; print(f"  {nm}: n={len(t)} PF={E.pf(t.R):.3f}")
    for y, t in ot.groupby(ot.date.dt.year):
        print(f"  {y}: n={len(t)} PF={E.pf(t.R):.3f} sumR={t.R.sum():.2f}")

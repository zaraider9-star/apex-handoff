"""Paper (shadow) ledger for Candidate 14 — frozen rule M=1, H=20. PAPER ONLY: never places orders.

Rule (frozen, see CLAUDE_TO_CHATGPT.md, Candidate 14 shadow pre-registration):
  long US100 at the close of a session when the latest VIX/VIX3M daily close ratio dated strictly
  before that session is > 1.0; SL = entry - 2 x ATR(14, Wilder); exit at SL (gap -> open) or at the
  close 20 sessions after entry; one position at a time; re-entry allowed at the exit-session close.
The whole ledger is rebuilt from START on every run (stateless, reproducible).
Usage: python3 -I shadow/run_shadow.py --repo <repo root>
"""
import argparse, io, json, subprocess, time, datetime as dt
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd

START = pd.Timestamp("2026-11-24")
H, SL_ATR, PTS_RT, MARKUP, RISK = 20, 2.0, 2.0, 0.025, 0.01
NY = ZoneInfo("America/New_York")


def fetch(url, ua=False):
    last = None
    for k in range(4):
        r = subprocess.run(["curl", "-s", "-m", "40"] + (["-A", "Mozilla/5.0"] if ua else []) + ["-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        if r.returncode == 0 and code == b"200" and body:
            return body
        last = f"curl rc={r.returncode} http={code.decode(errors='ignore')}"
        time.sleep(2 ** k)
    raise RuntimeError(f"download failed ({last}): {url}")


def yahoo(sym):
    q = "%5E" + sym.lstrip("^") if sym.startswith("^") else sym
    j = json.loads(fetch(f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?period1=1167609600&period2={int(time.time())}&interval=1d", ua=True))
    j = j["chart"]["result"][0]; qt = j["indicators"]["quote"][0]
    idx = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert(NY).normalize().tz_localize(None)
    df = pd.DataFrame({k: qt[k] for k in ["open", "high", "low", "close"]}, index=idx).dropna()
    return df[~df.index.duplicated(keep="last")].sort_index()


def fred(sid):
    s = pd.read_csv(io.BytesIO(fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=2007-01-01")), index_col=0, parse_dates=True).iloc[:, 0]
    return pd.to_numeric(s, errors="coerce").dropna()


def main():
    global START
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", default=".")
    ap.add_argument("--verify-start"); ap.add_argument("--verify-end")  # replay check only, never for the live ledger
    a = ap.parse_args()
    if a.verify_start: START = pd.Timestamp(a.verify_start)
    now = dt.datetime.now(NY); today = pd.Timestamp(now.date())
    px = yahoo("^NDX")
    if px.index[-1] == today and (now.hour, now.minute) < (16, 20):
        px = px.iloc[:-1]  # in-progress session, not final
    if a.verify_end: px = px[px.index <= pd.Timestamp(a.verify_end)]
    vix, vxv, dff = fred("VIXCLS"), fred("VXVCLS"), fred("DFF")
    r = pd.concat([vix, vxv], axis=1, join="inner").dropna(); ratio = r.iloc[:, 0] / r.iloc[:, 1]
    dates = px.index; o, h, l, c = (px[k].to_numpy() for k in ["open", "high", "low", "close"])
    pc = np.r_[np.nan, c[:-1]]
    tr = np.maximum(h - l, np.maximum(abs(h - pc), abs(l - pc))); tr[0] = h[0] - l[0]
    atr = np.full(len(tr), np.nan); atr[13] = tr[:14].mean()
    for i in range(14, len(tr)):
        atr[i] = (atr[i - 1] * 13 + tr[i]) / 14
    dffc = dff.reindex(pd.date_range(dff.index[0], today + pd.Timedelta(days=5))).ffill()
    cum = pd.Series(np.cumsum(dffc.to_numpy() / 100.0), index=dffc.index)

    def sig(i):  # latest ratio dated strictly before session i
        k = ratio.index.searchsorted(dates[i], side="left") - 1
        return (ratio.iloc[k] > 1.0, ratio.index[k], float(ratio.iloc[k])) if k >= 0 else (False, None, np.nan)

    def net_R(e, x, pxit):
        p0 = c[e]; dist = SL_ATR * atr[e]
        nights = (dates[x] - dates[e]).days
        rs = cum.loc[dates[x] - pd.Timedelta(days=1)] - cum.loc[dates[e] - pd.Timedelta(days=1)] if nights > 0 else 0.0
        net = (pxit - p0) / p0 - PTS_RT / p0 - (rs + MARKUP * nights) / 360.0
        return net / (dist / p0), net

    trades, pos, notes = [], None, []

    def blocked(i):
        d = dates[i]; closed_today = [t for t in trades if t["exit_date"] == d]
        if len(trades) >= 2 and trades[-1]["R"] < 0 and trades[-2]["R"] < 0 and trades[-1]["exit_date"] == d:
            return "2 pierderi la rând azi"
        if sum(t["R"] for t in closed_today) * RISK <= -0.03:
            return "stop zilnic -3%"
        wk = d.isocalendar()[:2]
        if sum(t["R"] for t in trades if t["exit_date"].isocalendar()[:2] == wk) * RISK <= -0.06:
            return "stop săptămânal -6%"
        return None

    def try_enter(i):
        nonlocal pos
        ok, rd, rv = sig(i)
        if not ok: return
        b = blocked(i)
        if b: notes.append(f"{dates[i].date()}: semnal blocat ({b})"); return
        if i == len(dates) - 1 and i >= 1 and rd != dates[i - 1]:
            notes.append(f"{dates[i].date()}: VIX din {rd.date()} (lipsă {dates[i-1].date()} pe FRED) — decizie de reconfirmat la rularea următoare")
        pos = dict(e=i, sl=c[i] - SL_ATR * atr[i], ratio_date=rd, ratio=rv)

    s0 = int(dates.searchsorted(START))
    for i in range(s0, len(dates)):
        if pos is None:
            try_enter(i); continue
        e, sl = pos["e"], pos["sl"]; x = None
        if o[i] <= sl: x, pxit, why = i, o[i], "SL (gap la open)"
        elif l[i] <= sl: x, pxit, why = i, sl, "SL"
        elif i == e + H: x, pxit, why = i, c[i], f"timp ({H} sesiuni)"
        if x is not None:
            R, net = net_R(e, x, pxit)
            trades.append(dict(entry_date=dates[e], entry=c[e], sl=sl, atr=atr[e], ratio_date=pos["ratio_date"], ratio=pos["ratio"],
                               exit_date=dates[x], exit=pxit, reason=why, R=R, net_pct=net * 100))
            pos = None
            try_enter(i)

    last = len(dates) - 1
    eq = float(np.prod([1 + RISK * t["R"] for t in trades])) if trades else 1.0
    gp = sum(t["R"] for t in trades if t["R"] > 0); gl = -sum(t["R"] for t in trades if t["R"] < 0)
    pf = (gp / gl if gl > 0 else (float("inf") if gp > 0 else float("nan")))
    lr_ok, lr_d, lr_v = sig(last) if last >= 0 else (False, None, np.nan)
    try:
        yv, y3 = yahoo("^VIX")["close"], yahoo("^VIX3M")["close"]
        pv = (yv / y3).dropna(); prev = (pv.index[-1].date(), float(pv.iloc[-1]))
    except Exception as ex:
        prev = None; notes.append(f"previzualizare Yahoo ^VIX/^VIX3M indisponibilă: {ex}")
    latest_fred = (ratio.index[-1].date(), float(ratio.iloc[-1]))

    L = [f"# Shadow C14 — raport sesiunea {dates[last].date()}", "",
         "Jurnal pe hârtie. Nu se plasează ordine. Strategia a fost REJECTATĂ în backtest (random-entry p = 0.060);",
         "jurnalul colectează date noi, nevăzute. Evaluare doar după 30 de trade-uri închise.", "", "## REZUMAT", "",
         f"- Ultima sesiune completă: {dates[last].date()} — US100 (^NDX) close {c[last]:.2f}",
         f"- VIX/VIX3M FRED cel mai recent ({latest_fred[0]}): {latest_fred[1]:.4f} → {'BACKWARDATION' if latest_fred[1] > 1 else 'contango'}"]
    if prev:
        L.append(f"- Previzualizare Yahoo ({prev[0]}): {prev[1]:.4f} (decizia oficială se ia doar pe FRED)")
    if pos:
        e = pos["e"]; Ru, netu = net_R(e, last, c[last]) if last > e else (np.nan, np.nan)
        L += [f"- POZIȚIE DESCHISĂ (hârtie): long US100 din {dates[e].date()} la {c[e]:.2f} (VIX/VIX3M {pos['ratio_date'].date()} = {pos['ratio']:.4f}); "
              f"SL {pos['sl']:.2f} (distanță {SL_ATR*atr[e]:.1f} puncte = {SL_ATR*atr[e]/c[e]*100:.2f}%); TP: fără, ieșire pe timp după {H} sesiuni "
              f"(ținută {last - e}, rămase {max(e + H - last, 0)})",
              f"- Nerealizat la close {dates[last].date()}: {Ru:+.2f}R ({netu*100:+.2f}% pe noțional)" if last > e else f"- Intrare la close-ul sesiunii {dates[e].date()}",
              f"- Lot (1% risc): loturi = equity × 1% / ({SL_ATR*atr[e]:.1f} puncte × valoarea unui punct pe lot la brokerul tău)"]
    else:
        if ratio.index[-1] >= dates[last]:
            nxt = "INTRARE long la close-ul sesiunii următoare" if latest_fred[1] > 1 else "niciun semnal la close-ul sesiunii următoare"
            L.append(f"- Fără poziție. Decizie pentru sesiunea următoare (VIX/VIX3M FRED {latest_fred[0]}): {nxt}")
        else:
            hint = "" if not prev else f"; previzualizarea Yahoo indică {'INTRARE' if prev[1] > 1 else 'niciun semnal'}"
            L.append(f"- Fără poziție. Decizia pentru sesiunea următoare depinde de VIX/VIX3M din {dates[last].date()}, "
                     f"încă nepublicat pe FRED{hint}")
    L += [f"- Trade-uri închise: {len(trades)} | sumă {sum(t['R'] for t in trades):+.2f}R | PF {pf:.2f} | equity hârtie {100*eq:.2f} (start 100, 1% risc/trade)",
          f"- Reguli de risc: {blocked(last) or 'OK'}", ""]
    if notes:
        L += ["## Note", ""] + [f"- {n}" for n in notes] + [""]
    if trades:
        L += ["## Trade-uri închise", "", "| intrare | preț | SL | ieșire | preț | motiv | R |", "|---|---|---|---|---|---|---|"]
        L += [f"| {t['entry_date'].date()} | {t['entry']:.2f} | {t['sl']:.2f} | {t['exit_date'].date()} | {t['exit']:.2f} | {t['reason']} | {t['R']:+.2f} |" for t in trades]
    rep = "\n".join(L) + "\n"
    import os
    os.makedirs(f"{a.repo}/shadow/reports", exist_ok=True)
    open(f"{a.repo}/shadow/STATUS.md", "w").write(rep)
    open(f"{a.repo}/shadow/reports/{dates[last].date()}.md", "w").write(rep)
    cols = ["entry_date", "entry", "sl", "atr", "ratio_date", "ratio", "exit_date", "exit", "reason", "R", "net_pct"]
    pd.DataFrame(trades, columns=cols).to_csv(f"{a.repo}/shadow/ledger.csv", index=False)
    print(rep)


if __name__ == "__main__":
    main()

"""Dukascopy minute BID/ASK candles: download (cached) and decode.
Format: LZMA-compressed records of >iiiiif = (seconds from 00:00 UTC, open, close, low, high, volume).
Prices are integers; the divisor is calibrated against an external reference level (see scale())."""
import lzma, os, struct, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd

URL = "https://datafeed.dukascopy.com/datafeed/{sym}/{y}/{m:02d}/{d:02d}/{side}_candles_min_1.bi5"


def path(root, sym, side, day):
    return f"{root}/{sym}/{side}/{day:%Y-%m-%d}.bi5"


def fetch_one(args, pause=0.4):
    """Sequential-friendly: honours Dukascopy's rate limit (HTTP 429) with growing back-off."""
    root, sym, side, day = args
    p = path(root, sym, side, day)
    if os.path.exists(p):
        return p, "cached"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    url = URL.format(sym=sym, y=day.year, m=day.month - 1, d=day.day, side=side)  # month is 0-based
    wait = 20
    for k in range(12):
        r = subprocess.run(["curl", "-s", "-m", "60", "-o", p + ".part", "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout
        if r.returncode == 0 and code in ("200", "404"):
            if code == "404":
                open(p + ".part", "wb").close()
            os.replace(p + ".part", p); time.sleep(pause)
            return p, code
        time.sleep(wait if code == "429" else 5); wait = min(wait * 2, 300)
    if os.path.exists(p + ".part"):
        os.remove(p + ".part")
    return p, f"fail rc={r.returncode} http={code}"


def fetch(root, sym, days, workers=1, log=None):
    jobs = [(root, sym, side, d) for d in days for side in ("BID", "ASK")]
    res = []
    for n, j in enumerate(jobs, 1):
        res.append(fetch_one(j))
        if log and n % 100 == 0:
            print(f"{sym} {n}/{len(jobs)} last={res[-1][1]}", file=log, flush=True)
    bad = [r for r in res if r[1].startswith("fail")]
    return len(res), bad


def decode(p, day):
    if not os.path.exists(p):
        return None
    raw = open(p, "rb").read()
    if not raw:
        return None
    data = lzma.decompress(raw, format=lzma.FORMAT_ALONE)
    n = len(data) // 24
    a = np.frombuffer(data[: n * 24], dtype=np.dtype([("t", ">i4"), ("o", ">i4"), ("c", ">i4"), ("l", ">i4"), ("h", ">i4"), ("v", ">f4")]))
    idx = pd.Timestamp(day, tz="UTC") + pd.to_timedelta(a["t"].astype(np.int64), unit="s")
    cols = {k: a[k].astype(np.int64) for k in ("o", "h", "l", "c")}; cols["v"] = a["v"].astype(np.float64)
    return pd.DataFrame(cols, index=idx.tz_convert("America/New_York"))


def load_day(root, sym, day, div):
    out = {}
    for side in ("BID", "ASK"):
        df = decode(path(root, sym, side, day), day)
        if df is None or df.empty:
            return None
        out[side] = df[["o", "h", "l", "c"]].astype(float) / div
    return out


if __name__ == "__main__":  # python3 -I duka.py <root> <SYM> <start> <end>  (fetch all calendar weekdays)
    root, sym, a, b = sys.argv[1:5]
    days = [d for d in pd.date_range(a, b) if d.weekday() < 5]
    n, bad = fetch(root, sym, days, log=sys.stdout)
    print(f"{sym}: {n} files, {len(bad)} failed", bad[:5])

"""Fetch prices from Yahoo, compute GARCH(1,1), write JSON files into docs/data/.

Run by the GitHub workflow every weekday evening. If Yahoo returns nothing for a
ticker, the previous data for it is kept and marked STALE, so the site never breaks.
"""
import datetime as dt
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

from tickers import BENCHMARK, LISTED, START_DATE

warnings.filterwarnings("ignore")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "data")
TD = 252


def download_one(ticker, start=START_DATE, tries=3):
    import yfinance as yf

    for _ in range(tries):
        try:
            df = yf.download(ticker, start=start, auto_adjust=True, progress=False)
            if df is not None and not df.empty:
                close = df["Close"]
                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:, 0]
                s = close.dropna()
                s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
                return s.rename(ticker)
        except Exception:
            pass
        time.sleep(2)
    return None


def read_json(name):
    p = os.path.join(DATA, name)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def write_json(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"), allow_nan=False)


def clean(x, nd):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), nd)


def main():
    allt = {**LISTED, **BENCHMARK}
    old = read_json("prices.json")
    series, status = {}, []

    for name, tk in allt.items():
        s = download_one(tk)
        if s is not None and len(s) > 30:
            series[name] = s
            status.append({"name": name, "ticker": tk, "status": "OK", "rows": int(len(s)), "last": str(s.index.max().date())})
        elif old and name in old["cols"]:
            o = pd.Series(old["cols"][name], index=pd.to_datetime(old["dates"]), dtype="float64").dropna()
            series[name] = o
            status.append({"name": name, "ticker": tk, "status": "STALE (Yahoo gave nothing, kept previous data)", "rows": int(len(o)), "last": str(o.index.max().date())})
        else:
            status.append({"name": name, "ticker": tk, "status": "EMPTY (no data on Yahoo for this ticker)", "rows": 0, "last": ""})
        print(status[-1])

    fresh = [s for s in status if s["status"] == "OK"]
    if not fresh:
        print("ERROR: Yahoo returned no fresh data at all. Keeping ALL previous files unchanged (the 'updated' time stays at the last good run).")
        sys.exit(1)

    prices = pd.concat(series, axis=1).sort_index()
    dates = [d.strftime("%Y-%m-%d") for d in prices.index]
    write_json("prices.json", {"dates": dates, "cols": {c: [clean(v, 4) for v in prices[c].tolist()] for c in prices.columns}})

    # GARCH(1,1) per stock (not for the benchmark)
    params, cond = {}, {}
    try:
        from arch import arch_model

        rets = np.log(prices / prices.shift(1))
        for c in prices.columns:
            if c in BENCHMARK:
                continue
            r = rets[c].dropna() * 100
            if len(r) < 250:
                continue
            try:
                res = arch_model(r, vol="Garch", p=1, q=1, dist="t", mean="Constant").fit(disp="off")
                p = res.params
                params[c] = {"omega": clean(p["omega"], 5), "alpha": clean(p["alpha[1]"], 4), "beta": clean(p["beta[1]"], 4),
                             "persistence": clean(p["alpha[1]"] + p["beta[1]"], 4), "n": int(len(r))}
                cv = (res.conditional_volatility * np.sqrt(TD)).reindex(prices.index)
                cond[c] = [clean(v, 2) for v in cv.tolist()]
            except Exception as e:
                print("GARCH failed for", c, str(e)[:80])
    except ImportError:
        print("arch not installed: skipping GARCH")
    write_json("garch.json", {"dates": dates, "params": params, "cond": cond})
    write_json("status.json", {"updated_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", "ok": True, "tickers": status})
    print(f"done: {prices.shape[1]} series, {len(dates)} days, GARCH for {len(params)}")


if __name__ == "__main__":
    main()

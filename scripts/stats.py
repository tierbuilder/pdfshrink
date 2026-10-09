#!/usr/bin/env python3
"""Print usage stats from Workers Analytics Engine (dataset pdfshrink).

    CF_ACCOUNT_ID=... CF_API_TOKEN=... python3 scripts/stats.py [days]

The API token needs the "Account Analytics: Read" permission
(dash.cloudflare.com → My Profile → API Tokens → Create Token → Custom).
"""
import json
import os
import sys
import urllib.request

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
ACCOUNT, TOKEN = os.environ.get("CF_ACCOUNT_ID"), os.environ.get("CF_API_TOKEN")
WHERE = f"timestamp > NOW() - INTERVAL '{DAYS}' DAY"
N = "SUM(_sample_interval)"  # Analytics Engine samples at high volume; this re-weights counts

QUERIES = {
    "Events": f"SELECT blob1 AS event, {N} AS n FROM pdfshrink WHERE {WHERE} GROUP BY event ORDER BY n DESC",
    "Pages where tools were used": f"SELECT blob2 AS page, {N} AS n FROM pdfshrink WHERE {WHERE} AND blob1 != 'files_added' AND blob1 != 'images_added' GROUP BY page ORDER BY n DESC LIMIT 15",
    "PDF compress: mode / method": f"SELECT blob4 AS mode, blob5 AS method, {N} AS n, round(SUM(_sample_interval * double1) / SUM(_sample_interval)) AS avg_saved_pct FROM pdfshrink WHERE {WHERE} AND blob1 = 'compressed' GROUP BY mode, method ORDER BY n DESC",
    "Exact-size hit rate (PDF + image)": f"SELECT blob1 AS event, blob6 AS hit, {N} AS n FROM pdfshrink WHERE {WHERE} AND blob6 != '' AND blob1 IN ('compressed', 'image_resized') GROUP BY event, hit ORDER BY event, hit",
    "Image target sizes (KB)": f"SELECT double2 AS kb, {N} AS n FROM pdfshrink WHERE {WHERE} AND blob1 = 'image_resized' GROUP BY kb ORDER BY n DESC LIMIT 10",
    "Countries": f"SELECT blob3 AS country, {N} AS n FROM pdfshrink WHERE {WHERE} GROUP BY country ORDER BY n DESC LIMIT 10",
    "Errors": f"SELECT blob7 AS message, {N} AS n FROM pdfshrink WHERE {WHERE} AND blob1 = 'error' GROUP BY message ORDER BY n DESC LIMIT 10",
}


def query(sql):
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/analytics_engine/sql",
        data=(sql + " FORMAT JSON").encode(), headers={"Authorization": f"Bearer {TOKEN}"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def table(rows):
    if not rows:
        print("  (no data yet)")
        return
    cols = list(rows[0])
    widths = [max(len(c), *(len(str(r[c])) for r in rows)) for c in cols]
    print("  " + "  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    for r in rows:
        print("  " + "  ".join(str(r[c]).ljust(w) for c, w in zip(cols, widths)))


if __name__ == "__main__":
    if not ACCOUNT or not TOKEN:
        sys.exit(__doc__)
    print(f"pdfshrink usage — last {DAYS} day(s)\n")
    for title, sql in QUERIES.items():
        print(title)
        try:
            table(query(sql).get("data", []))
        except urllib.error.HTTPError as e:
            print("  error:", e.code, e.read().decode()[:200])
        print()

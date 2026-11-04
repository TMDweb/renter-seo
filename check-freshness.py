#!/usr/bin/env python3
"""Check that every Renter ticket page and the dev board are current on GitHub Pages.

Usage: git pull, then python3 check-freshness.py [YYYY-MM-DD]   (default: today)
Lists every folder with an index.html, so pull first or new tickets are missed.
Exit 0 only when every page passes.
"""
import datetime, glob, os, random, re, ssl, sys, urllib.request
import certifi

BASE = "https://tmdweb.github.io/renter-seo/"
ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"assets", ".git", ".claude"}

day = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
want = f"{day:%b} {day.day}, {day.year}"  # e.g. "Nov 5, 2026"
ctx = ssl.create_default_context(cafile=certifi.where())

folders = sorted(d for d in os.listdir(ROOT)
                 if d not in SKIP and os.path.isfile(os.path.join(ROOT, d, "index.html")))
fails = 0
print(f"Checking {len(folders)} pages for '{want}'\n")
for d in folders:
    url = f"{BASE}{d}/?v={random.randint(1, 10**9)}"
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "freshness-check"}),
                                      timeout=30, context=ctx).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"FAIL  {d:34} not reachable: {e}"); fails += 1; continue
    kicker = re.search(r'class="kicker">([^<]*)', html)
    pill = re.search(r'class="statusbar"><span class="pill (\w+)">([^<]*)', html)
    k = kicker.group(1).strip() if kicker else ""
    p = f"{pill.group(1)}: {pill.group(2)}" if pill else "no statusbar"
    probs = []
    if not kicker: probs.append("no date stamp (kicker)")
    elif want not in k: probs.append(f"stale stamp: {k.split('·')[-1].strip()}")
    if not pill: probs.append("no statusbar")
    elif pill.group(1) != "done" and re.match(r"\s*(DONE|FIXED|COMPLETED)\b", pill.group(2)):
        probs.append("label says done but pill is not green")
    if probs:
        fails += 1; print(f"FAIL  {d:34} {p:40} {'; '.join(probs)}")
    else:
        print(f"ok    {d:34} {p}")
print(f"\n{len(folders) - fails} of {len(folders)} pass")
sys.exit(1 if fails else 0)

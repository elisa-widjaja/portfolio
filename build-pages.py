#!/usr/bin/env python3
"""Generate a real page per case study for GitHub Pages.

index.html is a single page with a hash router. For the live site we want
/recifriend-social etc. to be real URLs (so analytics can count each case
study and links survive a refresh), so this writes <slug>/index.html for
every visible project. Each copy is index.html with a <base href="/"> so
relative assets still resolve, and the project's title in <title>.
Run from the repo root; the deploy workflow calls it before uploading.
"""
import html
import json
import os
import re

src = open("index.html", encoding="utf-8").read()
blob = re.search(r'<script id="projects-data" type="application/json">(.*?)</script>', src, re.S).group(1)
projects = json.loads(blob)

def page(title):
    out = src.replace("<head>", '<head>\n<base href="/">', 1)
    if title:
        out = re.sub(r"<title>.*?</title>", "<title>" + html.escape(title) + " — Elisa Widjaja</title>", out, count=1, flags=re.S)
    return out

made = []
for slug, p in projects.items():
    if p.get("hidden"):
        continue
    os.makedirs(slug, exist_ok=True)
    with open(os.path.join(slug, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(p.get("t")))
    made.append(slug)

# Unknown paths render the home page instead of GitHub's 404.
with open("404.html", "w", encoding="utf-8") as f:
    f.write(page(None))

print("built", len(made), "pages:", ", ".join(made))

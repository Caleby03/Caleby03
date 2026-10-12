"""Generates the README analytics cards as static SVGs.

Needs no personal access token: profile, repository and language data come
from the REST API using the workflow's built-in GITHUB_TOKEN (public repos
only), and contribution counts come from the public contribution calendar,
which includes private contributions as anonymous counts when "Include
private contributions on my profile" is enabled.

Usage: python metrics.py <username> <output_dir>
"""

import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

API = "https://api.github.com"
# Markup languages would otherwise dominate the card and misrepresent the stack.
IGNORED_LANGUAGES = {"HTML", "CSS", "SCSS", "Jupyter Notebook"}
LANGUAGE_LIMIT = 8
PALETTE = ["#3B82F6", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6", "#64748B"]

STYLE = """
<style>
  .bg { fill: #ffffff; stroke: #e5e7eb; }
  .title { font: 600 16px 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #2563EB; }
  .label { font: 400 13px 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #4b5563; }
  .value { font: 700 13px 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #111827; }
  .big { font: 700 26px 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #111827; }
  .sub { font: 400 11px 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #6b7280; }
  .l0 { fill: #ebedf0; } .l1 { fill: #bfdbfe; } .l2 { fill: #60a5fa; } .l3 { fill: #2563eb; } .l4 { fill: #1e3a8a; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #0d1117; stroke: #30363d; }
    .title { fill: #58a6ff; }
    .label { fill: #9ca3af; }
    .value, .big { fill: #f3f4f6; }
    .sub { fill: #8b949e; }
    .l0 { fill: #161b22; } .l1 { fill: #1e3a8a; } .l2 { fill: #2563eb; } .l3 { fill: #60a5fa; } .l4 { fill: #bfdbfe; }
  }
</style>
"""


def fetch(url, accept="application/vnd.github+json"):
    headers = {"Accept": accept, "User-Agent": "readme-metrics"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
        body = resp.read().decode()
    return json.loads(body) if url.startswith(API) else body


def fetch_repos(user):
    repos, page = [], 1
    while True:
        batch = fetch(f"{API}/users/{user}/repos?type=owner&per_page=100&page={page}")
        repos += batch
        if len(batch) < 100:
            return [r for r in repos if not r["fork"] and not r["archived"]]
        page += 1


def parse_calendar(page):
    """Returns {date: count} from the public contributions page."""
    id_to_date = {}
    for tag in re.findall(r"<td\b[^>]*>", page):
        date, cell = re.search(r'data-date="([\d-]+)"', tag), re.search(r'\bid="([^"]+)"', tag)
        if date and cell:
            id_to_date[cell.group(1)] = date.group(1)
    counts = {}
    for target, text in re.findall(r'<tool-tip[^>]*?for="([^"]+)"[^>]*>(.*?)</tool-tip>', page, re.S):
        if target in id_to_date:
            m = re.match(r"\s*(\d[\d,]*) contributions?", text)
            counts[id_to_date[target]] = int(m.group(1).replace(",", "")) if m else 0
    if not counts:
        raise RuntimeError("could not parse contribution calendar; GitHub markup may have changed")
    return dict(sorted(counts.items()))


def streaks(counts, today):
    days = sorted(d for d in counts if d <= today.isoformat())
    longest = run = 0
    for d in days:
        run = run + 1 if counts[d] else 0
        longest = max(longest, run)
    current = 0
    # Today without contributions yet doesn't break the streak.
    for i, d in enumerate(reversed(days)):
        if counts[d]:
            current += 1
        elif i > 0:
            break
    return current, longest


def card(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">{STYLE}'
        f'<rect class="bg" x="0.5" y="0.5" rx="6" width="{width - 1}" height="{height - 1}"/>'
        f"{body}</svg>\n"
    )


def overview_svg(user, profile, repos, total):
    joined = dt.date.fromisoformat(profile["created_at"][:10])
    rows = [
        ("Contributions (last year)", f"{total:,}"),
        ("Public repositories", str(len(repos))),
        ("Stars earned", str(sum(r["stargazers_count"] for r in repos))),
        ("Followers", str(profile["followers"])),
        ("On GitHub since", joined.strftime("%b %Y")),
    ]
    body = f'<text class="title" x="20" y="32">{html.escape(profile.get("name") or user)}\'s GitHub Stats</text>'
    for i, (label, value) in enumerate(rows):
        y = 62 + i * 24
        body += f'<text class="label" x="20" y="{y}">{label}</text>'
        body += f'<text class="value" x="475" y="{y}" text-anchor="end">{value}</text>'
    return card(495, 185, body)


def languages_svg(totals):
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:LANGUAGE_LIMIT]
    whole = sum(v for _, v in top) or 1
    body = '<text class="title" x="20" y="32">Most Used Languages</text>'
    x = 20.0
    for i, (_, size) in enumerate(top):
        w = 455 * size / whole
        body += f'<rect x="{x:.2f}" y="48" width="{w:.2f}" height="8" fill="{PALETTE[i]}"/>'
        x += w
    for i, (name, size) in enumerate(top):
        cx, cy = 20 + (i % 2) * 230, 82 + (i // 2) * 24
        body += f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{PALETTE[i]}"/>'
        body += f'<text class="label" x="{cx + 16}" y="{cy}">{html.escape(name)} {100 * size / whole:.1f}%</text>'
    if not top:
        body += '<text class="label" x="20" y="82">No language data yet</text>'
    return card(495, 82 + ((len(top) + 1) // 2) * 24, body)


def streak_svg(counts, today):
    current, longest = streaks(counts, today)
    total = sum(counts.values())
    body = ""
    for i, (value, label) in enumerate(
        [(f"{total:,}", "Contributions (last year)"), (str(current), "Current streak (days)"), (str(longest), "Longest streak (days)")]
    ):
        cx = 92 + i * 155
        body += f'<text class="big" x="{cx}" y="44" text-anchor="middle">{value}</text>'
        body += f'<text class="sub" x="{cx}" y="62" text-anchor="middle">{label}</text>'
    # Heatmap: last 53 weeks, columns start on Sunday like GitHub's calendar.
    start = today - dt.timedelta(days=today.weekday() + 1 + 52 * 7)
    nonzero = sorted(c for c in counts.values() if c)
    cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.5, 0.75)] if nonzero else [1, 1, 1]
    for n in range((today - start).days + 1):
        d = start + dt.timedelta(days=n)
        c = counts.get(d.isoformat(), 0)
        level = 0 if not c else 1 + sum(c >= cut for cut in cuts)
        body += f'<rect class="l{min(level, 4)}" x="{20 + (n // 7) * 8.6:.1f}" y="{80 + (n % 7) * 8.6:.1f}" width="7" height="7" rx="1.5"/>'
    return card(495, 152, body)


def main():
    user, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=-5))).date()

    profile = fetch(f"{API}/users/{user}")
    repos = fetch_repos(user)
    counts = parse_calendar(fetch(f"https://github.com/users/{user}/contributions", accept="text/html"))

    languages = {}
    for repo in repos:
        for name, size in fetch(repo["languages_url"]).items():
            if name not in IGNORED_LANGUAGES:
                languages[name] = languages.get(name, 0) + size

    (out / "overview.svg").write_text(overview_svg(user, profile, repos, sum(counts.values())))
    (out / "languages.svg").write_text(languages_svg(languages))
    (out / "streak.svg").write_text(streak_svg(counts, today))
    print(f"wrote cards to {out}: {len(repos)} repos, {len(languages)} languages, {sum(counts.values())} contributions")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Repo Radar — find new, fast-rising GitHub repos that match your interests.

Reads interests.yml, queries the GitHub Search API for recently-created repos
that are gaining stars, ranks them by momentum (stars/day), drops anything
already reported, writes a dated markdown digest, and (optionally) opens a
GitHub issue with the results.

Delivery is configurable:
    SEND_EMAIL=true   + SMTP_USER/SMTP_PASS (+ EMAIL_TO)   → email the digest
    CREATE_ISSUE=true + GITHUB_TOKEN/GITHUB_REPOSITORY      → open a GitHub issue

Zero runtime deps except PyYAML. Auth via the GITHUB_TOKEN env var — optional
for searching (improves rate limits), required only to open an issue.

Usage:
    GITHUB_TOKEN=<token> python repo-radar/radar.py        # full run
    python repo-radar/radar.py --selftest                  # offline sanity check
"""
from __future__ import annotations

import html as html_lib
import json
import math
import os
import re
import smtplib
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "interests.yml"
SEEN = ROOT / "seen.json"
DIGESTS = ROOT / "digests"
API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "").strip()


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #
def _request(url, *, data=None, method="GET"):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "repo-radar")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def search(query, *, sort="stars", order="desc", per_page=30):
    params = {"q": query, "sort": sort, "order": order, "per_page": per_page}
    url = f"{API}/search/repositories?{urllib.parse.urlencode(params)}"
    try:
        return _request(url).get("items", [])
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:200]
        print(f"  ! query failed ({e.code}): {query}\n    {body}", file=sys.stderr)
        # Secondary rate limit — back off and retry once.
        if e.code in (403, 429):
            time.sleep(20)
            try:
                return _request(url).get("items", [])
            except Exception:
                return []
        return []
    except Exception as e:  # pragma: no cover - network failure
        print(f"  ! query error: {query} -> {e}", file=sys.stderr)
        return []


def create_issue(title, body):
    url = f"{API}/repos/{REPO}/issues"
    payload = json.dumps({"title": title, "body": body}).encode()
    try:
        data = _request(url, data=payload, method="POST")
        print(f"Opened issue #{data['number']}: {data['html_url']}")
    except urllib.error.HTTPError as e:  # pragma: no cover - network
        print(f"! issue creation failed ({e.code}): {e.read().decode()[:200]}",
              file=sys.stderr)


# --------------------------------------------------------------------------- #
# Email delivery
# --------------------------------------------------------------------------- #
def md_to_html(md):
    """Render the digest markdown as a clean, email-client-friendly HTML body."""
    def inline(s):
        s = html_lib.escape(s)
        # Stash `code` spans first so their contents escape no further markup
        # (e.g. the underscores in `CLAUDE_MEMORY` must not become italics).
        codes = []

        def stash(m):
            codes.append(m.group(1))
            return f"\x00{len(codes) - 1}\x00"

        s = re.sub(r"`([^`]+)`", stash, s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                   r'<a href="\2" style="color:#2563eb;text-decoration:none">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        # Underscore italics only at word boundaries — never inside snake_case.
        s = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<em>\1</em>", s)
        s = re.sub(r"\x00(\d+)\x00",
                   lambda m: '<code style="background:#f3f3f3;padding:1px 4px;'
                             f'border-radius:3px;font-size:13px">{codes[int(m.group(1))]}</code>',
                   s)
        return s

    out = ['<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,'
           'sans-serif;max-width:680px;margin:0 auto;color:#1a1a1a;line-height:1.5">']
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            out.append(f'<h1 style="font-size:22px;margin:0 0 4px">{inline(line[2:])}</h1>')
        elif line.startswith("## "):
            out.append(f'<h2 style="font-size:16px;margin:26px 0 8px;'
                       f'border-bottom:1px solid #eee;padding-bottom:4px">{inline(line[3:])}</h2>')
        elif line.strip() == "---":
            out.append('<hr style="border:none;border-top:1px solid #eee;margin:24px 0">')
        elif line.lstrip().startswith(">"):
            out.append(f'<div style="color:#555;font-size:14px;margin:2px 0 6px 16px">'
                       f'{inline(line.lstrip()[1:].strip())}</div>')
        elif re.match(r"^\d+\.\s", line):
            item = inline(re.sub(r"^\d+\.\s", "", line))
            out.append(f'<div style="margin-top:12px">{item}</div>')
        else:
            out.append(f'<p style="color:#444;font-size:14px">{inline(line)}</p>')
    out.append("</div>")
    return "\n".join(out)


def send_email(subject, markdown):
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "").strip()
    pwd = os.environ.get("SMTP_PASS", "").strip()
    to = (os.environ.get("EMAIL_TO") or user).strip()
    if not (user and pwd and to):
        print("! email not configured (need SMTP_USER, SMTP_PASS) — skipping",
              file=sys.stderr)
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.set_content(markdown)
    msg.add_alternative(md_to_html(markdown), subtype="html")
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=30) as s:
            s.starttls(context=ctx)
            s.login(user, pwd)
            s.send_message(msg)
        print(f"Emailed digest to {to}")
    except Exception as e:  # pragma: no cover - network
        print(f"! email send failed: {e}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def score(repo, now):
    """Momentum-first score: stars/day dominates, with floors for size + activity."""
    stars = repo.get("stargazers_count", 0)
    age_days = max((now - parse_dt(repo["created_at"])).total_seconds() / 86400, 1.0)
    velocity = stars / age_days
    pushed = parse_dt(repo["pushed_at"]) if repo.get("pushed_at") else parse_dt(repo["created_at"])
    active = (now - pushed).days <= 30
    composite = velocity * 30 + math.log2(stars + 1) + (5 if active else 0)
    return composite, velocity


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def render(results, now, new_count, within, min_stars):
    lines = [f"# 🛰️ Repo Radar — {now:%Y-%m-%d}", ""]
    if new_count:
        lines += [
            f"_{new_count} new repos, created in the last {within} days, "
            f"≥{min_stars}⭐ (some lanes set their own floor), "
            f"ranked by momentum (stars/day)._",
            "",
        ]
    else:
        lines += ["No new repos cleared the bar this run. The hunt continues.", ""]

    for name, repos in results:
        lines.append(f"## {name}")
        lines.append("")
        if not repos:
            lines += ["_Nothing new this run._", ""]
            continue
        for i, r in enumerate(repos, 1):
            lang = r.get("language") or "—"
            created = r["created_at"][:10]
            desc = (r.get("description") or "").strip() or "_no description_"
            lines.append(
                f"{i}. **[{r['full_name']}]({r['html_url']})** — "
                f"⭐ {r['stargazers_count']:,} · {r['_vel']:.1f}/day · "
                f"{lang} · since {created}"
            )
            lines.append(f"   > {desc}")
        lines.append("")

    lines += [
        "---",
        "",
        "_Generated by `repo-radar/radar.py`. "
        "Tune `repo-radar/interests.yml` to refine what shows up._",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def collect(cfg, now):
    st = cfg.get("settings", {}) or {}
    within = int(st.get("created_within_days", 120))
    min_stars = int(st.get("min_stars", 50))
    per_theme = int(st.get("per_theme", 6))
    langs = {l.lower() for l in (st.get("languages") or [])}
    excl_owners = {o.lower() for o in (st.get("exclude_owners") or [])}
    excl_kw = [k.lower() for k in (st.get("exclude_keywords") or [])]

    since = (now - timedelta(days=within)).strftime("%Y-%m-%d")

    seen = json.loads(SEEN.read_text()) if SEEN.exists() else {"repos": {}}
    seen_repos = seen.setdefault("repos", {})

    run_seen = set()          # dedupe across themes within a single run
    results = []
    new_count = 0

    for theme in cfg.get("themes", []):
        name = theme["name"]
        theme_min = int(theme.get("min_stars", min_stars))
        filt = f"created:>={since} stars:>={theme_min}"
        bucket = {}
        for q in theme.get("queries", []):
            full_q = f"{q} {filt}"
            print(f"[{name}] {full_q}", file=sys.stderr)
            for repo in search(full_q):
                fn = repo["full_name"]
                if fn in bucket or fn in run_seen:
                    continue
                if repo["owner"]["login"].lower() in excl_owners:
                    continue
                text = f"{repo['name']} {repo.get('description') or ''}".lower()
                if any(k in text for k in excl_kw):
                    continue
                if langs and (repo.get("language") or "").lower() not in langs:
                    continue
                bucket[fn] = repo
            time.sleep(1)  # stay clear of the search rate limit

        ranked = []
        for repo in bucket.values():
            repo["_score"], repo["_vel"] = score(repo, now)
            ranked.append(repo)
        ranked.sort(key=lambda r: r["_score"], reverse=True)

        fresh = [r for r in ranked if r["full_name"] not in seen_repos][:per_theme]
        for r in fresh:
            run_seen.add(r["full_name"])
        results.append((name, fresh))
        new_count += len(fresh)

    return results, new_count, within, min_stars, seen, seen_repos


def main():
    cfg = yaml.safe_load(CONFIG.read_text())
    now = datetime.now(timezone.utc)

    results, new_count, within, min_stars, seen, seen_repos = collect(cfg, now)

    digest = render(results, now, new_count, within, min_stars)
    DIGESTS.mkdir(exist_ok=True)
    (DIGESTS / f"{now:%Y-%m-%d}.md").write_text(digest)
    (DIGESTS / "latest.md").write_text(digest)
    print(f"\nWrote digest for {now:%Y-%m-%d} — {new_count} new repos")

    for _, repos in results:
        for r in repos:
            seen_repos[r["full_name"]] = now.strftime("%Y-%m-%d")
    SEEN.write_text(json.dumps(seen, indent=2, sort_keys=True) + "\n")

    subject = f"🛰️ Repo Radar — {now:%Y-%m-%d} ({new_count} new)"

    if os.environ.get("SEND_EMAIL", "").lower() in ("1", "true", "yes"):
        if new_count:
            send_email(subject, digest)
        else:
            print("No new repos — skipping email.")

    if os.environ.get("CREATE_ISSUE", "").lower() in ("1", "true", "yes"):
        if new_count and REPO and TOKEN:
            create_issue(subject, digest)
        elif not new_count:
            print("No new repos — skipping issue.")


# --------------------------------------------------------------------------- #
# Offline self-test (no network)
# --------------------------------------------------------------------------- #
def selftest():
    now = datetime.now(timezone.utc)
    fake = [
        {
            "full_name": "acme/agent-kit", "html_url": "https://github.com/acme/agent-kit",
            "name": "agent-kit", "description": "A tiny MCP agent framework.",
            "owner": {"login": "acme"}, "language": "Python",
            "stargazers_count": 1800,
            "created_at": (now - timedelta(days=40)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pushed_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        {
            "full_name": "acme/awesome-llms", "html_url": "https://github.com/acme/awesome-llms",
            "name": "awesome-llms", "description": "A curated list.",
            "owner": {"login": "acme"}, "language": "Markdown",
            "stargazers_count": 9000,
            "created_at": (now - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pushed_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    ]
    for r in fake:
        r["_score"], r["_vel"] = score(r, now)
    digest = render([("AI agents & LLM tooling", [fake[0]])], now, 1, 120, 50)
    assert "agent-kit" in digest
    assert "/day" in digest
    assert fake[0]["_vel"] > 0
    print(digest)
    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()

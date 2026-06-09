#!/usr/bin/env python3
"""
Weekly email digest — no external dependencies.
Uses only stdlib: smtplib, email.mime, subprocess, os, datetime.

Secrets (GitHub Actions env vars):
  GMAIL_USER          sender Gmail address
  GMAIL_APP_PASSWORD  16-character Google App Password
  DIGEST_RECIPIENTS   comma-separated recipient list
"""

import os
import smtplib
import subprocess
import sys
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── configuration ─────────────────────────────────────────────────────────────

GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENTS_RAW = os.environ.get("DIGEST_RECIPIENTS", "")

RESEARCHER_NAME = "Felipe Villasuso Lago"
INSTITUTION = "London South Bank University (LSBU)"
SITE_URL = "https://felipelago17.github.io/Joint-ventures-and-Energy-Trilemma-/"
REPO_URL = "https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-"

HARDCODED_DEADLINES = [
    {
        "date": "10 November 2026",
        "title": "BIS Affiliates Rule snap-back",
        "detail": (
            "US Bureau of Industry and Security (BIS) temporary general licence "
            "for affiliated-entity transactions is scheduled to expire. "
            "JV partners with US-person connections in Norwegian/UAE upstream should "
            "review affiliate transaction compliance before this date."
        ),
    },
]


# ── git helpers ───────────────────────────────────────────────────────────────

def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout.strip()


def commits_since_7_days():
    raw = git("log", "--since=7 days ago", "--oneline", "--no-merges")
    if not raw:
        return []
    out = []
    for line in raw.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            out.append((parts[0], parts[1]))
    return out


def changed_files_since_7_days():
    raw = git(
        "log", "--since=7 days ago",
        "--name-status", "--pretty=format:", "--no-merges",
        "--diff-filter=ACDMRT",
    )
    new_files, modified_files = [], []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        status, path = parts[0][0], parts[1]
        if status == "A":
            new_files.append(path)
        else:
            modified_files.append(path)
    return sorted(set(new_files)), sorted(set(modified_files))


def classify_by_folder(paths):
    buckets = {"literature": [], "regulations": [], "news": [], "other": []}
    for p in paths:
        if p.startswith("literature/") or p.startswith("docs/literature/"):
            buckets["literature"].append(p)
        elif p.startswith("regulations/") or p.startswith("docs/regulations/"):
            buckets["regulations"].append(p)
        elif p.startswith("news/") or p.startswith("docs/news/"):
            buckets["news"].append(p)
        else:
            buckets["other"].append(p)
    return buckets


# ── HTML builder ──────────────────────────────────────────────────────────────

CSS = """
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif;
         max-width: 660px; margin: 0 auto; padding: 24px 20px; color: #1a1a2e; }
  h1   { color: #1a237e; font-size: 1.4em; border-bottom: 3px solid #1a237e;
         padding-bottom: 10px; margin-bottom: 6px; }
  .meta { color: #555; font-size: 0.85em; margin-bottom: 28px; }
  h2   { color: #283593; font-size: 1.05em; margin-top: 30px; margin-bottom: 8px;
         border-left: 4px solid #3949ab; padding-left: 10px; }
  ul   { margin: 0; padding-left: 20px; }
  li   { margin-bottom: 5px; line-height: 1.5; }
  .commit-hash { font-family: 'SFMono-Regular', Consolas, monospace;
                 background: #e8eaf6; padding: 1px 5px; border-radius: 3px;
                 font-size: 0.85em; }
  .file-path   { font-family: 'SFMono-Regular', Consolas, monospace;
                 font-size: 0.85em; color: #283593; }
  .deadline    { background: #fff3e0; border-left: 4px solid #f57c00;
                 padding: 10px 14px; margin: 8px 0; border-radius: 0 6px 6px 0; }
  .deadline strong { color: #e65100; }
  .empty  { color: #888; font-style: italic; }
  hr      { border: none; border-top: 1px solid #e0e0e0; margin: 28px 0; }
  .footer { font-size: 0.8em; color: #757575; line-height: 1.6; }
  .footer a { color: #1565c0; }
  .btn    { display: inline-block; background: #1a237e; color: #fff !important;
            padding: 8px 18px; border-radius: 4px; text-decoration: none;
            font-size: 0.85em; margin-top: 6px; }
"""


def file_list_html(paths, label):
    if not paths:
        return f'<p class="empty">No {label.lower()} this week.</p>'
    items = "".join(
        f'<li><span class="file-path">{p}</span></li>' for p in paths
    )
    return f"<ul>{items}</ul>"


def build_html(commits, new_files, modified_files, today_str):
    new_by_folder = classify_by_folder(new_files)
    mod_by_folder = classify_by_folder(modified_files)

    # ── Section 1: New Literature Added ──────────────────────────────────────
    lit_new = new_by_folder["literature"]
    lit_mod = mod_by_folder["literature"]
    lit_html = ""
    if lit_new:
        lit_html += "<strong>New files:</strong>" + file_list_html(lit_new, "literature files")
    if lit_mod:
        lit_html += "<strong>Updated files:</strong>" + file_list_html(lit_mod, "updates")
    if not lit_new and not lit_mod:
        lit_html = '<p class="empty">No literature changes this week.</p>'

    # ── Section 2: Regulatory Updates ────────────────────────────────────────
    reg_new = new_by_folder["regulations"]
    reg_mod = mod_by_folder["regulations"]
    reg_html = ""
    if reg_new:
        reg_html += "<strong>New files:</strong>" + file_list_html(reg_new, "regulatory files")
    if reg_mod:
        reg_html += "<strong>Updated files:</strong>" + file_list_html(reg_mod, "updates")
    if not reg_new and not reg_mod:
        reg_html = '<p class="empty">No regulatory updates this week.</p>'

    # ── Section 3: News Digest ────────────────────────────────────────────────
    news_new = new_by_folder["news"]
    news_mod = mod_by_folder["news"]
    news_html = ""
    if news_new or news_mod:
        all_news = news_new + news_mod
        news_html = file_list_html(all_news, "news items")
    else:
        news_html = '<p class="empty">No news digest updates this week. Visit the <a href="' + SITE_URL + 'news/digest/">News Digest page</a> for the latest items.</p>'

    # ── Section 4: Upcoming Deadlines ────────────────────────────────────────
    deadlines_html = ""
    for d in HARDCODED_DEADLINES:
        deadlines_html += (
            f'<div class="deadline">'
            f'<strong>{d["date"]} — {d["title"]}</strong><br>'
            f'{d["detail"]}'
            f'</div>'
        )

    # ── Commit log ────────────────────────────────────────────────────────────
    if commits:
        commit_items = "".join(
            f'<li><a href="{REPO_URL}/commit/{sha}" class="commit-hash">{sha}</a> {subj}</li>'
            for sha, subj in commits
        )
        commit_html = f"<ul>{commit_items}</ul>"
    else:
        commit_html = '<p class="empty">No commits in the past 7 days.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>JV &amp; Energy Trilemma Weekly Digest — {today_str}</title>
  <style>{CSS}</style>
</head>
<body>

<h1>JV &amp; Energy Trilemma — Weekly Digest</h1>
<p class="meta">
  {today_str} &nbsp;|&nbsp;
  <a href="{REPO_URL}">{REPO_URL}</a>
</p>

<h2>📚 New Literature Added</h2>
{lit_html}

<h2>⚖️ Regulatory Updates</h2>
{reg_html}

<h2>📰 News Digest</h2>
{news_html}

<h2>⏰ Upcoming Deadlines</h2>
{deadlines_html}

<h2>🔀 All Commits This Week</h2>
{commit_html}

<hr>
<a class="btn" href="{SITE_URL}">View Research Site →</a>

<hr>
<div class="footer">
  <p>
    This digest is sent on behalf of <strong>{RESEARCHER_NAME}</strong>,
    PhD researcher at <strong>{INSTITUTION}</strong>.<br>
    Research site: <a href="{SITE_URL}">{SITE_URL}</a>
  </p>
  <p>
    <strong>To unsubscribe:</strong> reply to this email or contact the researcher directly
    to be removed from the <code>DIGEST_RECIPIENTS</code> list.
    You can also view the
    <a href="{SITE_URL}subscribe/">subscription page</a>
    for details.
  </p>
</div>

</body>
</html>"""


def build_plain(commits, new_files, modified_files, today_str):
    lines = [
        f"JV & Energy Trilemma — Weekly Digest",
        f"{today_str}",
        f"Repository: {REPO_URL}",
        "",
        "=" * 60,
        "NEW LITERATURE ADDED",
        "=" * 60,
    ]
    if new_files:
        lines += [f"  NEW: {f}" for f in new_files if f.startswith("literature")]
    if modified_files:
        lines += [f"  MOD: {f}" for f in modified_files if f.startswith("literature")]
    if not any(f.startswith("literature") for f in new_files + modified_files):
        lines.append("  No literature changes this week.")

    lines += [
        "",
        "=" * 60,
        "REGULATORY UPDATES",
        "=" * 60,
    ]
    if any(f.startswith("regulations") for f in new_files + modified_files):
        lines += [f"  NEW: {f}" for f in new_files if f.startswith("regulations")]
        lines += [f"  MOD: {f}" for f in modified_files if f.startswith("regulations")]
    else:
        lines.append("  No regulatory updates this week.")

    lines += [
        "",
        "=" * 60,
        "NEWS DIGEST",
        "=" * 60,
    ]
    if any(f.startswith("news") for f in new_files + modified_files):
        lines += [f"  {f}" for f in new_files + modified_files if f.startswith("news")]
    else:
        lines.append(f"  No updates this week. Visit: {SITE_URL}news/digest/")

    lines += [
        "",
        "=" * 60,
        "UPCOMING DEADLINES",
        "=" * 60,
    ]
    for d in HARDCODED_DEADLINES:
        lines.append(f"  {d['date']} — {d['title']}")
        lines.append(f"  {d['detail']}")

    lines += [
        "",
        "=" * 60,
        f"ALL COMMITS ({len(commits)} total)",
        "=" * 60,
    ]
    if commits:
        lines += [f"  {sha} {subj}" for sha, subj in commits]
    else:
        lines.append("  No commits this week.")

    lines += [
        "",
        "-" * 60,
        f"Sent on behalf of {RESEARCHER_NAME} ({INSTITUTION}).",
        f"Research site: {SITE_URL}",
        "To unsubscribe: reply to this email or contact the researcher",
        "to be removed from the DIGEST_RECIPIENTS list.",
        "-" * 60,
    ]
    return "\n".join(lines)


# ── send ──────────────────────────────────────────────────────────────────────

def send_email(subject, html_body, plain_body, recipients):
    if not GMAIL_USER:
        print("ERROR: GMAIL_USER is not set.", file=sys.stderr)
        sys.exit(1)
    if not GMAIL_APP_PASSWORD:
        print("ERROR: GMAIL_APP_PASSWORD is not set.", file=sys.stderr)
        sys.exit(1)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{RESEARCHER_NAME} <{GMAIL_USER}>"
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    print(f"Connecting to smtp.gmail.com:587 as {GMAIL_USER}…")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, recipients, msg.as_string())

    print(f"Email sent to: {', '.join(recipients)}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    today_str = datetime.now(timezone.utc).strftime("%-d %B %Y")
    subject = f"JV & Energy Trilemma Weekly Digest — {today_str}"

    print("Collecting repository activity for the past 7 days…")
    commits = commits_since_7_days()
    new_files, modified_files = changed_files_since_7_days()
    print(f"  {len(commits)} commit(s), {len(new_files)} new file(s), "
          f"{len(modified_files)} modified file(s).")

    html_body = build_html(commits, new_files, modified_files, today_str)
    plain_body = build_plain(commits, new_files, modified_files, today_str)

    recipients = [r.strip() for r in RECIPIENTS_RAW.split(",") if r.strip()]
    if not recipients:
        print("WARNING: DIGEST_RECIPIENTS is empty — printing digest to log instead.")
        print("\n" + plain_body)
        return

    send_email(subject, html_body, plain_body, recipients)


if __name__ == "__main__":
    main()

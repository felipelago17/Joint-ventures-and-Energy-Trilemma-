#!/usr/bin/env python3
"""
Weekly email digest — collect last 7 days of repo activity and send via SendGrid.
Reads SENDGRID_API_KEY and SUBSCRIBERS from environment (GitHub Actions secrets).
Optionally reads SENDER_EMAIL from environment (repository variable).
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

try:
    import markdown as md_lib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])
    import markdown as md_lib


# ── configuration ────────────────────────────────────────────────────────────

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SUBSCRIBERS_RAW = os.environ.get("SUBSCRIBERS", "")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "noreply@example.com")
SENDER_NAME = "PhD Research Digest"
REPO_URL = "https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-"
SITE_URL = "https://felipelago17.github.io/Joint-ventures-and-Energy-Trilemma-/"


# ── git helpers ───────────────────────────────────────────────────────────────

def git(*args):
    result = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return result.stdout.strip()


def get_commits_since_7_days():
    """Return list of (hash, subject) tuples for the past 7 days."""
    raw = git("log", "--since=7 days ago", "--oneline", "--no-merges")
    if not raw:
        return []
    commits = []
    for line in raw.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            commits.append((parts[0], parts[1]))
    return commits


def get_changed_files_since_7_days():
    """Return list of changed file paths for the past 7 days."""
    raw = git("log", "--since=7 days ago", "--name-only", "--pretty=format:", "--no-merges")
    files = sorted({f for f in raw.splitlines() if f.strip()})
    return files


def categorise_files(files):
    """Group files by top-level folder."""
    categories = {}
    for f in files:
        top = f.split("/")[0] if "/" in f else "(root)"
        categories.setdefault(top, []).append(f)
    return categories


# ── digest builder ────────────────────────────────────────────────────────────

def build_markdown_digest(commits, categories):
    today = datetime.now(timezone.utc).strftime("%d %B %Y")
    lines = [
        f"# PhD Research Weekly Digest — {today}",
        "",
        f"**Repository:** [{REPO_URL}]({REPO_URL})",
        f"**Research site:** [{SITE_URL}]({SITE_URL})",
        "",
        "---",
        "",
    ]

    # commits section
    lines += [f"## Commits in the past 7 days ({len(commits)} total)", ""]
    if commits:
        for sha, subject in commits:
            lines.append(f"- [`{sha}`]({REPO_URL}/commit/{sha}) {subject}")
    else:
        lines.append("_No commits in the past 7 days._")
    lines.append("")

    # changed files section
    total_files = sum(len(v) for v in categories.values())
    lines += [f"## Changed files ({total_files} total)", ""]
    if categories:
        for folder in sorted(categories):
            lines.append(f"**`{folder}/`**")
            for f in sorted(categories[folder]):
                lines.append(f"- `{f}`")
            lines.append("")
    else:
        lines.append("_No file changes in the past 7 days._")
        lines.append("")

    # research areas quick-links
    lines += [
        "## Research areas",
        "",
        "| Area | Link |",
        "|------|------|",
        f"| JV Governance literature | [{SITE_URL}literature/jv-governance/]({SITE_URL}literature/jv-governance/) |",
        f"| Energy Trilemma literature | [{SITE_URL}literature/energy-trilemma/]({SITE_URL}literature/energy-trilemma/) |",
        f"| Norway Upstream | [{SITE_URL}literature/norway-upstream/]({SITE_URL}literature/norway-upstream/) |",
        f"| UAE Upstream | [{SITE_URL}literature/uae-upstream/]({SITE_URL}literature/uae-upstream/) |",
        f"| JV Contribution | [{SITE_URL}literature/jv-contribution/]({SITE_URL}literature/jv-contribution/) |",
        f"| Bibliography | [{SITE_URL}literature/bibliography/]({SITE_URL}literature/bibliography/) |",
        f"| News Digest | [{SITE_URL}news/digest/]({SITE_URL}news/digest/) |",
        "",
        "---",
        "",
        "_You are receiving this digest because you subscribed to weekly updates for this PhD research repository. "
        "To unsubscribe, ask the repository owner to remove your address from the `SUBSCRIBERS` secret._",
    ]

    return "\n".join(lines)


def markdown_to_html(md_text, subject):
    body_html = md_lib.markdown(md_text, extensions=["tables", "fenced_code"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           max-width: 680px; margin: 40px auto; padding: 0 20px;
           color: #24292e; line-height: 1.6; }}
    h1   {{ color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 8px; }}
    h2   {{ color: #283593; margin-top: 32px; }}
    a    {{ color: #0288d1; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ background: #f5f5f5; padding: 2px 5px; border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, monospace; font-size: 0.9em; }}
    pre  {{ background: #f5f5f5; padding: 16px; border-radius: 6px; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
    th   {{ background: #e8eaf6; }}
    hr   {{ border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }}
    p:last-child {{ font-size: 0.85em; color: #757575; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>"""


# ── sendgrid sender ───────────────────────────────────────────────────────────

def send_via_sendgrid(subject, html_body, plain_body, recipients):
    if not SENDGRID_API_KEY:
        print("ERROR: SENDGRID_API_KEY is not set — aborting send.", file=sys.stderr)
        sys.exit(1)

    personalizations = [{"to": [{"email": r.strip()}]} for r in recipients if r.strip()]
    if not personalizations:
        print("No valid recipients found — skipping send.")
        return

    payload = {
        "personalizations": personalizations,
        "from": {"email": SENDER_EMAIL, "name": SENDER_NAME},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": plain_body},
            {"type": "text/html", "value": html_body},
        ],
    }

    resp = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=30,
    )

    if resp.status_code in (200, 202):
        print(f"Email sent successfully to {len(personalizations)} recipient(s). "
              f"Status: {resp.status_code}")
    else:
        print(f"ERROR: SendGrid returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print("Collecting repository activity for the past 7 days…")
    commits = get_commits_since_7_days()
    changed = get_changed_files_since_7_days()
    categories = categorise_files(changed)

    print(f"  Found {len(commits)} commit(s), {len(changed)} changed file(s).")

    digest_md = build_markdown_digest(commits, categories)
    today = datetime.now(timezone.utc).strftime("%d %B %Y")
    subject = f"[PhD Digest] Joint Ventures & Energy Trilemma — {today}"

    html_body = markdown_to_html(digest_md, subject)
    plain_body = digest_md  # plain-text fallback

    recipients = [r.strip() for r in SUBSCRIBERS_RAW.split(",") if r.strip()]
    if not recipients:
        print("WARNING: SUBSCRIBERS secret is empty — no email will be sent.")
        print("Digest content:\n")
        print(digest_md)
        return

    print(f"Sending digest to: {', '.join(recipients)}")
    send_via_sendgrid(subject, html_body, plain_body, recipients)


if __name__ == "__main__":
    main()

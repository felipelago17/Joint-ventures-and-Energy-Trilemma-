# Subscribe to the Weekly Digest

The **JV & Energy Trilemma Weekly Digest** is a Monday-morning email summarising the past week's activity in this PhD research repository — new literature added, regulatory updates, news items, and upcoming deadlines.

## Who can subscribe?

The digest is intended for:

- PhD supervisors and academic advisors at LSBU
- Research colleagues working on joint-venture governance or the energy trilemma
- Industry contacts following the Norway / UAE comparative study

## How to request access

Send an email to **Felipe Villasuso Lago** at the address on your institutional contact sheet (or reply to any previous digest you have received) with the subject line:

> **Subscribe — JV & Energy Trilemma Digest**

Include your preferred email address and your affiliation. You will be added to the next week's send.

## What the digest contains

Each Monday at 08:00 UTC the workflow collects:

| Section | Content |
|---------|---------|
| **New Literature Added** | Files added to `literature/by-theme/` during the past 7 days |
| **Regulatory Updates** | Changes to `regulations/norway/`, `regulations/uae/`, `regulations/international/` |
| **News Digest** | Updates to `news/digest.md` (auto-scraped from NPD, ADNOC, IEA, WEC) |
| **Upcoming Deadlines** | Fixed reminders (e.g., BIS Affiliates Rule snap-back, 10 November 2026) |
| **All Commits** | Full commit log with links for the past 7 days |

## Unsubscribe

Reply to any digest email with the subject line:

> **Unsubscribe — JV & Energy Trilemma Digest**

You will be removed before the next send. No automated unsubscribe link is provided; the list is managed manually via the `DIGEST_RECIPIENTS` repository secret.

## Technical notes (for supervisors)

The digest is sent via Gmail SMTP (no third-party email service). The workflow source is at
[`.github/workflows/weekly-digest.yml`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/.github/workflows/weekly-digest.yml)
and the Python script at
[`.github/scripts/send_digest_email.py`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/.github/scripts/send_digest_email.py).
It uses only Python standard-library modules (`smtplib`, `email.mime`) — no external dependencies.

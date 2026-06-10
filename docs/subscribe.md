# Subscribe to the Daily Digest

The **JV & Energy Trilemma Daily Digest** is a daily email summarising the past 24 hours of activity in this PhD research repository — new literature added, regulatory updates, news items, and upcoming deadlines.

---

## Subscribe

Click the button below to open a pre-filled subscription email:

<p style="text-align:center; margin: 2rem 0;">
  <a href="mailto:felchagas@gmail.com?subject=Subscribe%20%E2%80%94%20JV%20%26%20Energy%20Trilemma%20Digest&body=Please%20add%20me%20to%20the%20daily%20digest.%0A%0AName%3A%20%0AEmail%3A%20%0AAffiliation%3A%20"
     style="background-color:#1565c0; color:#ffffff; padding:14px 32px; border-radius:6px; text-decoration:none; font-size:1.1rem; font-weight:bold; display:inline-block;">
    ✉ Subscribe to the Digest
  </a>
</p>

Or send an email manually to **felchagas@gmail.com** with:

- **Subject:** `Subscribe — JV & Energy Trilemma Digest`
- **Body:** your name, preferred email address, and affiliation

You will be added before the next send.

---

## Who can subscribe?

The digest is intended for:

- PhD supervisors and academic advisors at LSBU
- Research colleagues working on joint-venture governance or the energy trilemma
- Industry contacts following the Norway / UAE comparative study

---

## What the digest contains

Each day at 08:00 UTC the workflow collects:

| Section | Content |
|---------|---------|
| **New Literature Added** | Files added to `literature/by-theme/` in the past 24 hours |
| **Regulatory Updates** | Changes to `regulations/norway/`, `regulations/uae/`, `regulations/international/` |
| **News Digest** | Updates to `news/digest.md` (auto-scraped from Sodir, ADNOC, EIA, WEC) |
| **Upcoming Deadlines** | Fixed reminders (e.g., BIS Affiliates Rule snap-back, 10 November 2026) |
| **All Commits** | Full commit log with links for the past 24 hours |

---

## Unsubscribe

<p style="text-align:center; margin: 2rem 0;">
  <a href="mailto:felchagas@gmail.com?subject=Unsubscribe%20%E2%80%94%20JV%20%26%20Energy%20Trilemma%20Digest&body=Please%20remove%20me%20from%20the%20digest."
     style="background-color:#b71c1c; color:#ffffff; padding:10px 24px; border-radius:6px; text-decoration:none; font-size:1rem; font-weight:bold; display:inline-block;">
    Unsubscribe
  </a>
</p>

The list is managed manually via the `DIGEST_RECIPIENTS` repository secret.

---

## Technical notes (for supervisors)

The digest is sent via Gmail SMTP (no third-party email service). The workflow source is at
[`.github/workflows/weekly-digest.yml`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/.github/workflows/weekly-digest.yml)
and the Python script at
[`.github/scripts/send_digest_email.py`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/.github/scripts/send_digest_email.py).
It uses only Python standard-library modules (`smtplib`, `email.mime`) — no external dependencies.

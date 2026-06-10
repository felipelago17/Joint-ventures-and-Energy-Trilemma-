# Subscribe to the Daily Digest

The **JV & Energy Trilemma Daily Digest** is sent every morning at 08:00 UTC with the past 24 hours of activity — new literature, regulatory updates, news, and upcoming deadlines.

---

## Subscribe instantly

<p style="text-align:center; margin: 2rem 0;">
  <a href="https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/issues/new?template=subscribe.yml"
     target="_blank"
     style="background-color:#1565c0; color:#ffffff; padding:16px 40px; border-radius:6px; text-decoration:none; font-size:1.15rem; font-weight:bold; display:inline-block;">
    ✉ Subscribe — fill in your email
  </a>
</p>

**How it works:**

1. Click the button above
2. Fill in your name, email, and affiliation (takes 30 seconds)
3. Click **Submit new issue**
4. You're automatically added — no further action needed

> A GitHub account is required. If you don't have one, [sign up free](https://github.com/signup) or use the [manual request](#no-github-account) option below.

---

## Unsubscribe

<p style="text-align:center; margin: 1.5rem 0;">
  <a href="https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/issues/new?template=unsubscribe.yml"
     target="_blank"
     style="background-color:#b71c1c; color:#ffffff; padding:12px 28px; border-radius:6px; text-decoration:none; font-size:1rem; font-weight:bold; display:inline-block;">
    Unsubscribe
  </a>
</p>

You will be removed before the next send.

---

## No GitHub account?

Send an email to **felchagas@gmail.com** with:

- **Subject:** `Subscribe — JV & Energy Trilemma Digest`
- **Body:** your name, preferred email address, and affiliation

<p style="text-align:center; margin: 1rem 0;">
  <a href="mailto:felchagas@gmail.com?subject=Subscribe%20%E2%80%94%20JV%20%26%20Energy%20Trilemma%20Digest&body=Please%20add%20me%20to%20the%20daily%20digest.%0A%0AName%3A%20%0AEmail%3A%20%0AAffiliation%3A%20"
     style="background-color:#455a64; color:#ffffff; padding:10px 24px; border-radius:6px; text-decoration:none; font-size:0.95rem; font-weight:bold; display:inline-block;">
    Send subscription email
  </a>
</p>

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

## Technical notes (for supervisors)

The digest is sent via Gmail SMTP. Subscriptions submitted via the button above are processed automatically by a GitHub Actions workflow and stored in [`data/subscribers.txt`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/data/subscribers.txt). The workflow source is at [`.github/workflows/handle-subscription.yml`](https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-/blob/main/.github/workflows/handle-subscription.yml).

# [BETA] Intel Requirement Daily Brief - Install Guide

> **What you get:** A daily email summarising your top Intel Requirement matches from ThreatConnect — plain-language reasons, direct deep-links back into TC, and highlighted actors, CVEs, and countries.
>
> **Setup time:** ~10 minutes. Only 2 fields are mandatory.

---

## Before you start

Make sure you have all three:

- [ ] ThreatConnect dedicated cloud, v8.0+, with AI capabilities enabled
- [ ] At least one **active** Intelligence Requirement in your TC instance
- [ ] Email address(es) ready — one for the brief, one for errors

---

## Step 1 — Import the playbook

1. Go to **Automation & Feeds → Playbooks**
2. Click **Import Playbook → Import Playbook** (top right)

   <img width="300" height="220" alt="image" src="https://github.com/user-attachments/assets/089bdac7-bbc8-4f24-9b2d-824b1a67566c" />

3. Upload `(BETA) Active Intel Requirement Brief - Daily.pbxz`
4. Wait for the canvas to load — **this can take 1–2 minutes**

✅ Done when you can see the playbook design canvas.

---

## Step 2 — Set your email addresses `REQUIRED`

Open the **⚙️ SETTINGS - CHANGE ME** step on the canvas.

<img width="550" height="300" alt="image" src="https://github.com/user-attachments/assets/0fdfd153-12f4-449d-b5e1-3c8818149be4" />

| Variable | What to enter |
|---|---|
| `recipients` | Where the daily brief gets sent (comma-separate multiple addresses) |
| `failure_recipients` | Where errors get sent — usually your admin |

Click **Save.**

> 💡 **These are the only two fields you must configure.** Steps 3 and 4 are optional — skip straight to Step 5 if you don't need to customise further.

---

## Step 3 — Adjust lookback window and card volume `OPTIONAL`

| Variable | Default | What it does |
|---|---|---|
| `time_window_hours` | `24` | How far back to look for matches. Set to `48` for a 2-day lookback. |
| `max_reports` | `7` | Max cards per brief. Keep at 7 or below — higher values risk timeout errors. |

---

## Step 4 — Change the send schedule `OPTIONAL`

Click the green **Active IR Findings Brief Trigger** node.

**Default: Daily at 08:00 UTC** — that's ~09:00 BST, and overnight delivery for US East and West coasts.

| Mode | When to use it |
|---|---|
| **Daily** | Default — same time every day |
| **Weekly** | Specific days only (e.g. Mon/Wed/Fri) |
| **Monthly** | A specific date each month (e.g. the 1st) |
| **Advanced** | Custom cron — every weekday, every 6 hours, etc. |

[Full Timer Trigger docs →](https://knowledge.threatconnect.com/docs/playbooks-the-timer-trigger)

---

## Step 5 — Run a test

1. Toggle the playbook to **Active** mode (top right)

   <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/3b006803-1cac-411c-9123-10836b9eb39b" />

2. Click the **▶ play button** under the green Timer Trigger → run any profile

   <img width="354" height="374" alt="image" src="https://github.com/user-attachments/assets/073b6e81-246d-4862-b258-f431fe6c512e" />

   > No play button? Contact your Customer Success team to enable it.

3. Watch the execution run to completion
4. Check your inbox — subject line will read:
   `Threat Intelligence Brief — <Date> — N priorities`
5. Open the email and check the cards render correctly — titles should be clickable, with summaries and links back to ThreatConnect

   <img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/5e7c6ad6-4ef6-41d6-a2d2-29ecf6ec5a7b" />

---

## ✅ You're set up

The brief will now run automatically on schedule. Nothing else to do.

---

## BETA limitations

- **7 cards maximum per brief** — top 7 by TC score. The cap exists to avoid gateway timeouts; raising it risks occasional 3-minute failures
- **CVE detection** runs across both article titles and body text — surfaces as styled badges on each card
- **Inactive IRs are filtered out** automatically — only active IRs generate cards
- **Custom header images** are not available in BETA

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Execution times out at ~3 min | IR has very large keyword lists (50+ per section) | Tighten IR keyword coverage; or reduce context size by trimming descriptions |
| Run completes but no email arrives | Typo in `recipients` or `failure_recipients` | Recheck both values character-by-character |
| Email arrives but cards look wrong (broken HTML, missing dates) | Output token limit reached | Increase output token limit, or lower `max_reports` |
| Empty brief — "no priorities" | No IR results in the lookback window, or all matching IRs are inactive | Confirm at least one IR is active and has recent matches via CAL / Dataminr feeds |

---

## Feedback

This is a BETA release — send bugs, requests, and observations to the Dataminr product team. Most useful right now:

- **Volume:** customers who need more than 7 priorities per brief
- **Cadence:** non-standard schedules beyond Daily/Weekly/Monthly
- **Content:** cards with too much detail, too little, or wrong emphasis
- **Rendering:** any display issues in Outlook, Apple Mail, or Gmail
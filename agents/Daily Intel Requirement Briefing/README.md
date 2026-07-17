# [BETA] Intel Requirement Daily Brief - Install Guide

---

## What it does

* Curates latest, closest-matching Intel Requirement results into a priority list of result to review
* Plain-language reason as to why it maps to your IRs
* Direct link back into ThreatConnect for further review
* Highlighting of actors, cves, victims and countries involved

## Prerequisites

- ThreatConnect dedicated cloud environment with AI capabilities enabled, version 8.0+
- TC instance with at least one **active** Intelligence Requirement
- Desired recipient email address(es) for both success and failure notifications

---

## Step 1 — Import the playbook

1. Navigate to **Automation & Feeds → Playbooks**.
2. Click **Import Playbook → Import Playbook** (top right).

   <img width="300" height="220" alt="image" src="https://github.com/user-attachments/assets/089bdac7-bbc8-4f24-9b2d-824b1a67566c" />


3. Select `(BETA) Active Intel Requirement Brief - Daily.pbxz` to upload
4. Verify you can see the playbook design canvas after waiting for the upload to complete (it can take 1-2 minutes)

---

## Step 2 — Configure required scope variables

Open the **⚙️ SETTINGS - CHANGE ME** step near the start of the playbook canvas. Two variables are the bare minimum for any deployment:

| Variable | What to set | Notes |
|---|---|---|
| `recipients` | Comma-separated email addresses | The daily brief will be sent to this recipient(s) |
| `failure_recipients` | Comma-separated email addresses | Any errors with the execution will be sent to this email(s) - typically your admin |
<img width="550" height="300" alt="image" src="https://github.com/user-attachments/assets/0fdfd153-12f4-449d-b5e1-3c8818149be4" />


Click **Save**

`You can skip Step 3 and 4 if you don't want to customise further.`

## Step 3 — Configure optional scope variables (optional)

| Variable | What to set | Where it shows up |
|---|---|---|
| `time_window_hours` | Number of hours to look back for review | Defaults to 24 for a daily review. E.g would be 48 for a 2-day review. |
| `max_reports` | Number of maximum objects to return back in the email brief | Defaults to 7. Increasing this will increase Email length and potentially lead to failures due to LLM context sizes. |

## Step 4 — Adjust the Timer trigger schedule (optional)

Click on the green **Active IR Findings Brief Trigger** node.

Default schedule: **Daily at 08:00 UTC**. That covers UK morning briefings (~09:00 BST) and overnight delivery for US East and West coasts.

The TC UI exposes four scheduling modes:

| Schedule | Use when |
|---|---|
| **Daily** | What this Agent uses - generates the same time every day |
| **Weekly** | Wanting the brief only on specific days (e.g., Mon/Wed/Fri). Multi-select day checkboxes. |
| **Monthly** | Wanting a periodic digest on a specific day-of-month (e.g., the 1st). |
| **Advanced** | Raw Quartz cron field for anything the dropdown can't express (every weekday, every 6 hours, etc.). |

You can read more about the Timer Trigger configuration in depth [here](https://knowledge.threatconnect.com/docs/playbooks-the-timer-trigger).

## Step 5 — Run a test

1. At the top right of the Playbook designer page, change the playbook to **Active** mode
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/3b006803-1cac-411c-9123-10836b9eb39b" />

2. Click the play button under the green **Timer Trigger** and run any profile (create one if none available). `If no play button is present, reach out to your Customer Success team to enable it`
<img width="354" height="374" alt="image" src="https://github.com/user-attachments/assets/073b6e81-246d-4862-b258-f431fe6c512e" />

3. Watch the execution and wait for it to finish
4. Verify the email arrives in the configured recipient inboxes. Subject line will read:

   `Threat Intelligence Brief — <Date> — N priorities`

6. Open the email and skim the cards. You should see clickable titles and clickable links back to ThreatConnect, as well as a short write-up (exmaple below)
<img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/5e7c6ad6-4ef6-41d6-a2d2-29ecf6ec5a7b" />



**If the run completes but no email arrives:** 

validate that the email address is correct, and check the playbook execution steps if it exited early

**If the run fails or times out:** see [**Troubleshooting**](##Troubleshooting) below.

---

## BETA limitations

- **Defaults to a maximum 7 of priorities per brief.** If a busy day produces more than 7 matches, the top 7 by TC score show in the brief. The lower-ranked ones aren't surfaced in this version. (Cap was set with headroom for LLM-step variance — pushing higher caused occasional 3-minute gateway timeouts. See Troubleshooting if you see this on a deployment.)
- **CVE detection works on article titles AND article bodies.** Both surface as styled badges in the email; the most relevant CVE per brief becomes a badge highlighting that particular CVE at the top
- **Inactive IRs are filtered out**
- **Custom header images are disabled in BETA.** 

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Run times out at ~3 minutes | IR has unusually large  keyword lists (50+ keywords per IR section), inflating the LLM payload | Review the heaviest IRs; potentially tightening keyword coverage where possible. If keywords are necessary we can reduce context size by trimming down descriptions |
| Run completes but no email arrives | Typo in `recipients` or `failure_recipients`; address bounced silently | Recheck both variables character-by-character |
| Email arrives but card content looks wrong (missing dates, broken HTML) | Output token limit reached | See if output token limit can be increased, or reduce context being reviewed |
| Empty brief ("no priorities") | Either no IR results in the last 24 hours, or all matched IRs are inactive | Check that the instance has active IRs and that some have recent matches via CAL / Dataminr feeds |

---

## Feedback

This is a BETA release. Send feedback, bug reports, and feature requests to the Dataminr product team. Specifically interested in:

- Which customers want more than 7 priorities per brief (informs cap roadmap)
- Cadence patterns customers request beyond Daily/Weekly/Monthly
- Card content (too much detail, too little, wrong emphasis)
- Email rendering issues in specific clients (Outlook, Apple Mail, Gmail web)

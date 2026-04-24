# Boolean String Builder

A Claude Code agent skill that generates platform-ready Boolean search strings for recruiters.

Give it a role brief. Get back three copy-paste-ready search strings for LinkedIn Recruiter, Google X-ray, and GitHub. Works as a Claude Code skill locally, or as a remotely triggered routine via webhook.

---

## What it does

Building Boolean search strings is one of the most repetitive tasks in recruitment. A good string for a niche role can take 30-45 minutes to build properly across three platforms, each with different syntax.

This agent takes a role brief and does it in seconds.

**Input** (in `tools/role-brief.txt`):
- Role title
- Location
- Key skills and requirements
- Industry and seniority (optional)

**Output:**
- LinkedIn Recruiter string (ready to paste into LinkedIn Recruiter search)
- Google X-ray string (ready to paste into Google)
- GitHub string (for technical roles)

---

## How to run it

This is a Claude Code agent skill. You need [Claude Code](https://claude.ai/code) installed.

**1. Clone the repo**

```bash
git clone https://github.com/Richb2021/boolean-builder.git
cd boolean-builder
```

**2. Edit the role brief**

Open `tools/role-brief.txt` and fill in your mandate:

```
Role: Senior ERP Consultant
Location: Manchester, UK
Industry: Manufacturing
Experience: 7+ years
Skills: SAP S/4HANA, implementation, go-live, UAT, change management, RICE
Notes: Hybrid working, client-facing role
```

**3. Run with Claude Code**

```bash
claude
```

Claude reads `CLAUDE.md`, loads the skill from `SKILL.md`, and generates the strings. If notification channels are configured (see below), results are sent automatically. Otherwise they print to the terminal.

---

## Automated / remote use

The agent can be triggered remotely via webhook — push a role brief, get Boolean strings back by SMS or webhook within a minute.

**Setup:**

1. Fork this repo
2. Create a Claude Code Routine pointing at the repo (see [Routines docs](https://code.claude.com/docs/en/routines))
3. Set notification env vars in your cloud environment
4. Push an updated `tools/role-brief.txt` to trigger, or fire via the API trigger

**Notification channels** (set as environment variables):

| Channel | Variables needed |
|---------|-----------------|
| Twilio SMS | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `NOTIFY_TO_PHONE` |
| Webhook | `NOTIFY_WEBHOOK_URL` |
| Email (SMTP) | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `NOTIFY_TO_EMAIL` |

If no channels are configured the script exits with code 1 and results print to stdout.

---

## The strings it generates

**LinkedIn Recruiter** — built to LinkedIn Recruiter's Boolean syntax spec (AND/OR/NOT in capitals, quoted phrases, grouped alternatives, two OR groups maximum). LinkedIn Recruiter is a paid tool — if you've tested these strings and have feedback on how they perform, open an issue or leave a comment. Note: regular LinkedIn search does not support Boolean operators.

**Google X-ray** — uses `site:linkedin.com/in/` to surface public LinkedIn profiles via Google. Works without a LinkedIn subscription. Often finds candidates LinkedIn's own algorithm misses. Tested and confirmed working.

**GitHub** — keyword search with `followers:` and `location:` filters. Most useful for technical roles where candidates have an active GitHub presence. Tested and confirmed working.

**Stack Overflow** — Google X-ray on `stackoverflow.com/users` profiles. Shows demonstrated technical ability through real Q&A answers, not just claimed skills. Generated for technical roles only.

---

## Background

Built this after spending a lot of time with recruiters. One issue that keeps coming up: hours of manual work every week on Boolean string construction, following a completely predictable pattern. The WIRE Method — the framework behind this — starts by finding the highest Time Tax in a workflow and closing it first. Boolean string building is almost always in the top three for recruiters doing niche search.

---

## Licence

MIT. Use it, fork it, modify it. If you build something useful on top of it, share it back.

---

## Questions

Open an issue or connect on [LinkedIn](https://www.linkedin.com/in/richardbatt).

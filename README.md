# Boolean String Builder

Generate platform-ready Boolean search strings for recruiters. Works with any AI tool — no setup required.

---

## What it does

Building Boolean search strings is one of the most repetitive tasks in recruitment. A good string for a niche role can take 30-45 minutes to build properly across multiple platforms, each with different syntax.

This tool generates them in seconds. For each role it produces:

- **LinkedIn Recruiter string** — built to LinkedIn Recruiter's Boolean syntax spec
- **Google X-ray string** — surfaces public LinkedIn profiles via Google search
- **GitHub string** — for technical roles, finds candidates with active public repos
- **Stack Overflow string** — for technical roles, finds candidates with demonstrated technical engagement

Each string comes with a one-line rationale explaining the keyword strategy, so you know why it's built the way it is — not just what it says.

---

## How to use it

### Option 1 — AI desktop and CLI apps (recommended)

Works with Cowork, Claude Code, Codex App, Gemini CLI, OpenCode, ChatGPT desktop, or any other AI app that has access to a folder on your computer.

**Setup:**

1. Download the zip from GitHub (green Code button → Download ZIP)
2. Extract it to a folder anywhere on your computer
3. Open `tools/role-brief.txt` and fill in your mandate

Or if you prefer the command line: `git clone https://github.com/Richb2021/boolean-builder.git`

**Edit the role brief:**

Open `tools/role-brief.txt` and fill in your mandate:

```
Role: Senior Python Engineer
Location: Toronto, Canada
Industry: Fintech / SaaS
Experience: 5+ years
Skills: Python, FastAPI, Django, microservices, PostgreSQL, AWS, Docker
Notes: Series B company, hybrid working
```

**Run in your app:**

| App | What to do |
|-----|-----------|
| Claude Code / Cowork | Open the folder — reads `CLAUDE.md` automatically and runs |
| Codex CLI / OpenCode | Open the folder — reads `AGENTS.md` automatically and runs |
| ChatGPT desktop | Open the folder, ask it to read `AGENTS.md` and generate strings |
| Gemini CLI | Open the folder, ask it to read `SKILL.md` and generate strings |

The agent reads your role brief, generates all four strings with rationale, and prints results to the terminal. If notification channels are configured it can also send results by SMS or webhook — see below.

---

### Option 2 — Any AI chat tool (no desktop app)

If you don't have a compatible desktop app, the repo includes a copy-paste prompt that works with any chat interface.

1. Open [PROMPT.md](./PROMPT.md)
2. Copy the entire prompt
3. Paste into ChatGPT, Claude, Gemini, Copilot, or any other chat tool
4. Fill in the role details where marked and hit send

---

### Option 3 — Automated / webhook (results by SMS)

Point a Claude Code Routine at this repo. When triggered, it reads `tools/role-brief.txt`, generates the strings, and sends results by SMS or webhook within a minute.

**Notification channels** — add these as environment variables in your cloud environment:

| Channel | Variables needed |
|---------|-----------------|
| Twilio SMS | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `NOTIFY_TO_PHONE` |
| Webhook | `NOTIFY_WEBHOOK_URL` |
| Email (SMTP) | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `NOTIFY_TO_EMAIL` |

If no channels are configured, results print to the terminal and the script exits with code 1.

---

## The platforms

**LinkedIn Recruiter** — built to LinkedIn Recruiter's Boolean syntax spec (AND/OR/NOT in capitals, layered keyword structure, maximum two OR groups). LinkedIn Recruiter is the paid tool used by most recruitment firms doing volume hiring. Regular LinkedIn search does not support Boolean operators. If you test these strings and have feedback, open an issue.

**Google X-ray** — uses `site:linkedin.com/in/` to surface public LinkedIn profiles via Google. Works without any LinkedIn subscription. Tested and confirmed working.

**GitHub** — keyword search with `followers:>10` and `repos:>3` filters. Technical roles only. Tested and confirmed working.

**Stack Overflow** — Google X-ray on `stackoverflow.com/users` profiles with reputation filter. Shows candidates with demonstrated technical engagement. Technical roles only. Tested and confirmed working.

---

## How the strings are structured

Strings are built in layers — not flat keyword lists:

1. **Title group** — role title and synonyms (must-have)
2. **Core skill** — the single primary technology or discipline, mandatory AND
3. **Supporting skills** — frameworks, tools, alternatives (broad enough to avoid missing strong candidates)
4. **Location** — regional variations, or applied via UI filter

This layered structure is why the strings produce better recall than manually written Boolean without losing precision.

---

## Files

| File | Purpose |
|------|---------|
| `PROMPT.md` | Copy-paste prompt for any AI chat tool |
| `CLAUDE.md` | Agent instructions for Claude Code and Cowork |
| `AGENTS.md` | Agent instructions for Codex CLI and OpenCode |
| `SKILL.md` | Full platform rules, syntax reference, and examples |
| `tools/role-brief.txt` | Edit this with your mandate before running |
| `tools/notify.py` | Sends results by SMS, webhook, or email |

---

## Background

Built this after spending a lot of time with recruiters. One issue that keeps coming up: Boolean string construction taking 30-45 minutes per mandate, following a completely predictable pattern. The WIRE Method — the framework behind this — starts by finding the highest Time Tax in a workflow and closing it first. Boolean string building is almost always in the top three for recruiters doing niche search.

---

## Licence

MIT. Use it, fork it, modify it. If you build something useful on top of it, share it back.

---

## Questions

Open an issue or connect on [LinkedIn](https://www.linkedin.com/in/richardbatt).

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
3. Open the folder in your AI app
4. Provide the role brief — either type it directly, paste it in, or drop it into `tools/role-brief.txt`

Or if you prefer the command line: `git clone https://github.com/Richb2021/boolean-builder.git`

**Run in your app:**

| App | What to do |
|-----|-----------|
| Cowork / Claude Code | Open the folder — reads `CLAUDE.md` automatically |
| Codex App / OpenCode | Open the folder — reads `AGENTS.md` automatically |
| ChatGPT desktop | Open the folder, ask it to read `AGENTS.md` |
| Gemini CLI | Open the folder, ask it to read `SKILL.md` |

Provide the role title, location, and key skills. The agent generates all four strings with rationale and prints results. If notification channels are configured it sends results by SMS or webhook instead — see below.

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

## Quality and Learning System

Every string the agent generates is automatically validated and the results inform future runs.

### Validation

After generating strings, the agent runs `scripts/validate_boolean.py` — a deterministic Python validator that checks every string against platform-specific rules before output. Nothing leaves the agent with a hard validation failure.

**What it checks:**

| Platform | Checks |
|----------|--------|
| LinkedIn Recruiter | No site: operator, uppercase AND/OR/NOT, max 2 OR groups, under 500 chars, has AND connectors, min 4 title synonyms, core skill anchor present, no location in string |
| Google X-ray | Starts with site:linkedin.com/in/, has quoted phrases, has negative exclusions, not over-specified (max 4 OR groups), has location terms |
| GitHub | No site: operator, no OR groups in brackets, has in:bio/language:/followers:/repos: qualifiers |
| Stack Overflow | Starts with site:stackoverflow.com/users, has quoted terms, has reputation filter, has OR group for skills |

Run it manually against any strings:

```bash
python scripts/validate_boolean.py \
  --linkedin "your linkedin string" \
  --google "your google string" \
  --github "your github string" \
  --stackoverflow "your stackoverflow string"
```

Output includes a score per platform (0-100), hard errors that must be fixed, and warnings to review.

### Memory and Learning

The agent reads two files at session start to improve every run:

**`memory/patterns.json`** — structured learning store with:
- Global lessons (platform rules that have caused problems in production)
- Validated string patterns by role type (Python engineer, ERP consultant, etc.)
- Bad patterns to avoid, with the reason and the fix

**`memory/feedback.md`** — human-readable feedback log. After testing strings in production, add a GOOD/OK/BAD rating and a one-line lesson. The agent reads this each session and applies the findings.

Over time the pattern library builds up validated templates by role type — the 10th Python engineer brief produces better strings than the first.

### Files

| File | Purpose |
|------|---------|
| `PROMPT.md` | Copy-paste prompt for any AI chat tool |
| `CLAUDE.md` | Agent instructions for Claude Code and Cowork |
| `AGENTS.md` | Agent instructions for Codex CLI and OpenCode |
| `SKILL.md` | Full platform rules, syntax reference, and examples |
| `scripts/validate_boolean.py` | Deterministic quality validator — runs after every generation |
| `memory/patterns.json` | Learning store — global lessons and validated patterns by role type |
| `memory/feedback.md` | Production feedback log — add GOOD/BAD ratings here |
| `tools/role-brief.txt` | Optional: pre-load a role brief here |
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

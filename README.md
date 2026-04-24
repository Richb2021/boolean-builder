# Boolean String Builder

Generate platform-ready Boolean search strings for recruiters. Works with any AI tool.

---

## Three ways to use it

### 1. Any AI chat tool — no setup at all

Copy the prompt from [PROMPT.md](./PROMPT.md), paste into ChatGPT, Claude, Gemini, Copilot, or any other chat interface. Fill in the role. Hit send. Works anywhere, nothing to install.

### 2. AI desktop and CLI apps — clone and run

For apps that have file access and can run Python, clone the repo and point your app at it. Edit `tools/role-brief.txt` with your mandate, then run.

| App | How to use |
|-----|-----------|
| Claude Code / Cowork | Open the folder — reads `CLAUDE.md` automatically |
| Codex CLI / OpenCode | Open the folder — reads `AGENTS.md` automatically |
| ChatGPT desktop app | Open the folder and ask it to read `AGENTS.md` and generate strings |
| Gemini CLI | Open the folder and ask it to read `SKILL.md` and generate strings |

```bash
git clone https://github.com/Richb2021/boolean-builder.git
cd boolean-builder
# Edit tools/role-brief.txt with your role
# Open in your AI app and run
```

### 3. Automated / webhook — fire remotely, get results by SMS

Point a Claude Code Routine at this repo. Update `tools/role-brief.txt` and trigger via webhook. Results arrive by SMS or webhook within a minute. See [SKILL.md](./SKILL.md) for setup.

---

## What problem this solves

Building Boolean search strings is one of the most repetitive tasks in recruitment. A good string for a niche role can take 30-45 minutes to build properly across multiple platforms, each with different syntax.

This prompt does it in seconds.

---

## How to use it

1. Open [PROMPT.md](./PROMPT.md)
2. Copy the entire prompt
3. Paste it into your AI tool of choice
4. Fill in your role title, location, and key skills where marked
5. Hit send

That is it. Copy the strings it generates, paste into your search platform, run.

---

## The strings it generates

**LinkedIn Recruiter** — built to LinkedIn Recruiter's Boolean syntax spec. LinkedIn Recruiter is the paid tool used by most recruitment firms doing volume hiring. If you test these strings and have feedback, open an issue. Note: regular LinkedIn search does not support Boolean operators.

**Google X-ray** — uses `site:linkedin.com/in/` to surface public LinkedIn profiles via Google. Works without any LinkedIn subscription. Tested and confirmed working.

**GitHub** — keyword search with `followers:` filter. For technical roles only. Finds candidates with active public repositories. Tested and confirmed working.

**Stack Overflow** — Google X-ray on `stackoverflow.com/users` profiles. Shows demonstrated technical ability, not just claimed skills. For technical roles only. Tested and confirmed working.

---

## Advanced use — Claude Code agent

If you use Claude Code, the `SKILL.md` and `CLAUDE.md` files in this repo turn it into an automated agent. Point a Claude Code Routine at the repo, update `tools/role-brief.txt` with your mandate, and get results sent by SMS or webhook without opening a browser.

See [SKILL.md](./SKILL.md) for setup instructions.

---

## Background

Built this after spending a lot of time with recruiters. One issue that keeps coming up: Boolean string construction taking 30-45 minutes per mandate, following a completely predictable pattern. The WIRE Method — the framework behind this — starts by finding the highest Time Tax in a workflow and closing it first. Boolean string building is almost always in the top three for recruiters doing niche search.

---

## Licence

MIT. Use it, fork it, modify it. If you build something useful on top of it, share it back.

---

## Questions

Open an issue or connect on [LinkedIn](https://www.linkedin.com/in/richardbatt).

# Boolean String Builder

A free tool that generates platform-ready Boolean search strings for recruiters in seconds.

Give it a role brief. Get back three copy-paste-ready search strings for LinkedIn Recruiter, Google X-ray, and GitHub. No setup, no subscription, no interface to learn.

---

## What it does

Building Boolean search strings is one of the most repetitive tasks in recruitment. A good string for a niche role — say a BESS Project Manager in Ontario or a Senior ERP Consultant in the Midlands — can take 30-45 minutes to build properly across three platforms, each with slightly different syntax.

This tool takes a role brief and does it in seconds.

**Input:**
- Role title
- Location
- Key skills and requirements
- Industry (optional)
- Years of experience (optional)

**Output:**
- LinkedIn Recruiter string (ready to paste into LinkedIn search)
- Google X-ray string (ready to paste into Google)
- GitHub string (for technical roles)

---

## How to run it

You need Python 3 and an Anthropic API key. If you do not have one, get it free at [console.anthropic.com](https://console.anthropic.com) — the free tier is enough.

**1. Clone the repo**

```bash
git clone https://github.com/Richb2021/boolean-builder.git
cd boolean-builder
```

**2. Run it**

```bash
python boolean_builder.py
```

The browser opens automatically at `http://localhost:8080`.

**3. Enter your API key**

Paste your Anthropic API key into the field at the top of the page, or set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python boolean_builder.py
```

**4. Fill in the role brief and hit Generate**

---

## As an agent (run remotely via webhook)

The `boolean-builder-agent/` folder contains the same tool built as a Claude Code agent. This version runs on Anthropic's infrastructure, reads a `role-brief.txt` file, generates the strings, and sends results by SMS or webhook — no browser, no local server.

This is the pattern for running it as part of an automated recruitment workflow:

1. Push a `role-brief.txt` to the repo with the mandate details
2. Trigger fires automatically via GitHub webhook
3. Boolean strings arrive by SMS or webhook within a minute

See `boolean-builder-agent/SKILL.md` for full setup instructions.

---

## The strings it generates

**LinkedIn Recruiter** — uses standard Boolean syntax (AND/OR/NOT in capitals, quoted phrases, grouped alternatives). Built for LinkedIn Recruiter, the paid tool used by most recruitment firms doing volume hiring. Note: regular LinkedIn search does not support Boolean operators.

**Google X-ray** — uses `site:linkedin.com/in/` to search public LinkedIn profiles from Google. Useful when LinkedIn's own algorithm doesn't surface the candidates you need. Works on any Google account, no subscription required.

**GitHub** — keyword search with `in:bio` and `followers:` filters. Most useful for technical roles where candidates have an active GitHub presence.

---

## Background

Built this after spending time with a TA professional who had completed a $15,000 AI bootcamp and still had no working automations in his practice. The Boolean string problem kept coming up — hours of manual work every week, following a completely predictable pattern. Seemed like the right place to start.

The WIRE Method — the framework this is built around — is about finding the highest Time Tax in a workflow and closing it first. Boolean string building is almost always in the top three for recruiters doing niche search.

---

## Licence

MIT. Use it, fork it, modify it. If you build something useful on top of it, share it back.

---

## Questions

Open an issue or connect on [LinkedIn](https://www.linkedin.com/in/richardbatt).

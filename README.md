# Boolean String Builder Skill

An AI-agent skill that generates platform-ready candidate search strings for recruiters.

Give the agent a role brief. It returns copy-paste-ready sourcing strings for LinkedIn Recruiter, Google X-ray, and either GitHub user search or a second X-ray variant for non-technical roles. No separate app or UI is shipped in this repo.

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
- LinkedIn Recruiter string, ready to paste into the relevant Recruiter keyword/title field
- Google X-ray string, ready to paste into Google
- GitHub user-search string for technical roles, or an alternate Google X-ray string for non-technical roles
- The assumptions and title synonyms used to build the strings

---

## How to run it

This repository is a skill/instruction pack, not a standalone browser app.

**1. Clone the repo**

```bash
git clone https://github.com/Richb2021/boolean-builder.git
cd boolean-builder
```

**2. Use the skill**

In an agent environment that supports local skills, point the agent at `SKILL.md` and provide a role brief in the chat or in `tools/role-brief.txt`.

Example prompt:

```text
Use the boolean-builder skill for this mandate:

Role: Senior ERP Implementation Lead
Location: Midlands, UK
Industry: Manufacturing
Experience: 8+ years
Skills: SAP S/4HANA, change management, UAT, go-live, stakeholder management
```

**3. Optional notifications**

`tools/notify.py` can send generated strings by SMS, webhook, or email when the relevant environment variables are configured. If no channel is configured, the script exits non-zero so automation does not silently report success.

---

## As an automated agent

The skill can be used in an automated recruitment workflow:

1. Put the mandate details in `tools/role-brief.txt`
2. Trigger an agent run that reads `SKILL.md` and the brief
3. Return the generated strings in the session log, or call `tools/notify.py` if a delivery channel is configured

---

## The strings it generates

**LinkedIn Recruiter** — uses standard Boolean syntax (AND/OR/NOT in capitals, quoted phrases, grouped alternatives). Built for LinkedIn Recruiter and Recruiter Lite workflows, where recruitment firms can combine Boolean text with sourcing filters.

**Google X-ray** — uses `site:linkedin.com/in/` to search public LinkedIn profiles from Google. Useful when LinkedIn's own algorithm doesn't surface the candidates you need. Works on any Google account, no subscription required.

**GitHub** — user search using supported qualifiers such as `language:`, `location:`, `followers:`, `repos:`, and `type:user`. Most useful for technical roles where candidates have an active GitHub presence. For profile-bio/title terms, use a Google X-ray against `github.com` rather than unsupported GitHub bio syntax.

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

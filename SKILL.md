---
name: boolean-builder
description: |
  Recruitment Boolean String Generator. Takes a role brief and generates
  platform-ready Boolean search strings for LinkedIn Recruiter, Google X-ray,
  and GitHub user search. Handles niche technical and professional roles.
  Can send results via SMS, webhook, or email using notify.py when requested.
---

# Boolean String Builder

Specialist Boolean search string generator for talent acquisition professionals.

## Process

### Step 1: Parse the Role Brief

Extract these fields from the brief (use what you have, note gaps):

- **Role title** — what is the position called?
- **Location** — city, region, country, remote options?
- **Key skills** — technical and functional requirements
- **Seniority** — years of experience, level (senior/lead/manager)
- **Industry** — sector context that affects terminology

### Step 2: Build Title Synonyms

Before writing any string, list all realistic title variations for the role.
Recruiters and candidates use different terms. Examples:

| Role | Synonyms |
|------|----------|
| BESS Project Manager | "Battery Storage PM" "Energy Storage Manager" "BESS Delivery Lead" "Battery Project Lead" "ESS Project Manager" |
| ERP Implementation Lead | "ERP Consultant" "SAP Lead" "Systems Implementation Manager" "ERP Project Manager" "Enterprise Systems Lead" |
| Software Engineer | "Software Developer" "SWE" "Backend Engineer" "Full Stack Developer" "Application Developer" |
| Talent Acquisition | "Recruiter" "Talent Partner" "HR Business Partner" "People Operations" "Recruitment Manager" |
| Data Scientist | "ML Engineer" "Machine Learning Scientist" "Data Analyst" "AI Engineer" "Research Scientist" |

Always generate 4-6 title synonyms minimum. More for ambiguous roles.

### Step 3: Generate the Three Strings

#### LinkedIn Recruiter String

**Important:** This string is optimized for **LinkedIn Recruiter** and Recruiter Lite workflows. LinkedIn.com also supports standard Boolean searches, but Recruiter gives sourcing teams better candidate filters and saved-search workflows. Always clarify which tool the client is using.

**Syntax rules:**
- AND, OR, NOT must be uppercase
- Use quotes for multi-word phrases: "project manager"
- Group alternatives in parentheses: ("project manager" OR "delivery lead")
- LinkedIn supports title:, company:, school: operators
- Keep OR groups shallow and readable; use Recruiter filters for location, industry, seniority, and company constraints where possible
- Keep under 500 characters to be safe
- Do NOT use site: operator (that's Google)

**Template structure:**
```
("Title 1" OR "Title 2" OR "Title 3" OR "Title 4") AND ("Key Skill 1" OR "Key Skill 2" OR "Key Skill 3")
```

Add location as a third AND group only if needed — LinkedIn's location filter in the UI is often more reliable than Boolean location terms.

**Example (BESS PM, Ontario):**
```
("BESS Project Manager" OR "Battery Storage Project Manager" OR "ESS Project Manager" OR "Energy Storage Manager") AND ("BESS" OR "battery energy storage" OR "EPC" OR "grid interconnection" OR "commissioning")
```

#### Google X-ray String

**Syntax rules:**
- Must start with: site:linkedin.com/in/
- Use quotes for phrases
- Use - to exclude: -"job title you want to exclude"
- AND is implied by default; use OR explicitly
- Include intitle: for profile headline matches
- Aim for 3-5 key terms — too many and Google returns nothing

**Template structure:**
```
site:linkedin.com/in/ ("Title 1" OR "Title 2") ("Skill 1" OR "Skill 2") "Location"
```

**Example (BESS PM, Ontario):**
```
site:linkedin.com/in/ ("BESS Project Manager" OR "Battery Storage" OR "Energy Storage") ("project manager" OR "delivery lead" OR "programme manager") ("Ontario" OR "Toronto" OR "Canada")
```

#### GitHub String

**Important:** GitHub search is only productive for technical roles — developers, data scientists, ML engineers, DevOps, platform engineers, security engineers. For non-technical roles, produce a second Google X-ray variant instead.

**Syntax rules:**
- Use GitHub user-search qualifiers that GitHub documents for people search
- `type:user` — excludes organizations
- `followers:>N` — filters for accounts with some community signal
- `repos:>N` — filters for accounts with public repository activity
- `location:"City"` — location filter (not always populated by users)
- `language:Python` — users whose repositories are mostly in that language
- `in:name` — searches the user's real name field; GitHub does not document `in:bio`
- Avoid OR groups and long keyword lists; GitHub user search is weaker than LinkedIn/Google for role-title matching
- For profile bio/headline terms, use Google X-ray against GitHub profiles

**Template structure (technical roles):**
```
language:Python location:"City" followers:>10 repos:>3 type:user
```

**Template structure (non-technical roles — second Google X-ray instead):**
```
site:linkedin.com/in/ ("role title" OR "alternate title") ("key skill") ("location") -recruiter
```

**Example (AI Consultant — technical adjacent):**
```
language:Python location:"United Kingdom" followers:>10 repos:>3 type:user
```

**Example (GitHub profile X-ray for bio/title terms):**
```
site:github.com ("AI consultant" OR "machine learning engineer") ("Python" OR "LLM") ("United Kingdom" OR "London")
```

**Example (BESS PM — non-technical, second Google X-ray):**
```
site:linkedin.com/in/ ("BESS" OR "battery energy storage" OR "energy storage systems") ("project manager" OR "delivery lead") ("Ontario" OR "Canada") -recruiter
```

### Step 4: Quality Check

Before sending, verify each string:

- [ ] Title synonyms cover common variations (minimum 3-4)
- [ ] Location includes regional variations (city + province/state + country)
- [ ] LinkedIn string uses uppercase AND/OR/NOT
- [ ] Google string starts with site:linkedin.com/in/
- [ ] No string exceeds practical length limits
- [ ] Strings are copy-paste ready — no explanation text inside them
- [ ] Niche terminology is correct for the industry

### Step 5: Deliver Results

In an interactive session, return the strings directly to the user. In an automated workflow, send results with `tools/notify.py` if a channel is configured or the user asked for notification.

Format the notification clearly. Example:

```
python tools/notify.py "Boolean strings for [Role] in [Location]:

LINKEDIN:
[full linkedin string]

GOOGLE:
[full google string]

GITHUB/ALTERNATE:
[full github string]"
```

If the message is too long for SMS (>1,600 chars), summarise and note that full strings are in the session log. If no notification channel is configured, do not claim a notification was sent.

## Common TA Roles — Quick Reference

### Renewable Energy / Cleantech
- BESS PM: Battery Energy Storage, BESS, ESS, grid-scale storage, commissioning, IFC, FEED, EPC
- Solar Developer: PV, photovoltaic, solar farm, utility-scale, interconnection, ERCOT, CAISO
- Wind Energy: turbine, WTG, onshore/offshore, O&M, wake modelling, AEP

### Enterprise Technology
- ERP: SAP, Oracle, Dynamics 365, NetSuite, implementation, go-live, RICE, UAT, change management
- CRM: Salesforce, HubSpot, Microsoft Dynamics, CRM migration, revenue operations
- Cloud: AWS, Azure, GCP, cloud architect, migration, IaaS, PaaS, DevOps, Terraform

### Recruitment / TA
- TA Leader: Head of Talent, VP People, Director of Recruiting, Talent Acquisition Partner
- RPO: Recruitment Process Outsourcing, embedded recruiter, on-site recruiter
- Executive Search: retained search, C-suite, board, headhunter, search consultant

### Finance
- CFO/Finance Director: financial controller, FP&A, chartered accountant, CA, CPA, CFA
- Private Equity: deal sourcing, portfolio operations, M&A, due diligence, LBO

## Notification Channels

notify.py reads from environment variables. Channels configured:

| Channel | Env Vars Required |
|---------|------------------|
| Twilio SMS | TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, NOTIFY_TO_PHONE |
| Webhook | NOTIFY_WEBHOOK_URL |
| Email | SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, NOTIFY_TO_EMAIL |

Usage:
```bash
python tools/notify.py "Your message here"
python tools/notify.py "Message" --channel twilio
python tools/notify.py "Message" --channel webhook
```

The script exits non-zero if no channel sends successfully.

## Reading a Role Brief from File

If tools/role-brief.txt exists, read it first:

```bash
cat tools/role-brief.txt
```

The file format is plain text:
```
Role: BESS Project Manager
Location: Ontario, Canada
Industry: Renewable Energy
Experience: 5+ years
Skills: Battery Energy Storage Systems, BESS commissioning, project delivery,
        stakeholder management, IFC/FEED, EPC contract management
Notes: Client prefers Ontario-based candidates, open to remote from elsewhere in Canada
```

## Quality Gates

- [ ] Role brief fully parsed before generating
- [ ] Minimum 4 title synonyms per role
- [ ] All three platform strings generated (or explained why not)
- [ ] Strings are copy-paste ready
- [ ] Results returned in the session or sent via notify.py when requested/configured
- [ ] Assumptions noted if brief was incomplete

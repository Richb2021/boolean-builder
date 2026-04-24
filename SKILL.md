---
name: boolean-builder
description: |
  Recruitment Boolean String Generator. Takes a role brief and generates
  platform-ready Boolean search strings for LinkedIn Recruiter, Google X-ray,
  and GitHub. Handles niche technical and professional roles. Sends results
  via SMS, webhook, or email using notify.py.
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

### Step 2: Build Layered Keyword Structure

Recruiters think in layers, not flat keyword lists. Before writing any string, categorise the role requirements into three layers:

**Layer 1 — Core identity (must-have in every string)**
- Job titles and their synonyms
- The single primary technology or discipline (Python, SAP, BESS, etc.)

**Layer 2 — Supporting skills (nice-to-have, widen recall)**
- Frameworks, tools, methodologies
- These should expand coverage, not restrict it
- Include alternatives — a strong Python engineer may use Flask instead of Django

**Layer 3 — Context filters (applied last)**
- Location (often better applied via UI filter than Boolean)
- Seniority signals
- Industry context

**The structured intent template (apply to every string):**
```
(TITLE GROUP) AND (CORE SKILL) AND (SUPPORTING SKILL GROUP) AND (LOCATION if needed)
```

This prevents the most common mistake: over-filtering by mixing core and supporting skills into one group, which eliminates strong candidates who describe their experience differently.

**Title synonyms — always generate minimum 4-6:**

| Role | Synonyms |
|------|----------|
| BESS Project Manager | "Battery Storage PM" "Energy Storage Manager" "BESS Delivery Lead" "Battery Project Lead" "ESS Project Manager" |
| ERP Implementation Lead | "ERP Consultant" "SAP Lead" "Systems Implementation Manager" "ERP Project Manager" "Enterprise Systems Lead" |
| Software Engineer | "Software Developer" "SWE" "Backend Engineer" "Full Stack Developer" "Application Developer" |
| Talent Acquisition | "Recruiter" "Talent Partner" "HR Business Partner" "People Operations" "Recruitment Manager" |
| Data Scientist | "ML Engineer" "Machine Learning Scientist" "Data Analyst" "AI Engineer" "Research Scientist" |

### Step 3: Generate the Strings

#### LinkedIn Recruiter String

**Important:** This string is for **LinkedIn Recruiter** (paid tool, ~$170-200/seat/month). Regular LinkedIn search does not support Boolean operators. Always clarify which tool the client is using.

**Syntax rules:**
- AND, OR, NOT must be uppercase
- Use quotes for multi-word phrases
- Maximum two OR groups — LinkedIn Recruiter breaks with more
- Keep under 500 characters
- Do NOT use site: operator
- Use LinkedIn's UI location filter rather than adding location to the string

**Structured template:**
```
(TITLE GROUP) AND (CORE SKILL) AND (SUPPORTING SKILL GROUP)
```

The core skill sits as a mandatory standalone AND — this anchors the search without over-filtering on specific tools.

**Example (Senior Python Engineer):**
```
("Senior Python Engineer" OR "Python Developer" OR "Backend Engineer" OR "Senior Backend Developer") AND Python AND (Django OR FastAPI OR Flask OR microservices OR AWS OR Kubernetes OR Docker OR PostgreSQL OR "REST API" OR API OR backend)
```
*Rationale: Broad title match + Python anchor + flexible skill coverage including database, API, and generic backend terms — catches strong candidates whose profiles don't explicitly list frameworks.*

**Example (ERP Implementation Consultant):**
```
("ERP Implementation Consultant" OR "SAP Consultant" OR "SAP S/4HANA Consultant" OR "Systems Implementation Consultant") AND (SAP OR "S/4HANA" OR "S4HANA" OR "S/4") AND ("implementation" OR "go-live" OR UAT OR "change management" OR WRICEF OR RICE)
```
*Rationale: Core tech anchor covers all SAP version abbreviations candidates actually use — S4HANA and S/4 alone can add 20-30% more results. Process terms kept as supporting layer.*

**Example (BESS PM):**
```
("BESS Project Manager" OR "Battery Storage Project Manager" OR "ESS Project Manager" OR "Energy Storage Manager") AND BESS AND (commissioning OR "EPC" OR "grid interconnection" OR "IFC" OR "FEED")
```
*Rationale: BESS as mandatory anchor eliminates generic PM noise. Supporting terms cover the full project lifecycle vocabulary used in renewables.*

#### Google X-ray String

**Syntax rules:**
- Must start with: site:linkedin.com/in/
- Use quotes for phrases
- AND is implied; use OR explicitly
- Aim for 3-4 term groups — too many and Google returns nothing
- Avoid overly generic titles ("software engineer" alone is too broad — anchor with a core skill)
- Use -recruiter -"talent acquisition" to filter noise

**Structured template:**
```
site:linkedin.com/in/ (SPECIFIC TITLE GROUP) (CORE SKILL) (LOCATION GROUP)
```

**Example (Senior Python Engineer, Toronto):**
```
site:linkedin.com/in/ ("Python engineer" OR "Python developer" OR "backend engineer") (Python AND (Django OR FastAPI OR Flask OR microservices OR AWS OR Docker)) ("Toronto" OR "Ontario" OR "Canada")
```
*Rationale: X-ray tuned for public profiles with strong backend signals. Docker added to capture infrastructure-heavy engineers who don't explicitly list AWS/GCP.*

**Example (ERP Consultant, Manchester):**
```
site:linkedin.com/in/ ("SAP consultant" OR "ERP consultant" OR "SAP S/4HANA") (SAP OR "S/4HANA") ("Manchester" OR "North West" OR "UK")
```
*Rationale: Clean title and core tech anchor. Location covers the regional hiring radius. Process terms excluded here — recruiter can layer manually after first pass.*

**Example (BESS PM, Ontario):**
```
site:linkedin.com/in/ ("BESS Project Manager" OR "Battery Storage" OR "Energy Storage") ("BESS" OR "battery energy storage" OR "grid interconnection") ("Ontario" OR "Toronto" OR "Canada")
```
*Rationale: Niche enough that broad title match + one technical term surfaces the right pool. Grid interconnection is a strong signal of hands-on project experience.*

#### GitHub String

**Important:** GitHub search is NOT Boolean. No OR groups, no brackets. Technical roles only — for non-technical roles, produce a second Google X-ray variant instead.

**Syntax rules:**
- `in:bio` — searches profile bio
- `followers:>10` — filters hobby/inactive accounts
- `repos:>3` — filters accounts with real activity
- `language:` — primary coding language
- `location:"City"` — location (not always populated)
- One or two keywords only

**Template (technical roles):**
```
"core skill" in:bio language:PrimaryLanguage location:"City" followers:>10 repos:>3
```

**Template (non-technical roles — second Google X-ray instead):**
```
site:linkedin.com/in/ ("role title" OR "alternate title") ("core skill") ("location") -recruiter -"talent acquisition"
```

**Example (Senior Python Engineer, Toronto):**
```
Python in:bio language:Python location:"Toronto" followers:>10 repos:>3
```
*Rationale: Filters hobby accounts (followers) and empty profiles (repos). language:Python confirms active coding, not just claimed skills.*

**Example (BESS PM — non-technical, second X-ray):**
```
site:linkedin.com/in/ ("BESS" OR "battery energy storage" OR "energy storage systems") ("project manager" OR "delivery lead") ("Ontario" OR "Canada") -recruiter -"talent acquisition"
```
*Rationale: Alternate X-ray surfaces candidates outside LinkedIn's algorithm. Negative exclusions remove recruiters and TA professionals from results — quiet intelligence that separates average from strong sourcing.*

#### Stack Overflow String

**What it is:** Demonstrated technical ability through real answers — stronger signal than a LinkedIn headline. Technical roles only.

**Syntax rules:**
- Use Google X-ray: site:stackoverflow.com/users
- Use an OR group for related technologies — this is Google syntax, OR groups work here
- Include location
- Keep to 3-4 terms maximum

**Template:**
```
site:stackoverflow.com/users ("Skill 1" OR "Skill 2" OR "Skill 3") "Location"
```

**Example (Senior Python Engineer, Toronto):**
```
site:stackoverflow.com/users ("Python" OR "Django" OR "FastAPI") "Toronto" "reputation"
```
*Rationale: Reputation filter reduces low-activity accounts and increases likelihood of candidates with demonstrated technical engagement.*

**Example (ML Engineer):**
```
site:stackoverflow.com/users ("machine learning" OR "PyTorch" OR "TensorFlow") "London" "reputation"
```
*Rationale: Stack Overflow is a lower-yield platform than GitHub for sourcing but surfaces candidates who demonstrate technical depth through real answers, not just claimed skills.*

### Step 4: Quality Check

Before sending, verify each string:

- [ ] Title synonyms cover common variations (minimum 3-4)
- [ ] Location includes regional variations (city + province/state + country)
- [ ] LinkedIn string uses uppercase AND/OR/NOT, max two OR groups
- [ ] Google string starts with site:linkedin.com/in/
- [ ] GitHub string generated for technical roles only; alternate X-ray used for non-technical
- [ ] Stack Overflow string generated for technical roles only; skipped otherwise
- [ ] No string exceeds practical length limits
- [ ] Strings are copy-paste ready — no explanation text inside them
- [ ] Niche terminology is correct for the industry

### Step 5: Send Results

**Always include a one-line rationale under each string.** This is not optional — it tells the recruiter why the string is built the way it is and builds trust in the output. Keep it to one sentence. Focus on the keyword strategy, not a description of the string itself.

Format the notification clearly. Example:

```
python tools/notify.py "Boolean strings for [Role] in [Location]:

LINKEDIN:
[full linkedin string]
Rationale: [one sentence]

GOOGLE:
[full google string]

GITHUB/ALTERNATE:
[full github string]"
```

If the message is too long for SMS (>1,600 chars), summarise and note that full strings are in the session log.

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
- [ ] Results sent via notify.py
- [ ] Assumptions noted if brief was incomplete

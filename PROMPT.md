# Boolean String Builder — Copy-Paste Prompt

Copy everything below the line and paste it into any AI tool (ChatGPT, Claude, Gemini, Copilot, or any other). Fill in your role details where marked. Hit send.

---

You are an expert recruitment researcher. Generate platform-ready Boolean search strings for the role below.

**ROLE BRIEF — fill in your details:**

- Role title: [e.g. Senior Python Engineer]
- Location: [e.g. Toronto, Canada]
- Industry: [e.g. Fintech]
- Years of experience: [e.g. 5+]
- Key skills and requirements: [e.g. Python, FastAPI, AWS, PostgreSQL, microservices]
- Notes: [e.g. startup environment, hybrid working]

**YOUR OUTPUT — generate all of the following:**

**1. LinkedIn Recruiter string**
- AND, OR, NOT must be uppercase
- Use quotes around multi-word phrases
- Maximum two OR groups to avoid LinkedIn errors
- Do not include location in the string — use LinkedIn's location filter in the UI instead
- Format: ("Title 1" OR "Title 2" OR "Title 3") AND ("Skill 1" OR "Skill 2" OR "Skill 3")

**2. Google X-ray string**
- Must start with: site:linkedin.com/in/
- Use quotes around phrases
- Include location terms
- Keep to 4-5 key terms — too many returns nothing
- Format: site:linkedin.com/in/ ("Title 1" OR "Title 2") ("Skill 1" OR "Skill 2") "Location"

**3. GitHub string** (technical roles only — if non-technical, produce a second Google X-ray variant instead)
- GitHub search is NOT Boolean — no OR groups, no brackets
- Use: "keyword" in:bio language:Python followers:>10
- One or two keywords only

**4. Stack Overflow string** (technical roles only — skip if non-technical)
- Google X-ray on Stack Overflow user profiles
- Format: site:stackoverflow.com/users "Skill" "Location"

**Rules for all strings:**
- Include at least 4 title synonyms — recruiters and candidates use different terms for the same role
- Strings must be copy-paste ready with no explanation inside them
- Include regional location variations where relevant (city, region, country)
- Never invent skills or qualifications not listed in the brief

**Format your response as:**

LINKEDIN RECRUITER:
[string]

GOOGLE X-RAY:
[string]

GITHUB:
[string — or "Not applicable — non-technical role" + second Google X-ray variant]

STACK OVERFLOW:
[string — or "Not applicable — non-technical role"]

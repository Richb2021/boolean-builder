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
- Structure in layers: title group AND core skill AND supporting skill group
- Format: ("Title 1" OR "Title 2" OR "Title 3") AND CoreSkill AND (Tool1 OR Tool2 OR Tool3 OR Alternative)
- The core skill as a standalone AND is mandatory — it anchors the search. The supporting group should include alternatives so strong candidates aren't missed.

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
- Think in layers: (1) title group, (2) core mandatory skill, (3) supporting skills with alternatives, (4) location
- The core skill sits as a mandatory standalone AND — this anchors the search without over-filtering on specific tools
- Supporting skills must include alternatives — a strong candidate may use Flask instead of Django, or describe experience differently
- Include at least 4 title synonyms — recruiters and candidates use different terms for the same role
- Avoid overly generic terms on their own ("software engineer" alone is too broad — anchor with a core skill)
- Strings must be copy-paste ready with no explanation inside them
- Include regional location variations (city, region, country)
- Never invent skills or qualifications not in the brief

**Format your response as:**

LINKEDIN RECRUITER:
[string]
Why: [one sentence explaining the keyword strategy — e.g. "Python as mandatory anchor with broad framework coverage for high recall"]

GOOGLE X-RAY:
[string]
Why: [one sentence — e.g. "X-ray tuned for public profiles with backend signals, Docker added to cover real-world infrastructure experience"]

GITHUB:
[string — or "Not applicable — non-technical role" + second Google X-ray variant]
Why: [one sentence]

STACK OVERFLOW:
[string — or "Not applicable — non-technical role"]
Why: [one sentence]

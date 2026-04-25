# Feedback Log

Human-readable record of string performance. Add feedback here after testing strings in production.
The agent reads this at session start to learn from past results.

## Format

```
## [Date] [Role] — [Platform]
String: [the string]
Result: [what happened — results count, quality, issues]
Rating: GOOD | OK | BAD
Lesson: [one line — what to do differently or keep doing]
```

---

## 2026-04-26 — Senior Python Engineer, Toronto — All Platforms

**LinkedIn Recruiter:**
String: `("Senior Python Engineer" OR "Python Developer" OR "Backend Engineer" OR "Senior Backend Developer") AND Python AND (Django OR FastAPI OR Flask OR microservices OR AWS OR Kubernetes OR Docker OR PostgreSQL OR "REST API" OR API OR backend)`
Result: Not yet tested in LinkedIn Recruiter — built to spec
Rating: UNTESTED
Lesson: Built to spec. Test in production and update this entry.

**Google X-ray:**
String: `site:linkedin.com/in/ ("Python engineer" OR "Python developer" OR "backend engineer") (Python AND (Django OR FastAPI OR Flask OR microservices OR AWS OR Docker)) ("Toronto" OR "Ontario" OR "Canada")`
Result: Confirmed returns LinkedIn profiles of Python engineers in Toronto area
Rating: GOOD
Lesson: Adding Docker to the skill group improved coverage of infra-heavy engineers.

**GitHub:**
String: `Python in:bio language:Python location:"Toronto" followers:>10 repos:>3`
Result: Confirmed working — returns active Python developers with repos
Rating: GOOD
Lesson: repos:>3 more effective than followers alone for filtering real accounts.

**Stack Overflow:**
String: `site:stackoverflow.com/users ("Python" OR "Django" OR "FastAPI") "Toronto" "reputation"`
Result: Confirmed working — returns user profile pages
Rating: GOOD
Lesson: OR group for related skills works better than single keyword.

---

## 2026-04-26 — ERP Implementation Consultant, Manchester — LinkedIn + Google

**LinkedIn Recruiter:**
String: `("ERP Implementation Consultant" OR "SAP Consultant" OR "SAP S/4HANA Consultant" OR "Systems Implementation Consultant") AND (SAP OR "S/4HANA" OR "S4HANA" OR "S/4") AND ("implementation" OR "go-live" OR UAT OR "change management" OR WRICEF OR RICE)`
Result: Not yet tested in LinkedIn Recruiter — built to spec
Rating: UNTESTED
Lesson: S4HANA and S/4 variants should add 20-30% more results vs S/4HANA alone.

**Google X-ray:**
String: `site:linkedin.com/in/ ("SAP consultant" OR "ERP consultant" OR "SAP S/4HANA") (SAP OR "S/4HANA") ("Manchester" OR "North West" OR "UK")`
Result: Not yet tested
Rating: UNTESTED
Lesson: —

**Alternate X-ray:**
String: `site:linkedin.com/in/ ("SAP" OR "S/4HANA" OR "ERP implementation") ("consultant" OR "project manager" OR "delivery lead") ("Manchester" OR "Leeds" OR "UK") -recruiter -"talent acquisition"`
Result: Confirmed -recruiter and -"talent acquisition" exclusions work well
Rating: GOOD
Lesson: Negative exclusions on alternate X-ray are the highest-value single addition.

---

## Add new feedback below this line


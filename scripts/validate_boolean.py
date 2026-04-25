#!/usr/bin/env python3
"""
Boolean String Validator for Boolean Builder Agent

Checks generated Boolean strings against platform-specific syntax rules,
character limits, structural quality, and completeness.

Usage:
    # Validate strings passed as arguments
    python scripts/validate_boolean.py \
        --linkedin '("Python Dev" OR "Backend Eng") AND Python AND (Django OR Flask)' \
        --google 'site:linkedin.com/in/ ("Python dev") Python "Toronto"' \
        --github 'Python in:bio language:Python location:"Toronto" followers:>10 repos:>3' \
        --stackoverflow 'site:stackoverflow.com/users ("Python" OR "Django") "Toronto" "reputation"'

    # Validate from a JSON file
    python scripts/validate_boolean.py --file output.json

    # Validate from stdin (JSON)
    echo '{"linkedin": "...", "google": "..."}' | python scripts/validate_boolean.py --stdin

Exit codes:
    0 — All checks passed (or only warnings)
    1 — One or more hard failures
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class Check:
    name: str
    passed: bool
    level: str          # "error" | "warning" | "info"
    message: str


@dataclass
class PlatformResult:
    platform: str
    string: str
    checks: list[Check] = field(default_factory=list)

    @property
    def errors(self):
        return [c for c in self.checks if not c.passed and c.level == "error"]

    @property
    def warnings(self):
        return [c for c in self.checks if not c.passed and c.level == "warning"]

    @property
    def passed(self):
        return len(self.errors) == 0

    @property
    def score(self):
        total = len(self.checks)
        if total == 0:
            return 100
        passed = sum(1 for c in self.checks if c.passed)
        return round((passed / total) * 100)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def count_or_groups(s: str) -> int:
    """Count distinct OR groups (text in parentheses containing OR)."""
    groups = re.findall(r'\([^)]+\)', s)
    return sum(1 for g in groups if ' OR ' in g.upper())


def has_uppercase_operators(s: str) -> bool:
    """Check that AND/OR/NOT are uppercase (not lowercase)."""
    # Lowercase operators would appear as standalone words
    has_lower_and = bool(re.search(r'\band\b', s))
    has_lower_or  = bool(re.search(r'\bor\b', s))
    has_lower_not = bool(re.search(r'\bnot\b', s))
    return not (has_lower_and or has_lower_or or has_lower_not)


def count_operators(s: str) -> int:
    """Count total Boolean operators."""
    operators = re.findall(r'\b(AND|OR|NOT)\b', s)
    return len(operators)


def has_negative_exclusions(s: str) -> bool:
    """Check for at least one negative exclusion."""
    return bool(re.search(r'-\w+', s))


def count_title_synonyms(s: str) -> int:
    """Estimate number of title synonyms in the first OR group."""
    first_group = re.search(r'\(([^)]+)\)', s)
    if not first_group:
        return 0
    return first_group.group(1).upper().count(' OR ') + 1


# ---------------------------------------------------------------------------
# Platform validators
# ---------------------------------------------------------------------------

def validate_linkedin(s: str) -> PlatformResult:
    result = PlatformResult(platform="LinkedIn Recruiter", string=s)
    checks = result.checks

    # Hard rules (errors)
    checks.append(Check(
        "No site: operator",
        "site:" not in s.lower(),
        "error",
        "LinkedIn strings must not contain site: — that is Google syntax"
    ))

    checks.append(Check(
        "Uppercase AND/OR/NOT operators",
        has_uppercase_operators(s),
        "error",
        "LinkedIn requires AND, OR, NOT in uppercase — lowercase operators are ignored"
    ))

    or_groups = count_or_groups(s)
    checks.append(Check(
        "Maximum two OR groups",
        or_groups <= 2,
        "error",
        f"Found {or_groups} OR groups — LinkedIn Recruiter breaks silently with more than 2"
    ))

    char_count = len(s)
    checks.append(Check(
        "Character limit (<500)",
        char_count <= 500,
        "error",
        f"String is {char_count} characters — LinkedIn truncates above 500"
    ))

    checks.append(Check(
        "Has AND connectors",
        " AND " in s,
        "error",
        "String has no AND connectors — likely a flat keyword list with no structure"
    ))

    # Structural quality (warnings)
    synonyms = count_title_synonyms(s)
    checks.append(Check(
        "Minimum 4 title synonyms",
        synonyms >= 4,
        "warning",
        f"First OR group has ~{synonyms} terms — aim for 4-6 title synonyms for broad recall"
    ))

    checks.append(Check(
        "Core skill anchor present",
        bool(re.search(r'\bAND\s+\w+\s+AND\b', s)),
        "warning",
        "No standalone core skill anchor detected (e.g. AND Python AND) — layered structure improves recall"
    ))

    checks.append(Check(
        "No location in string",
        not bool(re.search(r'\b(UK|USA|London|Toronto|Canada|United Kingdom)\b', s, re.IGNORECASE)),
        "warning",
        "Location found in string — use LinkedIn's location filter in the UI for more reliable results"
    ))

    return result


def validate_google_xray(s: str) -> PlatformResult:
    result = PlatformResult(platform="Google X-ray", string=s)
    checks = result.checks

    checks.append(Check(
        "Starts with site:linkedin.com/in/",
        s.strip().startswith("site:linkedin.com/in/"),
        "error",
        "Google X-ray string must start with site:linkedin.com/in/"
    ))

    checks.append(Check(
        "Has quoted phrases",
        '"' in s,
        "error",
        "No quoted phrases found — multi-word terms must be in quotes"
    ))

    checks.append(Check(
        "Has negative exclusions",
        has_negative_exclusions(s),
        "warning",
        "No negative exclusions found — add -recruiter -consultant -freelancer to reduce noise"
    ))

    # Check not too many groups (Google returns nothing with too many)
    or_groups = count_or_groups(s)
    checks.append(Check(
        "Not over-specified (max 4 OR groups)",
        or_groups <= 4,
        "warning",
        f"Found {or_groups} OR groups — Google returns fewer results with complex queries, aim for 3-4 max"
    ))

    checks.append(Check(
        "Has location terms",
        bool(re.search(r'"[A-Z][a-z]+ ?(OR [A-Z])?[a-z]*"', s)) or
        bool(re.search(r'\b(UK|USA|Canada|London|Toronto|United Kingdom|United States)\b', s, re.IGNORECASE)),
        "warning",
        "No obvious location terms found — X-ray without location returns global noise"
    ))

    return result


def validate_github(s: str) -> PlatformResult:
    result = PlatformResult(platform="GitHub", string=s)
    checks = result.checks

    checks.append(Check(
        "No site: operator",
        "site:" not in s.lower(),
        "error",
        "GitHub search does not use site: — that is Google syntax"
    ))

    checks.append(Check(
        "No OR groups with brackets",
        not bool(re.search(r'\([^)]*\bOR\b[^)]*\)', s, re.IGNORECASE)),
        "error",
        "GitHub search does not support OR groups in brackets — use simple keyword + qualifiers"
    ))

    has_qualifier = any(q in s for q in [
        "in:bio", "language:", "followers:", "location:", "repos:"
    ])
    checks.append(Check(
        "Has at least one GitHub qualifier",
        has_qualifier,
        "error",
        "No GitHub qualifiers found — add in:bio, language:, followers:>N, or repos:>N"
    ))

    checks.append(Check(
        "Has followers filter",
        "followers:" in s,
        "warning",
        "No followers: filter — add followers:>10 to remove hobby/inactive accounts"
    ))

    checks.append(Check(
        "Has repos filter",
        "repos:" in s,
        "warning",
        "No repos: filter — add repos:>3 to filter empty profiles"
    ))

    checks.append(Check(
        "Has language filter (for technical roles)",
        "language:" in s,
        "warning",
        "No language: filter — for technical roles, language:Python confirms active coding not just claimed skill"
    ))

    return result


def validate_stackoverflow(s: str) -> PlatformResult:
    result = PlatformResult(platform="Stack Overflow", string=s)
    checks = result.checks

    checks.append(Check(
        "Starts with site:stackoverflow.com/users",
        "site:stackoverflow.com/users" in s,
        "error",
        "Stack Overflow X-ray must use site:stackoverflow.com/users"
    ))

    checks.append(Check(
        "Has quoted skill terms",
        '"' in s,
        "error",
        "No quoted terms found — skills must be in quotes"
    ))

    checks.append(Check(
        "Has reputation filter",
        "reputation" in s.lower(),
        "warning",
        "No reputation filter — add 'reputation' to reduce low-activity accounts"
    ))

    or_groups = count_or_groups(s)
    checks.append(Check(
        "Has OR group for related skills",
        or_groups >= 1,
        "warning",
        "No OR group for related skills — Stack Overflow X-ray benefits from skill alternatives e.g. ('Python' OR 'Django' OR 'FastAPI')"
    ))

    return result


# ---------------------------------------------------------------------------
# Scorer and reporter
# ---------------------------------------------------------------------------

def print_result(result: PlatformResult, verbose: bool = False) -> None:
    status = "PASS" if result.passed else "FAIL"
    score_str = f"{result.score}/100"
    print(f"\n{'='*60}")
    print(f"  {result.platform.upper()}  [{status}]  Score: {score_str}")
    print(f"{'='*60}")
    print(f"  String: {result.string[:120]}{'...' if len(result.string) > 120 else ''}")
    print()

    if result.errors:
        print("  ERRORS (must fix):")
        for c in result.errors:
            print(f"    ✗  {c.name}")
            print(f"       {c.message}")

    if result.warnings:
        print("  WARNINGS (should fix):")
        for c in result.warnings:
            print(f"    ⚠  {c.name}")
            print(f"       {c.message}")

    if verbose:
        passed_checks = [c for c in result.checks if c.passed]
        if passed_checks:
            print("  PASSED:")
            for c in passed_checks:
                print(f"    ✓  {c.name}")


def run_validation(strings: dict, verbose: bool = False) -> list[PlatformResult]:
    validators = {
        "linkedin":      validate_linkedin,
        "google":        validate_google_xray,
        "github":        validate_github,
        "stackoverflow": validate_stackoverflow,
    }

    results = []
    for key, validator in validators.items():
        if key in strings and strings[key]:
            result = validator(strings[key])
            results.append(result)

    return results


def print_summary(results: list[PlatformResult]) -> bool:
    """Print summary and return True if all passed."""
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")

    all_passed = True
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        warnings = f"  ({len(r.warnings)} warnings)" if r.warnings else ""
        print(f"  {status}  {r.platform:<30} {r.score}/100{warnings}")
        if not r.passed:
            all_passed = False

    overall = "ALL CHECKS PASSED" if all_passed else "VALIDATION FAILED — fix errors above"
    print(f"\n  Overall: {overall}")
    return all_passed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate Boolean search strings for platform-specific rules."
    )
    parser.add_argument("--linkedin",      help="LinkedIn Recruiter string")
    parser.add_argument("--google",        help="Google X-ray string")
    parser.add_argument("--github",        help="GitHub string")
    parser.add_argument("--stackoverflow", help="Stack Overflow string")
    parser.add_argument("--file",          help="JSON file with platform strings")
    parser.add_argument("--stdin",         action="store_true", help="Read JSON from stdin")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show passing checks too")
    parser.add_argument("--json-out",      action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    strings = {}

    if args.stdin:
        try:
            strings = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error parsing stdin JSON: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        strings = json.loads(path.read_text())
    else:
        if args.linkedin:      strings["linkedin"]      = args.linkedin
        if args.google:        strings["google"]        = args.google
        if args.github:        strings["github"]        = args.github
        if args.stackoverflow: strings["stackoverflow"] = args.stackoverflow

    if not strings:
        parser.print_help()
        sys.exit(1)

    results = run_validation(strings, verbose=args.verbose)

    if args.json_out:
        output = []
        for r in results:
            output.append({
                "platform": r.platform,
                "score": r.score,
                "passed": r.passed,
                "errors": [{"name": c.name, "message": c.message} for c in r.errors],
                "warnings": [{"name": c.name, "message": c.message} for c in r.warnings],
            })
        print(json.dumps(output, indent=2))
    else:
        for r in results:
            print_result(r, verbose=args.verbose)
        all_passed = print_summary(results)
        sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

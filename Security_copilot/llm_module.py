import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


SECTION_HEADINGS = [
    "Executive Summary",
    "Business Impact",
    "Priority Recommendations",
    "Quick Wins",
    "Longer-Term Improvements",
]


def _build_org_profile_text(org_profile):
    return f"""
Organisation profile:
- Organisation: {org_profile.get('org_name', 'N/A')}
- Sector: {org_profile.get('sector', 'N/A')}
- Company size: {org_profile.get('size', 'N/A')}
- Internal IT team: {org_profile.get('it_team', 'N/A')}
- Dedicated security staff: {org_profile.get('security_staff', 'N/A')}
- Web application type: {org_profile.get('web_app_type', 'N/A')}
- Stores customer data: {org_profile.get('stores_customer_data', 'N/A')}
- Processes payments: {org_profile.get('processes_payments', 'N/A')}
- Uses cloud hosting: {org_profile.get('uses_cloud', 'N/A')}
- Uses third-party support: {org_profile.get('uses_third_party_support', 'N/A')}
""".strip()


def _build_results_text(results):
    top_categories = results.get("category_results", [])[:3]
    top_remediations = results.get("remediation_actions", [])[:5]

    category_text = "\n".join(
        f"- {c['owasp']}: {c['percent']}% ({c['level']})"
        for c in top_categories
    ) or "- No category data available."

    remediation_text = "\n".join(
        f"- {r['owasp']}: {r['remediation']}"
        for r in top_remediations
    ) or "- No remediation priorities available."

    return f"""
Assessment summary:
- Overall risk level: {results.get('overall_level', 'N/A')}
- Overall risk exposure: {results.get('overall_percent', 'N/A')}%
- ASVS Level 1 compliance proxy: {results.get('asvs_compliance_percent', 'N/A')}%

Top OWASP categories:
{category_text}

Top remediation priorities:
{remediation_text}
""".strip()


def _build_output_format_instructions():
    return """
Return the response in exactly this format:

Executive Summary:
<2-4 sentences>

Business Impact:
<2-4 sentences>

Priority Recommendations:
- item 1
- item 2
- item 3

Quick Wins:
- item 1
- item 2

Longer-Term Improvements:
- item 1
- item 2

Use simple language suitable for a non-technical SME manager.
""".strip()


def build_prompt(org_profile, results):
    return f"""
You are a cybersecurity advisor for small and medium-sized businesses.

{_build_org_profile_text(org_profile)}

{_build_results_text(results)}

{_build_output_format_instructions()}
""".strip()


def build_refinement_prompt(org_profile, results, first_output_text):
    return f"""
You are refining a cybersecurity report for a small or medium-sized business.

{_build_org_profile_text(org_profile)}

{_build_results_text(results)}

Initial draft:
{first_output_text}

Refine the draft so it is:
1. More specific to the business profile
2. More practical for an SME
3. Better prioritised
4. Clear for a non-technical manager
5. Concise and professional

{_build_output_format_instructions()}
""".strip()


def fallback_tailored_output(org_profile, results, reason="Fallback mode used."):
    top_categories = results.get("category_results", [])[:3]
    remediations = results.get("remediation_actions", [])[:3]

    top_category_names = (
        ", ".join(c["owasp"] for c in top_categories)
        if top_categories
        else "general web security issues"
    )

    top_recommendations = (
        [r["remediation"] for r in remediations]
        if remediations
        else ["Maintain current controls and review regularly."]
    )

    quick_wins = []
    long_term = []

    if org_profile.get("processes_payments") == "yes":
        quick_wins.append("Enable MFA for admin and payment-related accounts.")
    if org_profile.get("stores_customer_data") == "yes":
        quick_wins.append("Review access to stored customer data and ensure encryption is in place.")
    if org_profile.get("uses_cloud") == "yes":
        quick_wins.append("Review cloud configuration settings and remove unnecessary exposure.")
    if org_profile.get("security_staff") == "no":
        long_term.append("Introduce a lightweight security review process for updates and access changes.")
    if org_profile.get("it_team") == "no":
        long_term.append("Assign ownership for patching, backups, and periodic security reviews.")

    if not quick_wins:
        quick_wins = [
            "Review the highest-risk categories first.",
            "Strengthen admin access controls.",
        ]

    if not long_term:
        long_term = [
            "Establish regular patching and monitoring.",
            "Review security logging and incident response readiness.",
        ]

    return {
        "mode": "fallback",
        "debug_reason": reason,
        "executive_summary": (
            f"This organisation received an overall {results.get('overall_level')} risk rating "
            f"with {results.get('overall_percent')}% exposure. The main areas of concern are "
            f"{top_category_names}."
        ),
        "business_impact": (
            "If these weaknesses remain unresolved, they could increase the likelihood of "
            "unauthorised access, service disruption, data exposure, or reputational damage."
        ),
        "priority_recommendations": top_recommendations,
        "quick_wins": quick_wins,
        "long_term_improvements": long_term,
    }


def _extract_section(text, heading):
    marker = f"{heading}:"
    start = text.find(marker)
    if start == -1:
        return ""

    start += len(marker)

    next_positions = []
    for h in SECTION_HEADINGS:
        marker_h = f"{h}:"
        if marker_h != marker:
            pos = text.find(marker_h, start)
            if pos != -1:
                next_positions.append(pos)

    end = min(next_positions) if next_positions else len(text)
    return text[start:end].strip()


def _extract_bullets(section_text):
    items = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def _parse_llm_text(final_text):
    executive_summary = _extract_section(final_text, "Executive Summary")
    business_impact = _extract_section(final_text, "Business Impact")
    priority_recommendations = _extract_bullets(
        _extract_section(final_text, "Priority Recommendations")
    )
    quick_wins = _extract_bullets(_extract_section(final_text, "Quick Wins"))
    long_term_improvements = _extract_bullets(
        _extract_section(final_text, "Longer-Term Improvements")
    )

    return {
        "executive_summary": executive_summary or final_text,
        "business_impact": business_impact or "Included in generated summary.",
        "priority_recommendations": priority_recommendations,
        "quick_wins": quick_wins,
        "long_term_improvements": long_term_improvements,
    }


def generate_tailored_llm_output(org_profile, results):
    api_key = os.environ.get("OPENAI_API_KEY")

    if OpenAI is None:
        print("[LLM DEBUG] OpenAI package import failed.")
        return fallback_tailored_output(
            org_profile,
            results,
            "OpenAI package not installed or import failed.",
        )

    if not api_key:
        print("[LLM DEBUG] OPENAI_API_KEY is missing.")
        return fallback_tailored_output(
            org_profile,
            results,
            "OPENAI_API_KEY is not set.",
        )

    prompt = build_prompt(org_profile, results)

    try:
        print("[LLM DEBUG] Starting OpenAI first-pass call...")
        client = OpenAI(api_key=api_key)

        first_response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        first_text = getattr(first_response, "output_text", "").strip()

        if not first_text:
            return fallback_tailored_output(
                org_profile,
                results,
                "LLM first-pass returned empty output.",
            )

        print("[LLM DEBUG] Starting OpenAI second-pass refinement...")
        refinement_prompt = build_refinement_prompt(org_profile, results, first_text)

        refined_response = client.responses.create(
            model="gpt-4.1-mini",
            input=refinement_prompt,
        )

        refined_text = getattr(refined_response, "output_text", "").strip()
        final_text = refined_text if refined_text else first_text

        parsed = _parse_llm_text(final_text)

        return {
            "mode": "llm_refined",
            "debug_reason": "Two-pass LLM generation succeeded.",
            **parsed,
        }

    except Exception as e:
        error_text = f"{type(e).__name__}: {str(e)}"
        print(f"[LLM DEBUG] OpenAI call failed: {error_text}")

        return fallback_tailored_output(
            org_profile,
            results,
            f"LLM API call failed: {error_text}",
        )
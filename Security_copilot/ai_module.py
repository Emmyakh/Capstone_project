import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def generate_ai_explanation(risk):
    """
    Existing explanation block kept for top OWASP risks.
    """
    explanation = f"""
This vulnerability relates to {risk['owasp']}.

Why it matters:
{risk['issue']}

Recommended SME mitigation:
- Apply OWASP best practices
- Prioritise fixing this issue based on severity
- Conduct secure configuration reviews
"""
    return explanation.strip()


def build_prompt(org_profile, results):
    top_categories = results.get("category_results", [])[:3]
    top_remediations = results.get("remediation_actions", [])[:5]

    category_text = "\n".join(
        [f"- {c['owasp']}: {c['percent']}% ({c['level']})" for c in top_categories]
    )

    remediation_text = "\n".join(
        [f"- {r['owasp']}: {r['remediation']}" for r in top_remediations]
    )

    prompt = f"""
You are a cybersecurity advisor for small and medium-sized businesses.

Organisation profile:
- Organisation: {org_profile.get('org_name', 'N/A')}
- Sector: {org_profile.get('sector', 'N/A')}
- Company size: {org_profile.get('size', 'N/A')}
- Internal IT team: {org_profile.get('it_team', 'N/A')}
- Dedicated security staff: {org_profile.get('security_staff', 'N/A')}
- Web application type: {org_profile.get('web_app_type', 'N/A')}
- Stores customer data: {org_profile.get('stores_customer_data', 'N/A')}
- Processes online payments: {org_profile.get('processes_payments', 'N/A')}
- Uses cloud hosting: {org_profile.get('uses_cloud', 'N/A')}
- Uses third-party web support: {org_profile.get('uses_third_party_support', 'N/A')}

Assessment summary:
- Overall risk level: {results.get('overall_level')}
- Overall risk exposure: {results.get('overall_percent')}%
- ASVS Level 1 compliance proxy: {results.get('asvs_compliance_percent')}%

Top OWASP categories:
{category_text}

Top remediation priorities:
{remediation_text}

Return a concise business-friendly response with these headings:
1. Executive Summary
2. Business Impact
3. Priority Recommendations
4. Quick Wins
5. Longer-Term Improvements

Keep the language simple and suitable for a non-technical SME manager.
"""
    return prompt.strip()


def fallback_tailored_output(org_profile, results):
    top_categories = results.get("category_results", [])[:3]
    remediations = results.get("remediation_actions", [])[:5]

    sector = org_profile.get("sector", "SME")
    app_type = org_profile.get("web_app_type", "web application")
    overall_level = results.get("overall_level", "Unknown")
    overall_percent = results.get("overall_percent", 0)

    top_category_names = [c["owasp"] for c in top_categories]
    key_risks = ", ".join(top_category_names) if top_category_names else "general web security weaknesses"

    top_recommendations = [r["remediation"] for r in remediations[:3]]
    if not top_recommendations:
        top_recommendations = ["Maintain current controls and review them regularly."]

    quick_wins = []
    longer_term = []

    if org_profile.get("processes_payments") == "yes":
        quick_wins.append("Review payment-related access controls and enforce MFA for admin accounts.")
    if org_profile.get("stores_customer_data") == "yes":
        quick_wins.append("Verify that customer data is encrypted and access is limited to authorised staff only.")
    if org_profile.get("uses_cloud") == "yes":
        quick_wins.append("Review cloud configuration settings and remove unnecessary public exposure.")
    if org_profile.get("it_team") == "no":
        longer_term.append("Assign clear security ownership or engage a trusted managed provider for regular reviews.")
    if org_profile.get("security_staff") == "no":
        longer_term.append("Introduce a lightweight security review process for changes, updates, and incidents.")

    if not quick_wins:
        quick_wins = [
            "Apply the highest-priority remediation actions first.",
            "Review admin accounts and session security settings."
        ]

    if not longer_term:
        longer_term = [
            "Establish a regular patching and review cycle.",
            "Improve logging, monitoring, and incident response readiness."
        ]

    return {
        "executive_summary": (
            f"This {sector} organisation operates a {app_type} and received an overall "
            f"{overall_level} risk rating ({overall_percent}% exposure). The most significant "
            f"areas of concern are {key_risks}."
        ),
        "business_impact": (
            f"If these weaknesses are not addressed, the organisation may face unauthorised access, "
            f"data exposure, service disruption, or loss of trust from customers and stakeholders."
        ),
        "priority_recommendations": top_recommendations,
        "quick_wins": quick_wins,
        "long_term_improvements": longer_term,
        "prompt_used": build_prompt(org_profile, results)
    }


def generate_tailored_llm_output(org_profile, results):
    """
    Uses OpenAI if OPENAI_API_KEY is available and the openai package is installed.
    Otherwise falls back to a deterministic tailored output.
    The OpenAI API supports project API keys and Python client usage through official docs. :contentReference[oaicite:0]{index=0}
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return fallback_tailored_output(org_profile, results)

    prompt = build_prompt(org_profile, results)

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text_output = getattr(response, "output_text", "").strip()

        if not text_output:
            return fallback_tailored_output(org_profile, results)

        return {
            "executive_summary": text_output,
            "business_impact": "Generated within the executive summary.",
            "priority_recommendations": [],
            "quick_wins": [],
            "long_term_improvements": [],
            "prompt_used": prompt
        }

    except Exception:
        return fallback_tailored_output(org_profile, results)
from scenario_data import SCENARIOS
from question_bank import QUESTIONS
from scoring import compute_scores
from llm_module import generate_tailored_llm_output

all_results = []

for scenario in SCENARIOS:
    results = compute_scores(QUESTIONS, scenario["answers"])
    llm_output = generate_tailored_llm_output(scenario, results)

    top_categories = results["category_results"][:3]

    all_results.append({
        "org_name": scenario["org_name"],
        "sector": scenario["sector"],
        "overall_level": results["overall_level"],
        "overall_percent": results["overall_percent"],
        "asvs_compliance_percent": results["asvs_compliance_percent"],
        "top_categories": [
            f"{c['owasp']} ({c['percent']}%, {c['level']})" for c in top_categories
        ],
        "priority_recommendations": llm_output["priority_recommendations"],
        "quick_wins": llm_output["quick_wins"],
        "executive_summary": llm_output["executive_summary"]
    })

for r in all_results:
    print("\n" + "=" * 80)
    print(f"Organisation: {r['org_name']}")
    print(f"Sector: {r['sector']}")
    print(f"Overall Risk: {r['overall_level']} ({r['overall_percent']}%)")
    print(f"ASVS Compliance Proxy: {r['asvs_compliance_percent']}%")
    print("Top Categories:")
    for cat in r["top_categories"]:
        print(f" - {cat}")
    print("Priority Recommendations:")
    for rec in r["priority_recommendations"]:
        print(f" - {rec}")
    print("Quick Wins:")
    for q in r["quick_wins"]:
        print(f" - {q}")
    print("Executive Summary:")
    print(r["executive_summary"])
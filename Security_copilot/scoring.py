ANSWER_VALUES = {
    "yes": 0,
    "managed": 1,
    "not_sure": 2,
    "no": 3
}

def classify_percentage(percent: float) -> str:
    if percent <= 20:
        return "Low"
    elif percent <= 50:
        return "Medium"
    elif percent <= 75:
        return "High"
    else:
        return "Critical"


def compute_scores(questions, form_data):

    cat_score = {}
    cat_max = {}

    remediation_actions = []

    total_controls = len(questions)
    yes_count = 0

    for q in questions:
        ans = form_data.get(q["id"], "not_sure")

        if ans == "yes":
            yes_count += 1

        value = ANSWER_VALUES.get(ans, 2)
        weighted = value * q["weight"]

        owasp = q["owasp"]
        cat_score[owasp] = cat_score.get(owasp, 0) + weighted
        cat_max[owasp] = cat_max.get(owasp, 0) + (3 * q["weight"])

        # 🔥 Add remediation if not fully satisfied
        if ans in ["no", "not_sure", "managed"]:
            remediation_actions.append({
                "question_id": q["id"],
                "question": q["text"],
                "owasp": q["owasp"],
                "severity_weight": q["weight"],
                "answer": ans,
                "remediation": q["remediation"]
            })

    # Sort remediation by severity weight (highest first)
    remediation_actions.sort(key=lambda x: x["severity_weight"], reverse=True)

    category_results = []
    overall_score = 0
    overall_max = 0

    for owasp in cat_score:
        score = cat_score[owasp]
        maximum = cat_max[owasp]
        percent = round((score / maximum) * 100, 2) if maximum else 0.0
        level = classify_percentage(percent)

        category_results.append({
            "owasp": owasp,
            "score": score,
            "max": maximum,
            "percent": percent,
            "level": level
        })

        overall_score += score
        overall_max += maximum

    category_results.sort(key=lambda x: x["percent"], reverse=True)

    overall_percent = round((overall_score / overall_max) * 100, 2) if overall_max else 0.0
    overall_level = classify_percentage(overall_percent)

    asvs_compliance = round((yes_count / total_controls) * 100, 2) if total_controls else 0.0

    return {
        "category_results": category_results,
        "overall_score": overall_score,
        "overall_percent": overall_percent,
        "overall_level": overall_level,
        "asvs_compliance_percent": asvs_compliance,
        "remediation_actions": remediation_actions
    }
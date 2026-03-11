OWASP_WEIGHTS = {
    "A01 Broken Access Control": 5,
    "A02 Cryptographic Failures": 4,
    "A03 Injection": 5,
    "A05 Security Misconfiguration": 3,
    "A07 Identification & Authentication Failures": 4,
    "A09 Security Logging & Monitoring Failures": 3
}


def assess_risks(form_data):
    risks = []

    if form_data.get("input_validation") == "no":
        risks.append({
            "owasp": "A03 Injection",
            "issue": "Application does not validate user inputs, increasing risk of SQL Injection.",
            "severity": OWASP_WEIGHTS["A03 Injection"]
        })

    if form_data.get("authentication") == "no":
        risks.append({
            "owasp": "A07 Identification & Authentication Failures",
            "issue": "Weak authentication mechanisms may allow unauthorised access.",
            "severity": OWASP_WEIGHTS["A07 Identification & Authentication Failures"]
        })

    if form_data.get("https") == "no":
        risks.append({
            "owasp": "A02 Cryptographic Failures",
            "issue": "Data transmission is not encrypted, exposing sensitive information.",
            "severity": OWASP_WEIGHTS["A02 Cryptographic Failures"]
        })

    return risks


def calculate_score(risks):
    return sum(risk["severity"] for risk in risks)


def prioritise_risks(risks):
    return sorted(risks, key=lambda x: x["severity"], reverse=True)
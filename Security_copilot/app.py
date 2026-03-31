from flask import Flask, render_template, request, session, send_file
from question_bank import QUESTIONS
from scoring import compute_scores
from ai_module import generate_ai_explanation
from pdf_report import build_pdf_report
from llm_module import generate_tailored_llm_output
import os
import uuid

app = Flask(__name__, template_folder="Templates", static_folder="Static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-secret-key-change-me")

# Simple in-memory report store for current session runs
REPORT_CACHE = {}


def extract_org_profile(form_data):
    return {
        "org_name": form_data.get("org_name", "").strip(),
        "sector": form_data.get("sector", "").strip(),
        "size": form_data.get("size", "").strip(),
        "it_team": form_data.get("it_team", "").strip(),
        "security_staff": form_data.get("security_staff", "").strip(),
        "web_app_type": form_data.get("web_app_type", "").strip(),
        "stores_customer_data": form_data.get("stores_customer_data", "").strip(),
        "processes_payments": form_data.get("processes_payments", "").strip(),
        "uses_cloud": form_data.get("uses_cloud", "").strip(),
        "uses_third_party_support": form_data.get("uses_third_party_support", "").strip(),
    }


@app.route("/")
def home():
    sections = {}
    for q in QUESTIONS:
        sections.setdefault(q["section"], []).append(q)
    return render_template("index.html", sections=sections)


@app.route("/analyze", methods=["POST"])
def analyze():
    org_profile = extract_org_profile(request.form)
    results = compute_scores(QUESTIONS, request.form)
    llm_output = generate_tailored_llm_output(org_profile, results)

    top_categories = results["category_results"][:3]
    ai_guidance = []

    for cat in top_categories:
        ai_guidance.append(generate_ai_explanation({
            "owasp": cat["owasp"],
            "issue": f"Risk level is {cat['level']} with {cat['percent']}% exposure based on questionnaire responses.",
            "severity": cat["level"]
        }))

    chart_labels = [c["owasp"] for c in results["category_results"]]
    chart_values = [c["percent"] for c in results["category_results"]]

    # Store full report server-side, not in cookie session
    report_id = str(uuid.uuid4())
    REPORT_CACHE[report_id] = {
        "results": results,
        "ai_guidance": ai_guidance,
        "org_profile": org_profile,
        "llm_output": llm_output
    }

    # Store only tiny reference in session
    session["latest_report_id"] = report_id

    return render_template(
        "report.html",
        results=results,
        ai_guidance=ai_guidance,
        llm_output=llm_output,
        org_profile=org_profile,
        chart_labels=chart_labels,
        chart_values=chart_values
    )


@app.route("/download_pdf")
def download_pdf():
    report_id = session.get("latest_report_id")

    if not report_id or report_id not in REPORT_CACHE:
        return "No report found. Please run an assessment first.", 400

    report_data = REPORT_CACHE[report_id]
    results = report_data["results"]
    ai_guidance = report_data["ai_guidance"]
    org_profile = report_data["org_profile"]
    llm_output = report_data["llm_output"]

    pdf_buffer = build_pdf_report(results, ai_guidance, org_profile, llm_output)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="SME_Security_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
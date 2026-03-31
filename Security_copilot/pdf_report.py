from io import BytesIO
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


class PDFWriter:
    def __init__(self, c, title):
        self.c = c
        self.width, self.height = A4
        self.left_margin = 50
        self.right_margin = 50
        self.top_margin = 50
        self.bottom_margin = 50
        self.y = self.height - self.top_margin

        self._draw_title(title)

    def _draw_title(self, title):
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(self.left_margin, self.y, title)
        self.y -= 30

    def _new_page(self):
        self.c.showPage()
        self.y = self.height - self.top_margin

    def _check_space(self, needed=20):
        if self.y < self.bottom_margin + needed:
            self._new_page()

    def write_heading(self, text, font_name="Helvetica-Bold", font_size=13, gap=12):
        self._check_space(30)
        self.c.setFont(font_name, font_size)
        self.c.drawString(self.left_margin, self.y, text)
        self.y -= gap

    def write_line(self, text, indent=0, font_name="Helvetica", font_size=10, gap=14):
        self._check_space(gap + 4)
        self.c.setFont(font_name, font_size)
        self.c.drawString(self.left_margin + indent, self.y, str(text))
        self.y -= gap

    def write_paragraph(self, text, indent=0, font_name="Helvetica", font_size=10, gap=6):
        text = str(text)
        max_width = self.width - self.left_margin - self.right_margin - indent
        lines = simpleSplit(text, font_name, font_size, max_width)

        self.c.setFont(font_name, font_size)

        for line in lines:
            self._check_space(16)
            self.c.drawString(self.left_margin + indent, self.y, line)
            self.y -= 14

        self.y -= gap


def build_pdf_report(
    results: Dict[str, Any],
    ai_guidance: List[str],
    org_profile: Dict[str, Any] = None,
    llm_output: Dict[str, Any] = None
) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w = PDFWriter(c, "SME Web Application Security Co-pilot Report")

    org_profile = org_profile or {}
    llm_output = llm_output or {}

    # Organisation profile
    w.write_heading("Organisation Profile")
    w.write_line(f"Organisation: {org_profile.get('org_name', 'N/A')}")
    w.write_line(f"Sector: {org_profile.get('sector', 'N/A')}")
    w.write_line(f"Company Size: {org_profile.get('size', 'N/A')}")
    w.write_line(f"Internal IT Team: {org_profile.get('it_team', 'N/A')}")
    w.write_line(f"Dedicated Security Staff: {org_profile.get('security_staff', 'N/A')}")
    w.write_line(f"Web Application Type: {org_profile.get('web_app_type', 'N/A')}")
    w.write_line(f"Stores Customer Data: {org_profile.get('stores_customer_data', 'N/A')}")
    w.write_line(f"Processes Payments: {org_profile.get('processes_payments', 'N/A')}")
    w.write_line(f"Uses Cloud Hosting: {org_profile.get('uses_cloud', 'N/A')}")
    w.write_line(f"Uses Third-Party Support: {org_profile.get('uses_third_party_support', 'N/A')}")
    w.y -= 8

    # Summary
    w.write_heading("Summary")
    w.write_line(f"Overall Risk Level: {results.get('overall_level', 'N/A')}", font_name="Helvetica-Bold", font_size=11)
    w.write_line(f"Overall Risk Exposure: {results.get('overall_percent', 'N/A')}%")
    w.write_line(f"ASVS L1 Controls Satisfied (Proxy): {results.get('asvs_compliance_percent', 'N/A')}%")
    w.y -= 8

    # Tailored LLM output
    w.write_heading("Tailored Executive Summary")
    w.write_paragraph(
        llm_output.get("executive_summary", "No executive summary available.")
    )

    w.write_heading("Business Impact")
    w.write_paragraph(
        llm_output.get("business_impact", "No business impact explanation available.")
    )

    w.write_heading("Priority Recommendations")
    priority_recommendations = llm_output.get("priority_recommendations", [])
    if priority_recommendations:
        for i, item in enumerate(priority_recommendations, start=1):
            w.write_paragraph(f"{i}. {item}", indent=10)
    else:
        w.write_line("Recommendations are included in the executive summary.", indent=10)

    w.write_heading("Quick Wins")
    quick_wins = llm_output.get("quick_wins", [])
    if quick_wins:
        for i, item in enumerate(quick_wins, start=1):
            w.write_paragraph(f"{i}. {item}", indent=10)
    else:
        w.write_line("No quick wins available.", indent=10)

    w.write_heading("Longer-Term Improvements")
    long_term = llm_output.get("long_term_improvements", [])
    if long_term:
        for i, item in enumerate(long_term, start=1):
            w.write_paragraph(f"{i}. {item}", indent=10)
    else:
        w.write_line("No longer-term improvements available.", indent=10)

    # OWASP risk breakdown
    w.write_heading("OWASP Risk Breakdown")
    for cat in results.get("category_results", []):
        w.write_line(
            f"{cat['owasp']} - {cat['percent']}% ({cat['level']})",
            indent=10
        )
    w.y -= 10

    # Remediation actions
    w.write_heading("Prioritised Remediation Actions")
    rems = results.get("remediation_actions", [])
    if not rems:
        w.write_line("No remediation actions required based on provided answers.", indent=10)
    else:
        for i, item in enumerate(rems, start=1):
            text = f"{i}. {item['owasp']} - {item['remediation']}"
            w.write_paragraph(text, indent=10)

    w.y -= 6

    # Existing simple AI guidance
    w.write_heading("AI Guidance (Top Risks)")
    if not ai_guidance:
        w.write_line("No AI guidance available.", indent=10)
    else:
        for idx, block in enumerate(ai_guidance, start=1):
            w.write_line(f"Guidance {idx}:", indent=10, font_name="Helvetica-Bold")

            for raw_line in block.strip().splitlines():
                line = raw_line.strip()
                if not line:
                    w.y -= 6
                    continue
                w.write_line(line, indent=20)

            w.y -= 8

    c.save()
    buffer.seek(0)
    return buffer
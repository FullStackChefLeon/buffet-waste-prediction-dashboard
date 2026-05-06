from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT


input_file = "reports/project_brief.md"
output_file = "reports/project_brief.pdf"


def clean_line(line: str) -> str:
    line = line.strip()
    line = line.replace("&", "&amp;")
    line = line.replace("<", "&lt;")
    line = line.replace(">", "&gt;")
    return line


styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    alignment=TA_LEFT,
    spaceAfter=16,
)

heading_style = ParagraphStyle(
    "CustomHeading",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    spaceBefore=12,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    spaceAfter=6,
)

bullet_style = ParagraphStyle(
    "CustomBullet",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    leftIndent=14,
    firstLineIndent=-8,
    spaceAfter=4,
)


doc = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=0.7 * inch,
    leftMargin=0.7 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
)

story = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    raw = line.strip()

    if not raw:
        story.append(Spacer(1, 6))
        continue

    if raw.startswith("# "):
        text = clean_line(raw.replace("# ", "", 1))
        story.append(Paragraph(text, title_style))

    elif raw.startswith("## "):
        text = clean_line(raw.replace("## ", "", 1))
        story.append(Paragraph(text, heading_style))

    elif raw.startswith("### "):
        text = clean_line(raw.replace("### ", "", 1))
        story.append(Paragraph(text, heading_style))

    elif raw.startswith("- "):
        text = clean_line(raw.replace("- ", "", 1))
        story.append(Paragraph(f"- {text}", bullet_style))

    else:
        text = clean_line(raw)
        story.append(Paragraph(text, body_style))

doc.build(story)

print(f"Created: {output_file}")

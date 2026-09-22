from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Image, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

# ── Color Palette ──────────────────────────────────────────────
BLUE = colors.HexColor("#2563eb")
DARK = colors.HexColor("#1e293b")
GRAY = colors.HexColor("#64748b")
LIGHT = colors.HexColor("#f1f5f9")
GREEN = colors.HexColor("#16a34a")
RED = colors.HexColor("#dc2626")


def build_pdf_report(
    narrative: str,
    trend_results: dict,
    outlier_results: dict,
    forecast_results: dict,
    chart_paths: list,
    output_path: str = "outputs/business_report.pdf"
) -> str:

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Custom Styles ──────────────────────────────────────────
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=28,
        textColor=BLUE,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=GRAY,
        spaceAfter=4,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=BLUE,
        spaceBefore=16,
        spaceAfter=8,
        fontName="Helvetica-Bold"
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        textColor=DARK,
        spaceAfter=6,
        leading=16
    )

    # ── Cover Page ─────────────────────────────────────────────
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("AI Business Report", title_style))
    story.append(Paragraph("Automated Analysis & Insights", subtitle_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))
    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE))
    story.append(Spacer(1, 0.3 * inch))

    # ── Key Metrics Table ──────────────────────────────────────
    story.append(Paragraph("Key Metrics at a Glance", heading_style))

    metrics_data = [
        ["Metric", "Value"],
        ["Total Revenue", f"${trend_results.get('total', 0):,.0f}"],
        ["Avg Monthly Revenue", f"${trend_results.get('average_monthly', 0):,.0f}"],
        ["Revenue Trend", trend_results.get('trend_direction', 'N/A').title()],
        ["Avg Growth Rate", f"{trend_results.get('avg_growth_rate', 0):.1f}%"],
        ["Best Month", trend_results.get('best_month', 'N/A')],
        ["Outliers Detected", str(outlier_results.get('total_outliers_found', 0))],
        ["Forecast Confidence", forecast_results.get('confidence', 'N/A').title()],
        ["Top Category", str(trend_results.get('top_category', 'N/A'))],
        ["Top Region", str(trend_results.get('top_region', 'N/A'))],
    ]

    metrics_table = Table(metrics_data, colWidths=[3 * inch, 3 * inch])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ROWHEIGHT", (0, 0), (-1, -1), 22),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── AI Narrative ───────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=LIGHT))
    story.append(Paragraph("Executive Summary", heading_style))

    for line in narrative.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Paragraph(line, body_style))

    story.append(PageBreak())

    # ── Charts ─────────────────────────────────────────────────
    chart_titles = {
        "chart_trend.png": "Revenue Trend Over Time",
        "chart_outliers.png": "Outlier Detection",
        "chart_forecast.png": "Revenue Forecast",
        "chart_breakdown.png": "Revenue Breakdown by Category & Region"
    }

    story.append(Paragraph("Visual Analysis", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    for chart_path in chart_paths:
        if os.path.exists(chart_path):
            filename = os.path.basename(chart_path)
            title = chart_titles.get(filename, filename)
            story.append(Paragraph(title, ParagraphStyle(
                "ChartTitle",
                parent=styles["Normal"],
                fontSize=11,
                textColor=DARK,
                fontName="Helvetica-Bold",
                spaceAfter=6
            )))
            story.append(Image(chart_path, width=6.5 * inch, height=3.2 * inch))
            story.append(Spacer(1, 0.3 * inch))

    # ── Forecast Table ─────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Forecast Details", heading_style))

    forecast_data = [["Month", "Forecasted Revenue", "Trend"]]
    forecasts = forecast_results.get("forecasts", [])
    for i, f in enumerate(forecasts):
        trend_arrow = "↑" if i == 0 or f["forecasted_revenue"] >= forecasts[i-1]["forecasted_revenue"] else "↓"
        forecast_data.append([
            f["month"],
            f"${f['forecasted_revenue']:,.0f}",
            trend_arrow
        ])

    forecast_table = Table(forecast_data, colWidths=[2.5 * inch, 2.5 * inch, 1 * inch])
    forecast_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWHEIGHT", (0, 0), (-1, -1), 24),
    ]))
    story.append(forecast_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Footer Note ────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=LIGHT))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "This report was autonomously generated by an AI Business Report Agent "
        "using LangGraph, Groq LLM, Pandas, and ReportLab.",
        ParagraphStyle("Footer", parent=styles["Normal"],
                       fontSize=8, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    print(f"  → PDF saved to {output_path}")
    return output_path
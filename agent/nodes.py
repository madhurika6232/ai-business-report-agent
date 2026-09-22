from agent.state import ReportState
from tools.analyzer import (
    load_and_summarize,
    run_trend_analysis,
    run_outlier_detection,
    run_forecast
)
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os
import pandas as pd

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

# ── Node 1: Load Data ──────────────────────────────────────────
def load_data_node(state: ReportState) -> dict:
    print("📂 Loading data...")
    df, summary = load_and_summarize(state["csv_path"])
    df.to_csv("outputs/working_data.csv", index=False)
    return {"df_summary": summary}

# ── Node 2: AI Decides Which Analyses to Run ──────────────────
def decide_analyses_node(state: ReportState) -> dict:
    print("🤔 AI is deciding which analyses to run...")
    llm = get_llm()

    prompt = f"""You are a data analyst. Based on this dataset summary, decide which analyses to run.

DATASET SUMMARY:
{state["df_summary"]}

AVAILABLE ANALYSES:
- "trends": Run if there are date columns and numeric columns
- "outliers": Run if there are numeric columns with potential anomalies
- "forecast": Run if there are date columns and enough rows (>20) to forecast

Respond ONLY with a valid JSON array.
Example: ["trends", "outliers", "forecast"]
Return ONLY the JSON array, no explanation."""

    response = llm.invoke(prompt)
    raw = response.content.strip().replace("```json", "").replace("```", "").strip()
    analyses = json.loads(raw)
    print(f"✅ AI decided to run: {analyses}")
    return {"analyses_to_run": analyses}

# ── Node 3: Trend Analysis ─────────────────────────────────────
def trend_analysis_node(state: ReportState) -> dict:
    print("📈 Running trend analysis...")
    df = pd.read_csv("outputs/working_data.csv", parse_dates=["date"])
    results = run_trend_analysis(df)
    print(f"  → Trend: {results.get('trend_direction')} | R²: {results.get('r_squared')}")
    return {"trend_results": results}

# ── Node 4: Outlier Detection ──────────────────────────────────
def outlier_detection_node(state: ReportState) -> dict:
    print("🔍 Detecting outliers...")
    df = pd.read_csv("outputs/working_data.csv")
    results = run_outlier_detection(df)
    print(f"  → Found {results.get('total_outliers_found')} outliers")
    return {"outlier_results": results}

# ── Node 5: Forecast ───────────────────────────────────────────
def forecast_node(state: ReportState) -> dict:
    print("🔮 Forecasting next 3 months...")
    df = pd.read_csv("outputs/working_data.csv", parse_dates=["date"])
    results = run_forecast(df, periods=3)
    print(f"  → Forecast trend: {results.get('trend')} | Confidence: {results.get('confidence')}")
    return {"forecast_results": results}

# ── Placeholder nodes (filled in Step 5) ──────────────────────
def generate_charts_node(state: ReportState) -> dict:
    print("📊 Generating charts...")
    from tools.visualizer import (
        generate_trend_chart,
        generate_outlier_chart,
        generate_forecast_chart,
        generate_category_chart
    )
    df = pd.read_csv("outputs/working_data.csv", parse_dates=["date"])
    
    paths = []

    if state.get("trend_results"):
        paths.append(generate_trend_chart(state["trend_results"]))
        print("  → Trend chart done")

    if state.get("outlier_results"):
        paths.append(generate_outlier_chart(df, state["outlier_results"]))
        print("  → Outlier chart done")

    if state.get("forecast_results") and state.get("trend_results"):
        paths.append(generate_forecast_chart(
            state["trend_results"], state["forecast_results"]
        ))
        print("  → Forecast chart done")

    paths.append(generate_category_chart(df))
    print("  → Breakdown chart done")

    return {"chart_paths": paths}

def write_narrative_node(state: ReportState) -> dict:
    print("✍️ Writing AI narrative...")
    llm = get_llm()

    prompt = f"""You are a senior business analyst writing an executive summary report.

Based on the analysis results below, write a professional plain-English narrative summary.
Structure it with these sections:
1. **Executive Summary** (2-3 sentences overview)
2. **Revenue Trends** (what the trend data shows)
3. **Anomalies & Outliers** (what was flagged and why it matters)
4. **Forecast & Outlook** (what's expected in coming months)
5. **Recommendations** (3 bullet points of actionable advice)

TREND ANALYSIS RESULTS:
{json.dumps(state.get("trend_results", {}), indent=2)}

OUTLIER DETECTION RESULTS:
{json.dumps(state.get("outlier_results", {}), indent=2)}

FORECAST RESULTS:
{json.dumps(state.get("forecast_results", {}), indent=2)}

Write in a confident, professional tone. Use specific numbers from the data.
Keep it concise — around 300 words total."""

    response = llm.invoke(prompt)
    narrative = response.content.strip()
    print("  → Narrative written!")
    return {"narrative": narrative}

def build_pdf_node(state: ReportState) -> dict:
    print("📄 Building PDF report...")
    from tools.report_builder import build_pdf_report

    path = build_pdf_report(
        narrative=state.get("narrative", ""),
        trend_results=state.get("trend_results", {}),
        outlier_results=state.get("outlier_results", {}),
        forecast_results=state.get("forecast_results", {}),
        chart_paths=state.get("chart_paths", []),
    )
    return {"report_path": path}
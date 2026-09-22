import streamlit as st
import os
import tempfile
import time
from agent.graph import build_graph

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Report Agent",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2563eb;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .status-box {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────
st.markdown('<div class="main-header">📊 AI Business Report Agent</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your sales CSV and get a full AI-powered business report in seconds</div>',
            unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.markdown("### How it works")
    st.markdown("""
    1. 📂 **Upload** your CSV file
    2. 🤔 **AI decides** which analyses to run
    3. 📈 **Trends, outliers & forecast** are computed
    4. 📊 **Charts** are generated automatically
    5. ✍️ **AI writes** a business narrative
    6. 📄 **PDF report** is ready to download
    """)
    st.divider()
    st.markdown("### Required CSV Columns")
    st.markdown("""
    - `date` — transaction date
    - `revenue` — sales revenue
    - Any other columns are bonus!
    """)
    st.divider()
    st.markdown("**Built with**")
    st.markdown("LangGraph · Groq LLM · Pandas · ReportLab")

# ── Main Area ──────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📂 Upload Your Data")
    uploaded_file = st.file_uploader(
        "Drop your CSV file here",
        type=["csv"],
        help="Must contain at least a date and revenue column"
    )

    if uploaded_file:
        import pandas as pd
        df_preview = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        st.success(f"✅ Loaded: {len(df_preview)} rows × {len(df_preview.columns)} columns")
        st.dataframe(df_preview.head(5), use_container_width=True)

with col2:
    st.markdown("### ⚙️ Report Settings")
    forecast_months = st.slider("Forecast months ahead", 1, 6, 3)
    include_outliers = st.checkbox("Include outlier detection", value=True)
    include_forecast = st.checkbox("Include revenue forecast", value=True)
    st.markdown("---")
    generate_btn = st.button(
        "🚀 Generate Report",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None
    )

# ── Run Agent ──────────────────────────────────────────────────
if generate_btn and uploaded_file:
    st.divider()
    st.markdown("### 🤖 Agent Running...")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Progress tracking
    progress = st.progress(0)
    status = st.empty()

    steps = [
        (10, "📂 Loading and analyzing your data..."),
        (25, "🤔 AI is deciding which analyses to run..."),
        (45, "📈 Running trend, outlier & forecast analysis..."),
        (65, "📊 Generating charts..."),
        (80, "✍️ Writing AI narrative..."),
        (95, "📄 Building PDF report..."),
    ]

    # Animate progress while agent runs
    import threading
    result_container = {}
    error_container = {}

    def run_agent():
        try:
            graph = build_graph()
            result = graph.invoke({
                "csv_path": tmp_path,
                "chart_paths": []
            })
            result_container["result"] = result
        except Exception as e:
            error_container["error"] = str(e)

    thread = threading.Thread(target=run_agent)
    thread.start()

    step_idx = 0
    while thread.is_alive():
        if step_idx < len(steps):
            prog, msg = steps[step_idx]
            progress.progress(prog)
            status.markdown(f'<div class="status-box">{msg}</div>',
                          unsafe_allow_html=True)
            step_idx += 1
        time.sleep(3)

    thread.join()
    progress.progress(100)
    status.markdown('<div class="status-box">✅ Report complete!</div>',
                   unsafe_allow_html=True)

    # ── Handle Errors ──────────────────────────────────────────
    if "error" in error_container:
        st.error(f"❌ Error: {error_container['error']}")
        st.stop()

    result = result_container["result"]

    # ── Results Dashboard ──────────────────────────────────────
    st.divider()
    st.markdown("### 📊 Results Dashboard")

    trend = result.get("trend_results", {})
    outliers = result.get("outlier_results", {})
    forecast = result.get("forecast_results", {})

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Revenue",
                  f"${trend.get('total', 0):,.0f}")
    with m2:
        st.metric("Avg Monthly Revenue",
                  f"${trend.get('average_monthly', 0):,.0f}")
    with m3:
        direction = trend.get('trend_direction', 'N/A')
        st.metric("Trend",
                  f"{'↑' if direction == 'upward' else '↓'} {direction.title()}")
    with m4:
        st.metric("Outliers Found",
                  outliers.get('total_outliers_found', 0))

    # Charts
    st.markdown("### 📈 Generated Charts")
    chart_paths = result.get("chart_paths", [])

    if chart_paths:
        c1, c2 = st.columns(2)
        for i, path in enumerate(chart_paths):
            if os.path.exists(path):
                if i % 2 == 0:
                    with c1:
                        st.image(path, use_container_width=True)
                else:
                    with c2:
                        st.image(path, use_container_width=True)

    # Narrative
    st.markdown("### ✍️ AI Executive Summary")
    narrative = result.get("narrative", "")
    if narrative:
        st.markdown(narrative)

    # Forecast table
    if forecast.get("forecasts"):
        st.markdown("### 🔮 Revenue Forecast")
        import pandas as pd
        forecast_df = pd.DataFrame(forecast["forecasts"])
        forecast_df.columns = ["Month", "Forecasted Revenue ($)"]
        forecast_df["Forecasted Revenue ($)"] = forecast_df["Forecasted Revenue ($)"].apply(
            lambda x: f"${x:,.0f}"
        )
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    # Download PDF
    st.divider()
    report_path = result.get("report_path", "outputs/business_report.pdf")
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download Full PDF Report",
                data=f,
                file_name="business_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

    # Cleanup temp file
    os.unlink(tmp_path)
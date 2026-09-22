import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import os

# Clean consistent style
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#f8f9fa",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.family": "sans-serif"
})

OUTPUT_DIR = "outputs"

def generate_trend_chart(trend_results: dict) -> str:
    """Line chart of monthly revenue trend."""
    monthly = trend_results["monthly_data"]
    months = [d["month"] for d in monthly]
    values = [d[trend_results["value_column"]] for d in monthly]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, values, marker="o", linewidth=2.5,
            color="#2563eb", markersize=6, label="Actual Revenue")

    # Trend line
    x = np.arange(len(months))
    z = np.polyfit(x, values, 1)
    p = np.poly1d(z)
    ax.plot(months, p(x), "--", color="#dc2626",
            linewidth=1.5, alpha=0.7, label="Trend Line")

    ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart_trend.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def generate_outlier_chart(df: pd.DataFrame, outlier_results: dict) -> str:
    """Scatter plot highlighting outliers in revenue."""
    numeric_cols = list(df.select_dtypes(include="number").columns)
    value_col = "revenue" if "revenue" in numeric_cols else numeric_cols[0]

    fig, ax = plt.subplots(figsize=(10, 5))

    # Detect outliers
    from scipy import stats
    z_scores = np.abs(stats.zscore(df[value_col].dropna()))
    is_outlier = z_scores > 2.5

    ax.scatter(range(len(df)), df[value_col],
               color="#2563eb", alpha=0.6, s=60, label="Normal")
    ax.scatter(np.where(is_outlier)[0], df[value_col][is_outlier],
               color="#dc2626", s=100, zorder=5, label="Outlier")

    ax.set_title(f"Outlier Detection — {value_col}", fontsize=14,
                 fontweight="bold", pad=15)
    ax.set_xlabel("Record Index")
    ax.set_ylabel(f"{value_col} ($)")
    ax.legend()
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart_outliers.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def generate_forecast_chart(trend_results: dict, forecast_results: dict) -> str:
    """Bar chart showing actual + forecasted revenue."""
    monthly = trend_results["monthly_data"]
    col = trend_results["value_column"]

    actual_months = [d["month"] for d in monthly]
    actual_values = [d[col] for d in monthly]

    forecast_months = [f["month"] for f in forecast_results["forecasts"]]
    forecast_values = [f["forecasted_revenue"] for f in forecast_results["forecasts"]]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(actual_months, actual_values, color="#2563eb",
           alpha=0.8, label="Actual")
    ax.bar(forecast_months, forecast_values, color="#16a34a",
           alpha=0.8, label="Forecast")

    # Divider line
    ax.axvline(x=len(actual_months) - 0.5, color="#dc2626",
               linestyle="--", linewidth=1.5, label="Forecast Start")

    ax.set_title("Revenue: Actual vs Forecast", fontsize=14,
                 fontweight="bold", pad=15)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart_forecast.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def generate_category_chart(df: pd.DataFrame) -> str:
    """Pie chart of revenue by category."""
    numeric_cols = list(df.select_dtypes(include="number").columns)
    value_col = "revenue" if "revenue" in numeric_cols else numeric_cols[0]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Category breakdown
    if "category" in df.columns:
        cat_data = df.groupby("category")[value_col].sum()
        axes[0].pie(cat_data.values, labels=cat_data.index,
                    autopct="%1.1f%%", startangle=90,
                    colors=["#2563eb", "#16a34a", "#dc2626", "#d97706"])
        axes[0].set_title("Revenue by Category", fontsize=13, fontweight="bold")
    else:
        axes[0].text(0.5, 0.5, "No category column",
                     ha="center", va="center")

    # Region breakdown
    if "region" in df.columns:
        reg_data = df.groupby("region")[value_col].sum()
        axes[1].pie(reg_data.values, labels=reg_data.index,
                    autopct="%1.1f%%", startangle=90,
                    colors=["#7c3aed", "#0891b2", "#be185d", "#065f46"])
        axes[1].set_title("Revenue by Region", fontsize=13, fontweight="bold")
    else:
        axes[1].text(0.5, 0.5, "No region column",
                     ha="center", va="center")

    plt.suptitle("Revenue Breakdown", fontsize=14,
                 fontweight="bold", y=1.02)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart_breakdown.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path
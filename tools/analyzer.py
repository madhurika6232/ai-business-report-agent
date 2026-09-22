import pandas as pd
import numpy as np
from scipy import stats
import json

def load_and_summarize(csv_path: str) -> tuple[pd.DataFrame, str]:
    """Load CSV and generate a text summary for the AI to read."""
    df = pd.read_csv(csv_path)
    
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])

    summary = {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "numeric_columns": list(df.select_dtypes(include='number').columns),
        "date_columns": date_cols,
        "categorical_columns": list(df.select_dtypes(include='object').columns),
        "sample_values": df.head(3).to_dict(orient='records'),
        "numeric_stats": df.describe().round(2).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "date_range": {
            col: {
                "min": str(df[col].min()),
                "max": str(df[col].max())
            } for col in date_cols
        }
    }

    return df, json.dumps(summary, indent=2, default=str)


def run_trend_analysis(df: pd.DataFrame) -> dict:
    """Analyze revenue trends over time."""
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    numeric_cols = list(df.select_dtypes(include='number').columns)

    if not date_cols or not numeric_cols:
        return {"error": "No date or numeric columns found"}

    date_col = date_cols[0]
    
    # Focus on revenue if exists, else first numeric
    value_col = "revenue" if "revenue" in numeric_cols else numeric_cols[0]

    # Monthly aggregation
    df_copy = df.copy()
    df_copy["month"] = df_copy[date_col].dt.to_period("M")
    monthly = df_copy.groupby("month")[value_col].sum().reset_index()
    monthly["month"] = monthly["month"].astype(str)

    # Growth rate
    monthly["growth_rate"] = monthly[value_col].pct_change() * 100

    # Linear trend
    x = np.arange(len(monthly))
    y = monthly[value_col].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Top performing category
    top_category = None
    if "category" in df.columns:
        top_category = df.groupby("category")[value_col].sum().idxmax()

    # Top performing region
    top_region = None
    if "region" in df.columns:
        top_region = df.groupby("region")[value_col].sum().idxmax()

    return {
        "value_column": value_col,
        "monthly_data": monthly.to_dict(orient="records"),
        "total": round(float(y.sum()), 2),
        "average_monthly": round(float(y.mean()), 2),
        "trend_slope": round(float(slope), 2),
        "trend_direction": "upward" if slope > 0 else "downward",
        "r_squared": round(float(r_value ** 2), 3),
        "avg_growth_rate": round(float(monthly["growth_rate"].mean(skipna=True)), 2),
        "best_month": monthly.loc[monthly[value_col].idxmax(), "month"],
        "worst_month": monthly.loc[monthly[value_col].idxmin(), "month"],
        "top_category": top_category,
        "top_region": top_region
    }


def run_outlier_detection(df: pd.DataFrame) -> dict:
    """Detect outliers using Z-score method."""
    numeric_cols = list(df.select_dtypes(include='number').columns)
    
    if not numeric_cols:
        return {"error": "No numeric columns found"}

    outliers_found = {}

    for col in numeric_cols:
        col_data = df[col].dropna()
        z_scores = np.abs(stats.zscore(col_data))
        outlier_mask = z_scores > 2.5
        outlier_indices = col_data[outlier_mask].index.tolist()

        if outlier_indices:
            outliers_found[col] = {
                "count": len(outlier_indices),
                "values": df.loc[outlier_indices, col].round(2).tolist()[:5],
                "mean": round(float(col_data.mean()), 2),
                "std": round(float(col_data.std()), 2),
                "min_outlier": round(float(df.loc[outlier_indices, col].min()), 2),
                "max_outlier": round(float(df.loc[outlier_indices, col].max()), 2),
            }

    return {
        "columns_checked": numeric_cols,
        "outliers": outliers_found,
        "total_outliers_found": sum(v["count"] for v in outliers_found.values()),
        "method": "Z-score (threshold: 2.5)"
    }


def run_forecast(df: pd.DataFrame, periods: int = 3) -> dict:
    """Simple linear regression forecast for next N months."""
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    numeric_cols = list(df.select_dtypes(include='number').columns)

    if not date_cols or not numeric_cols:
        return {"error": "No date or numeric columns found"}

    date_col = date_cols[0]
    value_col = "revenue" if "revenue" in numeric_cols else numeric_cols[0]

    df_copy = df.copy()
    df_copy["month"] = df_copy[date_col].dt.to_period("M")
    monthly = df_copy.groupby("month")[value_col].sum().reset_index()

    x = np.arange(len(monthly))
    y = monthly[value_col].values
    slope, intercept, r_value, _, _ = stats.linregress(x, y)

    # Forecast next N periods
    future_x = np.arange(len(monthly), len(monthly) + periods)
    future_y = slope * future_x + intercept

    last_month = monthly["month"].iloc[-1]
    future_months = [
        str(last_month + i + 1) for i in range(periods)
    ]

    forecast_data = [
        {"month": m, "forecasted_revenue": round(float(v), 2)}
        for m, v in zip(future_months, future_y)
    ]

    return {
        "value_column": value_col,
        "method": "Linear Regression",
        "r_squared": round(float(r_value ** 2), 3),
        "forecast_periods": periods,
        "forecasts": forecast_data,
        "trend": "growing" if slope > 0 else "declining",
        "confidence": "high" if r_value ** 2 > 0.8 else "medium" if r_value ** 2 > 0.5 else "low"
    }
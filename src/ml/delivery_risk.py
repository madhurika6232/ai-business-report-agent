"""
Late-Delivery Risk Prediction

Business goal:
Identify orders at elevated risk of late delivery early enough
for operations teams to investigate.

Target:
is_late

Success criteria:
- Use only information available before delivery.
- Prioritize detection of late orders over raw accuracy.
- Evaluate precision, recall, F1, ROC-AUC, and PR-AUC.
- Produce a risk probability rather than only a class label.
- Provide interpretable predictive signals.
"""

import pandas as pd


LEAKAGE_COLUMNS = [
    "order_delivered_customer_date",
    "delivery_days",
    "delay_days",
    "review_score",
    "is_negative_review",
    "review_comment_message",
    "has_review_comment",
]


def build_delivery_risk_dataset(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Build a leakage-safe dataset for late-delivery prediction."""

    df = orders[
        orders["is_late"].notna()
    ].copy()

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    df["order_estimated_delivery_date"] = pd.to_datetime(
    df["order_estimated_delivery_date"]
   )

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    # Target
    df["target_is_late"] = (
        df["is_late"]
        .astype(str)
        .str.lower()
        .map({
            "true": 1,
            "false": 0,
        })
    )

    # Features known at/near order placement
    df["order_month_num"] = (
        df["order_purchase_timestamp"].dt.month
    )

    df["order_day_of_week"] = (
        df["order_purchase_timestamp"].dt.dayofweek
    )

    df["order_hour"] = (
        df["order_purchase_timestamp"].dt.hour
    )

    feature_columns = [
        "order_month_num",
        "order_day_of_week",
        "order_hour",
        "order_revenue",
        "freight_value",
        "item_count",
        "category_count",
        "seller_count",
        "customer_state",
        "estimated_delivery_days",
    ]

    result = df[
        [
            "order_id",
            "order_purchase_timestamp",
        ]
        + feature_columns
        + ["target_is_late"]
    ].copy()

    return result

def time_based_split(
    data: pd.DataFrame,
    cutoff_date: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split delivery-risk data chronologically."""

    df = data.copy()

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    cutoff = pd.to_datetime(cutoff_date)

    train = df[
        df["order_purchase_timestamp"] < cutoff
    ].copy()

    test = df[
        df["order_purchase_timestamp"] >= cutoff
    ].copy()

    if train.empty or test.empty:
        raise ValueError(
            "Time split produced an empty train or test dataset."
        )

    return train, test

def baseline_predictions(
    data: pd.DataFrame,
) -> list[int]:
    """Predict every order as on-time for baseline comparison."""

    return [0] * len(data)

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "order_month_num",
    "order_day_of_week",
    "order_hour",
    "order_revenue",
    "freight_value",
    "item_count",
    "category_count",
    "seller_count",
    "seller_historical_orders",
    "seller_historical_late_rate",
    "estimated_delivery_days",
]

CATEGORICAL_FEATURES = [
    "customer_state",
]

MODEL_FEATURES = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)


def build_logistic_pipeline() -> Pipeline:
    """Build a class-weighted logistic regression pipeline."""

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

from sklearn.ensemble import RandomForestClassifier

def build_random_forest_pipeline() -> Pipeline:
    """Build a class-weighted random forest delivery-risk model."""

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

def add_historical_seller_features(
    risk_data: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Add leakage-safe historical seller performance features."""

    seller_orders = orders[
        [
            "order_id",
            "order_purchase_timestamp",
            "seller_ids",
            "is_late",
        ]
    ].copy()

    seller_orders = seller_orders[
        seller_orders["seller_ids"].notna()
        & seller_orders["is_late"].notna()
    ].copy()

    # Keep only single-seller orders for a clean historical signal.
    seller_orders = seller_orders[
        ~seller_orders["seller_ids"].str.contains(
            ",",
            regex=False,
        )
    ].copy()

    seller_orders["order_purchase_timestamp"] = pd.to_datetime(
        seller_orders["order_purchase_timestamp"]
    )

    seller_orders["is_late_numeric"] = (
        seller_orders["is_late"]
        .astype(str)
        .str.lower()
        .map({
            "true": 1,
            "false": 0,
        })
    )

    seller_orders = seller_orders.sort_values(
        [
            "seller_ids",
            "order_purchase_timestamp",
        ]
    )

    # Number of previous orders from this seller.
    seller_orders["seller_historical_orders"] = (
        seller_orders
        .groupby("seller_ids")
        .cumcount()
    )

    # Previous late orders only — current order is excluded.
    seller_orders["previous_late_orders"] = (
        seller_orders
        .groupby("seller_ids")["is_late_numeric"]
        .cumsum()
        - seller_orders["is_late_numeric"]
    )

    seller_orders["seller_historical_late_rate"] = (
        seller_orders["previous_late_orders"]
        / seller_orders["seller_historical_orders"]
    )

    seller_orders[
        "seller_historical_late_rate"
    ] = (
        seller_orders[
            "seller_historical_late_rate"
        ]
        .fillna(0)
    )

    historical_features = seller_orders[
        [
            "order_id",
            "seller_historical_orders",
            "seller_historical_late_rate",
        ]
    ]

    result = risk_data.merge(
        historical_features,
        on="order_id",
        how="left",
    )

    result["seller_historical_orders"] = (
        result["seller_historical_orders"]
        .fillna(0)
    )

    result["seller_historical_late_rate"] = (
        result["seller_historical_late_rate"]
        .fillna(0)
    )

    return result

def classify_risk_level(
    probability: float,
) -> str:
    """Convert late-delivery probability into an operational risk level."""

    if not 0 <= probability <= 1:
        raise ValueError(
            "Probability must be between 0 and 1."
        )

    if probability >= 0.80:
        return "critical"

    if probability >= 0.60:
        return "high"

    if probability >= 0.40:
        return "medium"

    return "low"

def get_feature_importance(
    model: Pipeline,
    top_n: int = 15,
) -> pd.DataFrame:
    """Return the strongest predictive signals from the logistic model."""

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than 0."
        )

    preprocessor = model.named_steps[
        "preprocessor"
    ]

    classifier = model.named_steps[
        "model"
    ]

    feature_names = (
        preprocessor.get_feature_names_out()
    )

    coefficients = classifier.coef_[0]

    importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients,
    })

    importance["absolute_importance"] = (
        importance["coefficient"].abs()
    )

    importance["risk_direction"] = (
        importance["coefficient"]
        .apply(
            lambda value:
            "higher_risk"
            if value > 0
            else "lower_risk"
        )
    )

    return (
        importance
        .sort_values(
            "absolute_importance",
            ascending=False,
        )
        .head(top_n)
        .reset_index(drop=True)
    )
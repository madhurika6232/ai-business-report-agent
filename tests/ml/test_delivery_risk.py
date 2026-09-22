from pathlib import Path

import pandas as pd
import pytest

from src.ml.delivery_risk import (
    LEAKAGE_COLUMNS,
    MODEL_FEATURES,
    add_historical_seller_features,
    build_delivery_risk_dataset,
    build_logistic_pipeline,
    classify_risk_level,
    get_feature_importance,
    time_based_split,
)

from src.ml.evaluation import (
    calculate_classification_metrics,
    evaluate_thresholds,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


@pytest.fixture(scope="module")
def risk_data(orders):
    data = build_delivery_risk_dataset(orders)

    return add_historical_seller_features(
        data,
        orders,
    )


@pytest.fixture(scope="module")
def trained_model(risk_data):
    train, test = time_based_split(
        risk_data,
        cutoff_date="2018-06-01",
    )

    model = build_logistic_pipeline()

    model.fit(
        train[MODEL_FEATURES],
        train["target_is_late"],
    )

    return model, train, test


def test_delivery_risk_dataset(risk_data):
    assert len(risk_data) == 96204

    assert risk_data[
        "target_is_late"
    ].isin([0, 1]).all()

    for column in LEAKAGE_COLUMNS:
        assert column not in risk_data.columns


def test_historical_seller_features(risk_data):
    assert risk_data[
        "seller_historical_orders"
    ].notna().all()

    assert risk_data[
        "seller_historical_late_rate"
    ].between(0, 1).all()


def test_time_split(risk_data):
    train, test = time_based_split(
        risk_data,
        cutoff_date="2018-06-01",
    )

    assert len(train) == 77601
    assert len(test) == 18603

    assert (
        train["order_purchase_timestamp"].max()
        < test["order_purchase_timestamp"].min()
    )


def test_logistic_model(trained_model):
    model, train, test = trained_model

    probabilities = model.predict_proba(
        test[MODEL_FEATURES]
    )[:, 1]

    predictions = (
        probabilities >= 0.60
    ).astype(int)

    metrics = calculate_classification_metrics(
        test["target_is_late"],
        predictions,
        probabilities,
    )

    assert metrics["roc_auc"] == pytest.approx(
        0.7058,
        abs=0.01,
    )

    assert metrics["recall"] > 0.50

    assert (
        (probabilities >= 0)
        & (probabilities <= 1)
    ).all()


def test_threshold_evaluation(trained_model):
    model, train, test = trained_model

    probabilities = model.predict_proba(
        test[MODEL_FEATURES]
    )[:, 1]

    result = evaluate_thresholds(
        test["target_is_late"],
        probabilities,
        thresholds=[0.5, 0.6, 0.7],
    )

    assert len(result) == 3

    threshold_06 = result[
        result["threshold"] == 0.6
    ].iloc[0]

    assert threshold_06["recall"] > 0.50


def test_risk_levels():
    assert classify_risk_level(0.20) == "low"
    assert classify_risk_level(0.45) == "medium"
    assert classify_risk_level(0.65) == "high"
    assert classify_risk_level(0.85) == "critical"

    with pytest.raises(ValueError):
        classify_risk_level(1.5)


def test_feature_importance(trained_model):
    model, train, test = trained_model

    result = get_feature_importance(
        model,
        top_n=10,
    )

    assert len(result) == 10
    assert result["coefficient"].notna().all()

    assert result["risk_direction"].isin(
        ["higher_risk", "lower_risk"]
    ).all()
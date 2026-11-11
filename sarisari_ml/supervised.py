"""
supervised.py - SUPERVISED LEARNING: predict a day's sales.

"Supervised" means we train on examples where the right answer is known.
Here the inputs are facts about a day, and the answer is that day's sales.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# The input columns (X). The column we predict (y) is daily_sales.
FEATURES = ["day_of_week", "is_weekend", "is_payday", "is_holiday", "is_rainy", "temperature"]
TARGET = "daily_sales"


def train_models(sales):
    """Train both models and return them with their test results."""
    X = sales[FEATURES]
    y = sales[TARGET]

    # Keep 20% of the days hidden from training so we can test on new data.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the two models on the same training data.
    forest = RandomForestRegressor(n_estimators=100, random_state=42)
    forest.fit(X_train, y_train)

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    # Predict the hidden test days.
    forest_predictions = forest.predict(X_test)
    linear_predictions = linear.predict(X_test)

    # MAE = average peso error (lower is better).
    # R2 = share of the sales pattern explained (closer to 1 is better).
    metrics = pd.DataFrame({
        "Model": ["Random Forest", "Linear Regression"],
        "MAE (pesos)": [
            mean_absolute_error(y_test, forest_predictions),
            mean_absolute_error(y_test, linear_predictions),
        ],
        "R2 Score": [
            r2_score(y_test, forest_predictions),
            r2_score(y_test, linear_predictions),
        ],
    })

    # How much the Random Forest relied on each input, largest first.
    importances = pd.DataFrame({
        "feature": FEATURES,
        "importance": forest.feature_importances_,
    }).sort_values("importance", ascending=False)

    # Actual vs predicted for the test days, in calendar order, for the chart.
    comparison = pd.DataFrame({
        "Actual": y_test,
        "Random Forest": forest_predictions,
        "Linear Regression": linear_predictions,
    }).sort_index()
    comparison.index.name = "day"

    return {
        "forest": forest,
        "linear": linear,
        "metrics": metrics,
        "importances": importances,
        "comparison": comparison,
    }


def predict_sales(model, day_of_week, is_payday, is_holiday, is_rainy, temperature):
    """Predict sales for one day using a trained model."""
    # Weekend can be worked out from the day: 5 = Saturday, 6 = Sunday.
    is_weekend = int(day_of_week >= 5)

    # The model needs the same columns, in the same order, as in training.
    one_day = pd.DataFrame(
        [[day_of_week, is_weekend, int(is_payday), int(is_holiday), int(is_rainy), temperature]],
        columns=FEATURES,
    )
    return float(model.predict(one_day)[0])


if __name__ == "__main__":
    # Quick self-test: python supervised.py
    from data import generate_sales

    results = train_models(generate_sales())
    print(results["metrics"].round(3))
    print(results["importances"].round(3))

    # A rainy Tuesday compared with a sunny payday Saturday.
    for name in ["forest", "linear"]:
        normal_day = predict_sales(results[name], 1, False, False, True, 29)
        payday = predict_sales(results[name], 5, True, False, False, 32)
        print(name, "rainy Tuesday:", round(normal_day), "| payday Saturday:", round(payday))

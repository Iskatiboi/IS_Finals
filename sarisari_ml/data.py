"""
data.py - Creates the synthetic (made-up but realistic) data for our store.

Nothing is downloaded. Everything is generated with numpy using a fixed seed,
so the same seed always gives exactly the same data.
"""

import numpy as np
import pandas as pd

# Philippine holidays written as (month, day).
HOLIDAYS = {
    (1, 1),    # New Year's Day
    (4, 9),    # Araw ng Kagitingan
    (5, 1),    # Labor Day
    (6, 12),   # Independence Day
    (8, 21),   # Ninoy Aquino Day
    (11, 1),   # All Saints' Day
    (11, 30),  # Bonifacio Day
    (12, 25),  # Christmas Day
    (12, 30),  # Rizal Day
    (12, 31),  # New Year's Eve
}


def generate_sales(n_days=365, seed=42):
    """Create one row of store sales per day."""
    rng = np.random.default_rng(seed)

    # A calendar, so paydays and holidays fall on real dates.
    dates = pd.date_range("2025-01-01", periods=n_days, freq="D")

    # 0 = Monday ... 6 = Sunday. Saturday (5) and Sunday (6) are the weekend.
    day_of_week = dates.dayofweek.to_numpy()
    is_weekend = (day_of_week >= 5).astype(int)

    # Payday is the 15th and the 30th, and also the day after each one.
    # (February has no 30th, so it only gets the mid-month payday here.)
    today = dates.day.to_numpy()
    yesterday = pd.date_range("2024-12-31", periods=n_days, freq="D").day.to_numpy()
    is_payday = (np.isin(today, [15, 30]) | np.isin(yesterday, [15, 30])).astype(int)

    # Check each date against our holiday list.
    is_holiday = np.array([(d.month, d.day) in HOLIDAYS for d in dates]).astype(int)

    # About 30% of days are rainy, and rainy days are a little cooler.
    is_rainy = (rng.random(n_days) < 0.30).astype(int)
    temperature = np.round(rng.normal(31, 2, n_days) - 2 * is_rainy, 1)

    # The sales rule: start at a base, then add or subtract each effect.
    noise = rng.normal(0, 100, n_days)
    daily_sales = (
        1500
        + 300 * is_weekend
        + 800 * is_payday
        + 500 * is_holiday
        - 300 * is_rainy
        + noise
    )

    return pd.DataFrame({
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "is_payday": is_payday,
        "is_holiday": is_holiday,
        "is_rainy": is_rainy,
        "temperature": temperature,
        "daily_sales": np.round(daily_sales, 2),
    })


# Each item is (name, typical price in pesos, group).
# The group is only used here to create realistic numbers.
# The KMeans model never sees it: it has to find the groups by itself.
PRODUCT_LIST = [
    # Cheap items that sell very quickly
    ("Pancit Canton", 16, "fast"),
    ("3-in-1 Coffee Sachet", 12, "fast"),
    ("Candies (per piece)", 2, "fast"),
    ("Shampoo Sachet", 8, "fast"),
    ("Cigarette (per stick)", 10, "fast"),
    ("Egg (per piece)", 9, "fast"),
    ("Biscuits Pack", 10, "fast"),
    ("Small Chips Pack", 12, "fast"),
    ("Detergent Sachet", 10, "fast"),
    ("Ice Candy", 5, "fast"),
    ("Toothpaste Sachet", 8, "fast"),
    # Mid-priced items that sell steadily
    ("Sardines Can", 26, "steady"),
    ("Rice (per kilo)", 52, "steady"),
    ("Load Card", 50, "steady"),
    ("Coke 1.5L", 78, "steady"),
    ("Loaf Bread", 68, "steady"),
    ("Cooking Oil (small bottle)", 45, "steady"),
    ("Corned Beef Can", 42, "steady"),
    ("Soy Sauce Bottle", 28, "steady"),
    ("Vinegar Bottle", 25, "steady"),
    ("Evaporated Milk Can", 38, "steady"),
    # Expensive items that sell slowly
    ("Cooking Oil 1L", 125, "slow"),
    ("Cigarettes (full pack)", 170, "slow"),
    ("Powdered Milk (large)", 220, "slow"),
    ("Rice Sack 5kg", 270, "slow"),
    ("Instant Coffee Jar", 190, "slow"),
    ("Fabric Conditioner Bottle", 150, "slow"),
    ("Shampoo Bottle", 185, "slow"),
    ("Hair Conditioner Bottle", 175, "slow"),
    ("Batteries Pack", 120, "slow"),
]

# Typical (average units per week, spread, average margin %, spread) per group.
GROUP_SETTINGS = {
    "fast": (150, 25, 12, 2.5),
    "steady": (60, 10, 18, 2.5),
    "slow": (12, 4, 28, 3.5),
}


def generate_products(seed=42):
    """Create a table of store products with price, units sold and margin."""
    rng = np.random.default_rng(seed)
    rows = []

    for name, typical_price, group in PRODUCT_LIST:
        units_mean, units_spread, margin_mean, margin_spread = GROUP_SETTINGS[group]

        # Add a small random change so the groups are not perfectly neat.
        price = typical_price * rng.normal(1.0, 0.05)
        units = rng.normal(units_mean, units_spread)
        margin = rng.normal(margin_mean, margin_spread)

        rows.append({
            "product": name,
            "price": round(price, 2),
            "weekly_units_sold": max(1, int(round(units))),  # never below 1
            "profit_margin": round(margin, 1),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Quick self-test: python data.py
    sales = generate_sales()
    products = generate_products()
    print(sales.head())
    print("Sales rows:", len(sales), "| average sales:", round(sales["daily_sales"].mean(), 2))
    print(products.head())
    print("Products:", len(products))

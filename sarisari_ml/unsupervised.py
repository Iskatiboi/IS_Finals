"""
unsupervised.py - UNSUPERVISED LEARNING: group similar products.

"Unsupervised" means there is no right answer in the data.
KMeans looks only at the numbers and finds groups by itself.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# The three numbers KMeans uses to compare products.
FEATURES = ["price", "weekly_units_sold", "profit_margin"]


def scale_features(products):
    """Put all features on the same scale, so price does not dominate."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(products[FEATURES])
    return scaler, scaled


def compute_elbow(products):
    """Compute the inertia for k = 1 to 8, to help us justify k = 3."""
    _, scaled = scale_features(products)
    rows = []

    for k in range(1, 9):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(scaled)
        # Inertia = how far products are from their group center (lower = tighter).
        rows.append({"k": k, "inertia": model.inertia_})

    return pd.DataFrame(rows)


def cluster_products(products):
    """Group products into 3 clusters and give each cluster a readable name."""
    scaler, scaled = scale_features(products)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_numbers = model.fit_predict(scaled)

    # Convert the cluster centers back to real units (pesos, units, percent).
    centers = pd.DataFrame(scaler.inverse_transform(model.cluster_centers_), columns=FEATURES)

    # Sort the clusters from lowest to highest average units sold, then name them.
    order = centers["weekly_units_sold"].sort_values().index
    names = {order[0]: "Slow Movers", order[1]: "Steady Sellers", order[2]: "Fast Movers"}

    # Copy the table so the original data is not changed.
    result = products.copy()
    result["cluster_name"] = [names[number] for number in cluster_numbers]

    # Average values and the number of products in each cluster.
    summary = result.groupby("cluster_name")[FEATURES].mean().round(2)
    summary["number_of_products"] = result["cluster_name"].value_counts()
    summary = summary.loc[["Fast Movers", "Steady Sellers", "Slow Movers"]].reset_index()

    return result, summary


if __name__ == "__main__":
    # Quick self-test: python unsupervised.py
    from data import generate_products

    items = generate_products()
    print(compute_elbow(items).round(2))
    labeled, table = cluster_products(items)
    print(table)
    print(labeled[["product", "cluster_name"]].to_string())

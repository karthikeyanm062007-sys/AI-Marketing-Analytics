from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def segment_customers(df, n_clusters=3):
    """
    Segment customers using K-Means clustering.
    """

    features = [
        "income",
        "website_visits",
        "email_opens",
        "email_clicks",
        "purchases",
        "total_spent"
    ]

    # Select features
    X = df[features].copy()

    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create K-Means model
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    # Train the model
    df = df.copy()
    df["cluster"] = model.fit_predict(X_scaled)

    return df, model, scaler


def summarize_segments(df):
    """
    Create a summary of each customer segment.
    """

    summary = (
        df.groupby("cluster")
        .agg(
            customers=("customer_id", "count"),
            average_income=("income", "mean"),
            average_purchases=("purchases", "mean"),
            average_spending=("total_spent", "mean"),
            average_website_visits=("website_visits", "mean")
        )
        .reset_index()
    )

    return summary


def label_segments(summary):
    """
    Give meaningful names to customer segments
    based on average spending.
    """

    sorted_clusters = (
        summary.sort_values("average_spending")["cluster"].tolist()
    )

    labels = {}

    if len(sorted_clusters) == 3:
        labels[sorted_clusters[0]] = "Low Value"
        labels[sorted_clusters[1]] = "Medium Value"
        labels[sorted_clusters[2]] = "High Value"

    elif len(sorted_clusters) == 2:
        labels[sorted_clusters[0]] = "Low Value"
        labels[sorted_clusters[1]] = "High Value"

    else:
        for cluster in sorted_clusters:
            labels[cluster] = f"Segment {cluster}"

    summary["segment_name"] = summary["cluster"].map(labels)

    return summary
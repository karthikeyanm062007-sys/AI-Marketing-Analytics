from src.data_processing import load_data, clean_data
from src.ml_models import (
    segment_customers,
    summarize_segments,
    label_segments
)   


df = load_data("data/marketing_data.csv")

df = clean_data(df)

segmented_df, model, scaler = segment_customers(df)

print("========== CUSTOMER SEGMENTS ==========")

print(
    segmented_df[
        [
            "customer_id",
            "income",
            "purchases",
            "total_spent",
            "cluster"
        ]
    ]
)

print("\n========== SEGMENT SUMMARY ==========")

summary = summarize_segments(segmented_df)

summary = label_segments(summary)

print(summary)  
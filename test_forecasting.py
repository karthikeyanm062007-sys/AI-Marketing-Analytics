from src.data_processing import load_data, clean_data

from src.forecasting import (
    generate_forecast,
    generate_overall_forecast,
    generate_forecast_insight
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data(
    "data/marketing_data.csv"
)

df = clean_data(df)


# ============================================================
# CAMPAIGN FORECAST
# ============================================================

forecast = generate_forecast(
    df,
    growth_rate=0.10
)

print()
print("========== AI MARKETING FORECAST ==========")
print()

print(
    forecast[
        [
            "campaign",
            "revenue",
            "forecast_revenue",
            "conversions",
            "forecast_conversions",
            "current_roas",
            "forecast_roas"
        ]
    ]
)


# ============================================================
# OVERALL FORECAST
# ============================================================

overall = generate_overall_forecast(
    df,
    growth_rate=0.10
)

print()
print("========== OVERALL FORECAST ==========")
print()

print(
    f"Current Revenue: "
    f"${overall['current_revenue']:,.0f}"
)

print(
    f"Forecast Revenue: "
    f"${overall['forecast_revenue']:,.0f}"
)

print(
    f"Current Conversions: "
    f"{overall['current_conversions']:,}"
)

print(
    f"Forecast Conversions: "
    f"{overall['forecast_conversions']:,}"
)

print(
    f"Current ROAS: "
    f"{overall['current_roas']:.2f}"
)

print(
    f"Forecast ROAS: "
    f"{overall['forecast_roas']:.2f}"
)


# ============================================================
# AI FORECAST INSIGHT
# ============================================================

print()
print("========== AI FORECAST INSIGHT ==========")
print()

print(
    generate_forecast_insight(
        overall,
        growth_rate=0.10
    )
)
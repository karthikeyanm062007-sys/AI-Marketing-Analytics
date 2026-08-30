# ============================================================
# AI MARKETING FORECASTING MODULE
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# PREPARE FORECAST DATA
# ============================================================

def prepare_forecast_data(df):
    """
    Prepare campaign-level marketing data.

    Revenue is calculated from total_spent because the
    project CSV does not contain a separate revenue column.
    """

    required_columns = [
        "campaign",
        "ad_spend",
        "conversions"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Calculate campaign revenue
    # --------------------------------------------------------

    if "total_spent" in df.columns:

        campaign_data = (
            df.groupby("campaign")
            .agg(
                revenue=("total_spent", "sum"),
                ad_spend=("ad_spend", "sum"),
                conversions=("conversions", "sum")
            )
            .reset_index()
        )

    else:

        raise ValueError(
            "The dataset must contain "
            "'total_spent' to calculate revenue."
        )

    return campaign_data


# ============================================================
# FORECAST REVENUE
# ============================================================

def forecast_revenue(df, growth_rate=0.10):

    forecast_data = prepare_forecast_data(df)

    forecast_data["forecast_revenue"] = (
        forecast_data["revenue"]
        * (1 + growth_rate)
    )

    forecast_data["forecast_revenue"] = (
        forecast_data["forecast_revenue"]
        .round(2)
    )

    return forecast_data


# ============================================================
# FORECAST CONVERSIONS
# ============================================================

def forecast_conversions(df, growth_rate=0.10):

    forecast_data = prepare_forecast_data(df)

    forecast_data["forecast_conversions"] = (
        forecast_data["conversions"]
        * (1 + growth_rate)
    )

    forecast_data["forecast_conversions"] = (
        forecast_data["forecast_conversions"]
        .round()
        .astype(int)
    )

    return forecast_data


# ============================================================
# FORECAST ROAS
# ============================================================

def forecast_roas(df, growth_rate=0.10):

    forecast_data = prepare_forecast_data(df)

    forecast_data["forecast_revenue"] = (
        forecast_data["revenue"]
        * (1 + growth_rate)
    )

    forecast_data["forecast_roas"] = np.where(
        forecast_data["ad_spend"] > 0,
        forecast_data["forecast_revenue"]
        / forecast_data["ad_spend"],
        0
    )

    forecast_data["forecast_roas"] = (
        forecast_data["forecast_roas"]
        .round(2)
    )

    return forecast_data


# ============================================================
# COMPLETE CAMPAIGN FORECAST
# ============================================================

def generate_forecast(df, growth_rate=0.10):

    forecast_data = prepare_forecast_data(df)

    # --------------------------------------------------------
    # Forecast revenue
    # --------------------------------------------------------

    forecast_data["forecast_revenue"] = (
        forecast_data["revenue"]
        * (1 + growth_rate)
    )

    # --------------------------------------------------------
    # Forecast conversions
    # --------------------------------------------------------

    forecast_data["forecast_conversions"] = (
        forecast_data["conversions"]
        * (1 + growth_rate)
    )

    # --------------------------------------------------------
    # Current ROAS
    # --------------------------------------------------------

    forecast_data["current_roas"] = np.where(
        forecast_data["ad_spend"] > 0,
        forecast_data["revenue"]
        / forecast_data["ad_spend"],
        0
    )

    # --------------------------------------------------------
    # Forecast ROAS
    # --------------------------------------------------------

    forecast_data["forecast_roas"] = np.where(
        forecast_data["ad_spend"] > 0,
        forecast_data["forecast_revenue"]
        / forecast_data["ad_spend"],
        0
    )

    # --------------------------------------------------------
    # Round values
    # --------------------------------------------------------

    forecast_data["forecast_revenue"] = (
        forecast_data["forecast_revenue"]
        .round(2)
    )

    forecast_data["forecast_conversions"] = (
        forecast_data["forecast_conversions"]
        .round()
        .astype(int)
    )

    forecast_data["current_roas"] = (
        forecast_data["current_roas"]
        .round(2)
    )

    forecast_data["forecast_roas"] = (
        forecast_data["forecast_roas"]
        .round(2)
    )

    return forecast_data


# ============================================================
# OVERALL FORECAST
# ============================================================

def generate_overall_forecast(
    df,
    growth_rate=0.10
):

    forecast_data = generate_forecast(
        df,
        growth_rate
    )

    current_revenue = (
        forecast_data["revenue"].sum()
    )

    forecast_revenue = (
        forecast_data["forecast_revenue"].sum()
    )

    current_conversions = (
        forecast_data["conversions"].sum()
    )

    forecast_conversions = (
        forecast_data["forecast_conversions"].sum()
    )

    total_ad_spend = (
        forecast_data["ad_spend"].sum()
    )

    # --------------------------------------------------------
    # Current ROAS
    # --------------------------------------------------------

    if total_ad_spend > 0:

        current_roas = (
            current_revenue
            / total_ad_spend
        )

    else:

        current_roas = 0


    # --------------------------------------------------------
    # Forecast ROAS
    # --------------------------------------------------------

    if total_ad_spend > 0:

        forecast_roas = (
            forecast_revenue
            / total_ad_spend
        )

    else:

        forecast_roas = 0


    return {

        "current_revenue": round(
            current_revenue,
            2
        ),

        "forecast_revenue": round(
            forecast_revenue,
            2
        ),

        "current_conversions": int(
            current_conversions
        ),

        "forecast_conversions": int(
            forecast_conversions
        ),

        "current_roas": round(
            current_roas,
            2
        ),

        "forecast_roas": round(
            forecast_roas,
            2
        )
    }


# ============================================================
# AI FORECAST INSIGHT
# ============================================================

def generate_forecast_insight(
    forecast,
    growth_rate=0.10
):

    current_revenue = forecast[
        "current_revenue"
    ]

    forecast_revenue = forecast[
        "forecast_revenue"
    ]

    current_roas = forecast[
        "current_roas"
    ]

    forecast_roas = forecast[
        "forecast_roas"
    ]

    revenue_change = (
        forecast_revenue
        - current_revenue
    )

    # --------------------------------------------------------
    # Improving forecast
    # --------------------------------------------------------

    if forecast_roas > current_roas:

        return (
            f"📈 Revenue is projected to increase by "
            f"{growth_rate * 100:.0f}% from "
            f"${current_revenue:,.0f} to "
            f"${forecast_revenue:,.0f}. "
            f"Forecast ROAS is expected to improve "
            f"from {current_roas:.2f} to "
            f"{forecast_roas:.2f}."
        )

    # --------------------------------------------------------
    # Declining forecast
    # --------------------------------------------------------

    elif forecast_roas < current_roas:

        return (
            f"⚠️ Revenue is projected to change by "
            f"${revenue_change:,.0f}. "
            f"Monitor campaign efficiency because "
            f"forecast ROAS is {forecast_roas:.2f}."
        )

    # --------------------------------------------------------
    # Stable forecast
    # --------------------------------------------------------

    return (
        f"📊 Marketing performance is projected "
        f"to remain relatively stable with "
        f"forecast ROAS of {forecast_roas:.2f}."
    )
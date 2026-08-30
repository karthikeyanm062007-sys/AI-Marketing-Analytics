import streamlit as st
import pandas as pd

from src.data_processing import load_data, clean_data
from src.analytics import calculate_kpis, campaign_performance
from src.ml_models import (
    segment_customers,
    summarize_segments,
    label_segments,
)
from src.recommendations import (
    generate_campaign_recommendations,
    generate_customer_recommendations,
)
from src.ai_scoring import generate_ai_scoring
from src.forecasting import (
    generate_forecast,
    generate_overall_forecast,
    generate_forecast_insight,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Marketing Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .metric-card {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 10px;
        }

        .recommendation-card {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 12px;
        }

        .score-card {
            padding: 20px;
            border-radius: 14px;
            border: 1px solid rgba(128,128,128,0.25);
            text-align: center;
        }

        .small-text {
            color: #777;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Marketing Analytics")

st.subheader(
    "Marketing Intelligence & Customer Segmentation Dashboard"
)

st.caption(
    "AI-powered marketing analytics, customer segmentation, "
    "campaign scoring, recommendations and forecasting."
)


# ============================================================
# LOAD DATA
# ============================================================

try:
    raw_data = load_data("data/marketing_data.csv")
    df = clean_data(raw_data)

except Exception as e:
    st.error("Unable to load marketing data.")
    st.exception(e)
    st.stop()


# ============================================================
# DASHBOARD CONTROLS
# ============================================================

st.sidebar.header("🎛️ Dashboard Controls")

campaigns_list = ["All Campaigns"] + sorted(
    df["campaign"].dropna().unique().tolist()
)

selected_campaign = st.sidebar.selectbox(
    "Campaign Filter",
    campaigns_list,
)

st.sidebar.caption(
    "Use the campaign filter to analyze individual marketing campaigns."
)


# ============================================================
# FILTER DATA
# ============================================================

if selected_campaign == "All Campaigns":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["campaign"] == selected_campaign
    ].copy()


# ============================================================
# MARKETING KPI CALCULATIONS
# ============================================================

kpis = calculate_kpis(filtered_df)


# ============================================================
# MARKETING KPIs
# ============================================================

st.header("📊 Marketing KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"${kpis['total_revenue']:,.0f}",
    )

with col2:
    st.metric(
        "📢 Ad Spend",
        f"${kpis['total_ad_spend']:,.0f}",
    )

with col3:
    st.metric(
        "🎯 Conversions",
        f"{kpis['total_conversions']:,.0f}",
    )

with col4:
    st.metric(
        "📈 ROAS",
        f"{kpis['roas']:.2f}",
    )


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👁️ Impressions",
        f"{kpis['total_impressions']:,.0f}",
    )

with col2:
    st.metric(
        "🖱️ Clicks",
        f"{kpis['total_clicks']:,.0f}",
    )

with col3:
    st.metric(
        "📊 CTR",
        f"{kpis['ctr']:.2f}%",
    )

with col4:
    st.metric(
        "💵 CPC",
        f"${kpis['cpc']:.2f}",
    )


# ============================================================
# CAMPAIGN PERFORMANCE
# ============================================================

st.header("📈 Campaign Performance")

campaigns = campaign_performance(filtered_df)

if campaigns is None or campaigns.empty:
    st.warning("No campaign performance data available.")
else:

    st.dataframe(
        campaigns,
        use_container_width=True,
        hide_index=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 ROAS by Campaign")

        roas_chart = campaigns.set_index("campaign")[
            ["ROAS"]
        ]

        st.bar_chart(roas_chart)

    with col2:
        st.subheader("🎯 Conversions by Campaign")

        conversion_chart = campaigns.set_index("campaign")[
            ["conversions"]
        ]

        st.bar_chart(conversion_chart)


# ============================================================
# AI CAMPAIGN PERFORMANCE SCORING
# ============================================================

st.header("🧠 AI Campaign Performance Score")

try:

    scored_campaigns = generate_ai_scoring(campaigns)

    if scored_campaigns is not None and not scored_campaigns.empty:

        st.subheader("🎯 Campaign AI Scores")

        score_columns = [
            "campaign",
            "AI Score",
            "Performance Level",
        ]

        available_score_columns = [
            col
            for col in score_columns
            if col in scored_campaigns.columns
        ]

        if available_score_columns:

            score_display = scored_campaigns[
                available_score_columns
            ].copy()

            st.dataframe(
                score_display,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.dataframe(
                scored_campaigns,
                use_container_width=True,
                hide_index=True,
            )

        if "AI Score" in scored_campaigns.columns:

            st.subheader("📊 AI Score Comparison")

            score_chart = scored_campaigns.set_index(
                "campaign"
            )[["AI Score"]]

            st.bar_chart(score_chart)

except Exception as e:

    st.warning("AI performance scoring could not be displayed.")

    with st.expander("Technical details"):
        st.exception(e)


# ============================================================
# AI MARKETING INSIGHTS
# ============================================================

st.header("🤖 AI Marketing Insights")

if campaigns is not None and not campaigns.empty:

    best_campaign = campaigns.loc[
        campaigns["ROAS"].idxmax()
    ]

    attention_campaign = campaigns.loc[
        campaigns["ROAS"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🟢 Best Performing Campaign")

        st.success(
            f"""
            **{best_campaign['campaign']}**

            ROAS: **{best_campaign['ROAS']:.2f}**

            Conversions: **{best_campaign['conversions']:,.0f}**

            Revenue: **${best_campaign['revenue']:,.0f}**

            Ad Spend: **${best_campaign['ad_spend']:,.0f}**
            """
        )

    with col2:

        st.subheader("🔴 Campaign Requiring Attention")

        st.error(
            f"""
            **{attention_campaign['campaign']}**

            ROAS: **{attention_campaign['ROAS']:.2f}**

            Ad Spend: **${attention_campaign['ad_spend']:,.0f}**

            Revenue: **${attention_campaign['revenue']:,.0f}**
            """
        )


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

st.header("🤖 AI Customer Segmentation")

try:

    segmented_df, segmentation_model, scaler = segment_customers(
        df.copy(),
        n_clusters=3,
    )

    segment_summary = summarize_segments(
        segmented_df
    )

    # label_segments modifies the summary
    # in the existing project implementation.
    labeled_summary = label_segments(
        segment_summary
    )

    if labeled_summary is not None:
        segment_summary = labeled_summary

    # Safety fallback in case the function modifies the
    # dataframe but does not explicitly return it.
    if "segment_name" not in segment_summary.columns:

        sorted_clusters = (
            segment_summary
            .sort_values("average_spending")["cluster"]
            .tolist()
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

        segment_summary["segment_name"] = (
            segment_summary["cluster"].map(labels)
        )

    # Add segment name to customer dataframe
    segmented_df["segment_name"] = segmented_df[
        "cluster"
    ].map(
        segment_summary.set_index("cluster")[
            "segment_name"
        ]
    )

    # --------------------------------------------------------
    # Segment chart
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👥 Customers by Segment")

        segment_counts = (
            segmented_df["segment_name"]
            .value_counts()
            .rename("customers")
        )

        st.bar_chart(segment_counts)

    with col2:

        st.subheader("👤 Customer Details")

        customer_columns = [
            "customer_id",
            "income",
            "purchases",
            "total_spent",
            "segment_name",
        ]

        available_customer_columns = [
            col
            for col in customer_columns
            if col in segmented_df.columns
        ]

        st.dataframe(
            segmented_df[
                available_customer_columns
            ],
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # Segment summary
    # --------------------------------------------------------

    st.subheader("📋 Segment Summary")

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # Customer insights
    # --------------------------------------------------------

    st.subheader("💡 Customer Insights")

    for _, row in segment_summary.iterrows():

        segment_name = row["segment_name"]
        customer_count = int(row["customers"])
        average_spending = float(
            row["average_spending"]
        )

        if segment_name == "High Value":

            st.success(
                f"💎 **High Value Customers:** "
                f"{customer_count} customers with average "
                f"spending of ${average_spending:,.2f}."
            )

        elif segment_name == "Medium Value":

            st.info(
                f"🚀 **Medium Value Customers:** "
                f"{customer_count} customers represent "
                f"an opportunity for upselling."
            )

        elif segment_name == "Low Value":

            st.warning(
                f"💤 **Low Value Customers:** "
                f"{customer_count} customers may need "
                f"targeted engagement campaigns."
            )

except Exception as e:

    st.error("Customer segmentation could not be displayed.")

    with st.expander("Technical details"):
        st.exception(e)

    segmented_df = None
    segment_summary = None


# ============================================================
# AI MARKETING RECOMMENDATIONS
# ============================================================

st.header("🧠 AI Marketing Recommendations")

# ------------------------------------------------------------
# Campaign Recommendations
# ------------------------------------------------------------

st.subheader("📢 AI Campaign Recommendations")

try:

    campaign_recommendations = (
        generate_campaign_recommendations(campaigns)
    )

    if campaign_recommendations:

        for recommendation in campaign_recommendations:

            campaign_name = recommendation.get(
                "campaign",
                "Campaign",
            )

            status = recommendation.get(
                "status",
                "Recommendation",
            )

            message = recommendation.get(
                "recommendation",
                "",
            )

            with st.container(border=True):

                st.markdown(
                    f"### {status} — {campaign_name}"
                )

                st.write(message)

    else:

        st.info(
            "No campaign recommendations available."
        )

except Exception as e:

    st.warning(
        "Campaign recommendations could not be generated."
    )

    with st.expander("Technical details"):
        st.exception(e)


# ------------------------------------------------------------
# Customer Recommendations
# ------------------------------------------------------------

st.subheader("👥 AI Customer Recommendations")

try:

    if segment_summary is not None:

        customer_recommendations = (
            generate_customer_recommendations(
                segment_summary
            )
        )

        if customer_recommendations:

            for recommendation in customer_recommendations:

                segment_name = recommendation.get(
                    "segment",
                    "Customer Segment",
                )

                message = recommendation.get(
                    "recommendation",
                    "",
                )

                with st.container(border=True):

                    st.markdown(
                        f"### 🎯 {segment_name}"
                    )

                    st.write(message)

        else:

            st.info(
                "No customer recommendations available."
            )

except Exception as e:

    st.warning(
        "Customer recommendations could not be generated."
    )

    with st.expander("Technical details"):
        st.exception(e)


# ============================================================
# AI MARKETING FORECAST
# ============================================================

st.header("🔮 AI Marketing Forecast")

st.caption(
    "AI-powered projection of future marketing performance."
)

try:

    # Generate campaign-level forecast
    forecast = generate_forecast(df)

    if forecast is not None and not forecast.empty:

        # Generate overall forecast
        overall_forecast = generate_overall_forecast(
            forecast
        )

        # ----------------------------------------------------
        # Extract overall values safely
        # ----------------------------------------------------

        current_revenue = float(
            overall_forecast.get(
                "current_revenue",
                kpis["total_revenue"],
            )
        )

        forecast_revenue = float(
            overall_forecast.get(
                "forecast_revenue",
                current_revenue,
            )
        )

        current_conversions = float(
            overall_forecast.get(
                "current_conversions",
                kpis["total_conversions"],
            )
        )

        forecast_conversions = float(
            overall_forecast.get(
                "forecast_conversions",
                current_conversions,
            )
        )

        current_roas = float(
            overall_forecast.get(
                "current_roas",
                kpis["roas"],
            )
        )

        forecast_roas = float(
            overall_forecast.get(
                "forecast_roas",
                current_roas,
            )
        )

        # ----------------------------------------------------
        # Forecast KPI cards
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Forecast Revenue",
                f"${forecast_revenue:,.0f}",
            )

        with col2:

            st.metric(
                "🎯 Forecast Conversions",
                f"{forecast_conversions:,.0f}",
            )

        with col3:

            st.metric(
                "📈 Forecast ROAS",
                f"{forecast_roas:.2f}",
            )

        # ----------------------------------------------------
        # Current vs Forecast
        # ----------------------------------------------------

        st.subheader("📊 Current vs Forecast")

        comparison_df = pd.DataFrame(
            {
                "Metric": [
                    "Revenue",
                    "Conversions",
                    "ROAS",
                ],
                "Current": [
                    current_revenue,
                    current_conversions,
                    current_roas,
                ],
                "Forecast": [
                    forecast_revenue,
                    forecast_conversions,
                    forecast_roas,
                ],
            }
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # Campaign forecast
        # ----------------------------------------------------

        st.subheader("🎯 Campaign Forecast")

        st.dataframe(
            forecast,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # Revenue forecast chart
        # ----------------------------------------------------

        if (
            "campaign" in forecast.columns
            and "revenue" in forecast.columns
            and "forecast_revenue" in forecast.columns
        ):

            st.subheader(
                "📈 Current Revenue vs Forecast Revenue"
            )

            revenue_chart = forecast.set_index(
                "campaign"
            )[
                [
                    "revenue",
                    "forecast_revenue",
                ]
            ].rename(
                columns={
                    "revenue": "Current Revenue",
                    "forecast_revenue": "Forecast Revenue",
                }
            )

            st.bar_chart(revenue_chart)

        # ----------------------------------------------------
        # Forecast insight
        # ----------------------------------------------------

        st.subheader("🧠 AI Forecast Insight")

        try:

            insight = generate_forecast_insight(
                overall_forecast
            )

            if insight:
                st.info(insight)

            else:
                revenue_growth = 0

                if current_revenue > 0:
                    revenue_growth = (
                        forecast_revenue
                        - current_revenue
                    ) / current_revenue * 100

                st.info(
                    f"📈 Revenue is projected to increase "
                    f"by {revenue_growth:.0f}% from "
                    f"${current_revenue:,.0f} to "
                    f"${forecast_revenue:,.0f}. "
                    f"Forecast ROAS is expected to improve "
                    f"from {current_roas:.2f} to "
                    f"{forecast_roas:.2f}."
                )

        except Exception:

            revenue_growth = 0

            if current_revenue > 0:
                revenue_growth = (
                    forecast_revenue
                    - current_revenue
                ) / current_revenue * 100

            st.info(
                f"📈 Revenue is projected to increase "
                f"by {revenue_growth:.0f}% from "
                f"${current_revenue:,.0f} to "
                f"${forecast_revenue:,.0f}. "
                f"Forecast ROAS is expected to improve "
                f"from {current_roas:.2f} to "
                f"{forecast_roas:.2f}."
            )

    else:

        st.warning(
            "Forecast data is not available."
        )

except Exception as e:

    st.error(
        "AI forecasting could not be displayed."
    )

    with st.expander("Technical details"):
        st.exception(e)


# ============================================================
# AI EXECUTIVE SUMMARY
# ============================================================

st.header("🧠 AI Executive Summary")

try:

    if campaigns is not None and not campaigns.empty:

        best = campaigns.loc[
            campaigns["ROAS"].idxmax()
        ]

        worst = campaigns.loc[
            campaigns["ROAS"].idxmin()
        ]

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            st.success(
                f"""
                **Best Campaign: {best['campaign']}**

                ROAS: **{best['ROAS']:.2f}**

                Conversions: **{best['conversions']:,.0f}**

                Revenue: **${best['revenue']:,.0f}**
                """
            )

        with summary_col2:

            st.warning(
                f"""
                **Campaign Requiring Attention: {worst['campaign']}**

                ROAS: **{worst['ROAS']:.2f}**

                Revenue: **${worst['revenue']:,.0f}**

                Ad Spend: **${worst['ad_spend']:,.0f}**
                """
            )

        # ----------------------------------------------------
        # Automatic recommendation
        # ----------------------------------------------------

        if best["ROAS"] > 1:

            st.info(
                f"💡 **Recommended Action:** "
                f"Consider gradually increasing investment in "
                f"{best['campaign']} while monitoring ROAS."
            )

        else:

            st.info(
                "💡 **Recommended Action:** "
                "Review campaign targeting, creatives, "
                "conversion performance and advertising spend "
                "before increasing budgets."
            )

except Exception:

    st.info(
        "AI executive summary is currently unavailable."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Marketing Analytics | "
    "Python • Pandas • Scikit-learn • Streamlit"
)

def calculate_kpis(df):
    """
    Calculate important marketing KPIs.
    """

    total_impressions = df["impressions"].sum()
    total_clicks = df["clicks"].sum()
    total_conversions = df["conversions"].sum()

    total_ad_spend = df["ad_spend"].sum()
    total_revenue = df["total_spent"].sum()

    # Click Through Rate
    if total_impressions > 0:
        ctr = total_clicks / total_impressions * 100
    else:
        ctr = 0

    # Conversion Rate
    if total_clicks > 0:
        conversion_rate = total_conversions / total_clicks * 100
    else:
        conversion_rate = 0

    # Cost Per Click
    if total_clicks > 0:
        cpc = total_ad_spend / total_clicks
    else:
        cpc = 0

    # Return On Ad Spend
    if total_ad_spend > 0:
        roas = total_revenue / total_ad_spend
    else:
        roas = 0

    return {
        "total_revenue": total_revenue,
        "total_ad_spend": total_ad_spend,
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "ctr": ctr,
        "conversion_rate": conversion_rate,
        "cpc": cpc,
        "roas": roas
    }


def campaign_performance(df):
    """
    Calculate performance for each marketing campaign.
    """

    result = (
        df.groupby("campaign")
        .agg(
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            conversions=("conversions", "sum"),
            ad_spend=("ad_spend", "sum"),
            revenue=("total_spent", "sum")
        )
        .reset_index()
    )

    # Campaign CTR
    result["CTR"] = (
        result["clicks"]
        / result["impressions"]
        * 100
    )

    # Campaign Conversion Rate
    result["Conversion Rate"] = (
        result["conversions"]
        / result["clicks"]
        * 100
    )

    # Campaign ROAS
    result["ROAS"] = (
        result["revenue"]
        / result["ad_spend"]
    )

    return result
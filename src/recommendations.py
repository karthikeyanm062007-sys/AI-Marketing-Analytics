def generate_campaign_recommendations(campaigns):
    """
    Generate marketing recommendations based on
    campaign performance.
    """

    recommendations = []

    for _, campaign in campaigns.iterrows():

        name = campaign["campaign"]
        roas = campaign["ROAS"]
        ctr = campaign["CTR"]
        conversion_rate = campaign["Conversion Rate"]

        # Strong campaign
        if roas >= 1.0:

            recommendations.append({
                "campaign": name,
                "status": "🟢 Strong",
                "recommendation": (
                    f"{name} is performing well with a "
                    f"ROAS of {roas:.2f}. "
                    "Consider increasing the budget gradually "
                    "while monitoring performance."
                )
            })

        # Moderate campaign
        elif roas >= 0.5:

            recommendations.append({
                "campaign": name,
                "status": "🟡 Moderate",
                "recommendation": (
                    f"{name} has a moderate ROAS of "
                    f"{roas:.2f}. "
                    "Test new creatives and audience targeting "
                    "before increasing the budget."
                )
            })

        # Weak campaign
        else:

            recommendations.append({
                "campaign": name,
                "status": "🔴 Needs Attention",
                "recommendation": (
                    f"{name} has a low ROAS of "
                    f"{roas:.2f}. "
                    "Review targeting, ad creatives, "
                    "and advertising spend."
                )
            })

        # CTR analysis
        if ctr < 4:

            recommendations.append({
                "campaign": name,
                "status": "💡 CTR Alert",
                "recommendation": (
                    f"{name} has a CTR of {ctr:.2f}%. "
                    "Consider improving ad copy, creatives, "
                    "and call-to-action messages."
                )
            })

        # Conversion analysis
        if conversion_rate < 8:

            recommendations.append({
                "campaign": name,
                "status": "🎯 Conversion Alert",
                "recommendation": (
                    f"{name} has a conversion rate of "
                    f"{conversion_rate:.2f}%. "
                    "Review the landing page, offer, "
                    "and conversion funnel."
                )
            })

    return recommendations


def generate_customer_recommendations(summary):
    """
    Generate recommendations based on customer segments.
    """

    recommendations = []

    for _, segment in summary.iterrows():

        segment_name = segment["segment_name"]
        customers = int(segment["customers"])
        spending = segment["average_spending"]

        # High Value customers
        if segment_name == "High Value":

            recommendations.append({
                "segment": segment_name,
                "recommendation": (
                    f"Target the {customers} High Value customers "
                    "with loyalty programs, personalized offers, "
                    "and retention campaigns. "
                    f"Their average spending is ${spending:,.2f}."
                )
            })

        # Medium Value customers
        elif segment_name == "Medium Value":

            recommendations.append({
                "segment": segment_name,
                "recommendation": (
                    f"Target the {customers} Medium Value customers "
                    "with upselling, cross-selling, and "
                    "personalized product recommendations."
                )
            })

        # Low Value customers
        elif segment_name == "Low Value":

            recommendations.append({
                "segment": segment_name,
                "recommendation": (
                    f"Target the {customers} Low Value customers "
                    "with engagement campaigns, introductory "
                    "offers, and reactivation campaigns."
                )
            })

    return recommendations
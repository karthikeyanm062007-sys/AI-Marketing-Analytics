# ============================================================
# AI MARKETING PERFORMANCE SCORING
# ============================================================


def calculate_ai_score(campaign):
    """
    Calculate an AI-style marketing performance score
    between 0 and 100.

    Scoring weights:

    ROAS              = 40%
    CTR               = 20%
    Conversion Rate   = 20%
    CPC Efficiency    = 20%
    """

    # --------------------------------------------------------
    # GET CAMPAIGN METRICS
    # --------------------------------------------------------

    roas = float(campaign["ROAS"])

    ctr = float(campaign["CTR"])

    conversion_rate = float(
        campaign["Conversion Rate"]
    )

    ad_spend = float(
        campaign["ad_spend"]
    )

    clicks = float(
        campaign["clicks"]
    )


    # --------------------------------------------------------
    # CALCULATE CPC
    # --------------------------------------------------------

    if clicks > 0:

        cpc = ad_spend / clicks

    else:

        cpc = 0


    # --------------------------------------------------------
    # ROAS SCORE
    #
    # Target ROAS = 2.0
    # --------------------------------------------------------

    roas_score = min(
        (roas / 2.0) * 100,
        100
    )


    # --------------------------------------------------------
    # CTR SCORE
    #
    # Target CTR = 10%
    # --------------------------------------------------------

    ctr_score = min(
        (ctr / 10.0) * 100,
        100
    )


    # --------------------------------------------------------
    # CONVERSION RATE SCORE
    #
    # Target Conversion Rate = 10%
    # --------------------------------------------------------

    conversion_score = min(
        (conversion_rate / 10.0) * 100,
        100
    )


    # --------------------------------------------------------
    # CPC SCORE
    #
    # Lower CPC is better.
    # Target CPC = $1.00
    # --------------------------------------------------------

    if cpc <= 1:

        cpc_score = 100

    else:

        cpc_score = max(
            0,
            (1 / cpc) * 100
        )


    # --------------------------------------------------------
    # FINAL AI SCORE
    # --------------------------------------------------------

    final_score = (
        roas_score * 0.40
        + ctr_score * 0.20
        + conversion_score * 0.20
        + cpc_score * 0.20
    )


    return round(
        min(final_score, 100),
        2
    )


# ============================================================
# PERFORMANCE CLASSIFICATION
# ============================================================

def classify_performance(score):
    """
    Convert numerical AI score into
    a performance category.
    """

    if score >= 80:

        return "🟢 Excellent"

    elif score >= 60:

        return "🟡 Good"

    elif score >= 40:

        return "🟠 Needs Improvement"

    else:

        return "🔴 Critical"


# ============================================================
# GENERATE AI SCORES
# ============================================================

def generate_ai_scoring(campaigns):
    """
    Calculate AI performance scores
    for all campaigns.
    """

    results = campaigns.copy()


    # Calculate AI score

    results["AI Score"] = results.apply(
        calculate_ai_score,
        axis=1
    )


    # Classify performance

    results["Performance"] = (
        results["AI Score"].apply(
            classify_performance
        )
    )


    # Calculate CPC for dashboard display

    results["CPC"] = (
        results["ad_spend"]
        / results["clicks"]
    ).round(2)


    return results


# ============================================================
# AI RECOMMENDATION
# ============================================================

def generate_score_recommendation(campaign):
    """
    Generate a recommendation based
    on the AI performance score.
    """

    score = float(
        campaign["AI Score"]
    )

    name = campaign["campaign"]


    # --------------------------------------------------------
    # EXCELLENT
    # --------------------------------------------------------

    if score >= 80:

        return (
            f"{name} is performing excellently. "
            "Consider gradually increasing the budget "
            "while monitoring ROAS and conversion performance."
        )


    # --------------------------------------------------------
    # GOOD
    # --------------------------------------------------------

    elif score >= 60:

        return (
            f"{name} is performing well but has room "
            "for improvement. Test new creatives, "
            "audiences, and landing pages."
        )


    # --------------------------------------------------------
    # NEEDS IMPROVEMENT
    # --------------------------------------------------------

    elif score >= 40:

        return (
            f"{name} needs improvement. Review targeting, "
            "ad creatives, CTR, and conversion performance "
            "before increasing the budget."
        )


    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    else:

        return (
            f"{name} requires immediate attention. "
            "Consider reducing inefficient spending and "
            "reviewing targeting, creatives, and the "
            "conversion funnel."
                )
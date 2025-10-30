import streamlit as st
import pandas as pd

# -----------------------
# OFFER CATALOG
# -----------------------

OFFER_CATALOG = {
    "IAM": [
        "Identity Diagnostics",
        "Identity Modernization"
    ],
    "Data & AI Security": [
        "Data & AI Security Diagnostics",
        "Data Protection Modernization"
    ],
    "SecOps": [
        "RED Sentinel",
        "RED Defender",
        "Security Copilot Accelerator (including Agentic)",
        "Unified Threat Protection (Sentinel, TI, Defender XDR, Copilot)"
    ],
    "Cloud Security": [
        "Cloud Security Optimization (CSPM)",
        "Cloud Security Modernization (CWPP)"
    ],
    "Cross-Solution Security": [
        "Security Posture Assessment",
        "Zero Trust Maturity Roadmap",
        "Microsoft Security Factory Integration"
    ]
}


# -----------------------
# RULE ENGINE
# -----------------------

def evaluate_rules(client):
    """
    Rule-based engine mapping client propensity and posture to solution areas + offers.
    """

    propensity = client.get("e5_propensity", 0)
    identity_maturity = client.get("identity_maturity", "unknown").lower()
    defender_active = client.get("defender_active", False)
    sentinel_active = client.get("sentinel_active", False)
    industry = client.get("industry", "general").lower()
    recent_incident = client.get("recent_incident", False)
    multicloud = client.get("multicloud", False)
    data_risk = client.get("data_risk", "medium").lower()
    cloud_maturity = client.get("cloud_maturity", "medium").lower()

    recommendations = []

    # === IAM Recommendations ===
    if propensity < 40 or identity_maturity in ["weak", "none", "poor"]:
        recommendations.append({
            "Solution Area": "IAM",
            "Primary Offer": "Identity Diagnostics",
            "Follow-up Offer": "Identity Modernization",
            "Rationale": "Low identity maturity detected. Start with an IAM Diagnostic to uncover risks, followed by modernization to strengthen Entra security posture.",
            "Timeline": "2–4 weeks"
        })

    elif 40 <= propensity < 80 and identity_maturity in ["average", "good"]:
        recommendations.append({
            "Solution Area": "IAM",
            "Primary Offer": "Identity Modernization",
            "Follow-up Offer": "Identity Diagnostics",
            "Rationale": "Moderate E5 readiness and existing identity controls. Focus on Entra modernization and automation for PIM and Conditional Access.",
            "Timeline": "4–6 weeks"
        })

    # === Data & AI Security Recommendations ===
    if data_risk in ["high", "very high"]:
        recommendations.append({
            "Solution Area": "Data & AI Security",
            "Primary Offer": "Data & AI Security Diagnostics",
            "Follow-up Offer": "Data Protection Modernization",
            "Rationale": "High data exposure risk. Diagnostic will assess sensitivity labels, insider risk, and AI data governance to prepare for modernization.",
            "Timeline": "3–5 weeks"
        })

    elif propensity >= 60 and data_risk in ["medium"]:
        recommendations.append({
            "Solution Area": "Data & AI Security",
            "Primary Offer": "Data Protection Modernization",
            "Follow-up Offer": "Data & AI Security Diagnostics",
            "Rationale": "Moderate risk with E5 potential. Introduce data protection modernization to extend Purview, Insider Risk, and AI security controls.",
            "Timeline": "4–6 weeks"
        })

    # === SecOps Recommendations ===
    if propensity >= 80 and (defender_active or sentinel_active):
        recommendations.append({
            "Solution Area": "SecOps",
            "Primary Offer": "RED Sentinel",
            "Follow-up Offer": "Unified Threat Protection (Sentinel, TI, Defender XDR, Copilot)",
            "Rationale": "High E5 readiness with active Defender or Sentinel signals. Deploy RED Sentinel for unified detection and integrate with Unified Threat Protection stack.",
            "Timeline": "4–6 weeks"
        })
    elif 40 <= propensity < 80 and not sentinel_active:
        recommendations.append({
            "Solution Area": "SecOps",
            "Primary Offer": "RED Defender",
            "Follow-up Offer": "Security Copilot Accelerator (including Agentic)",
            "Rationale": "Mid-level E5 readiness with limited SOC visibility. RED Defender strengthens endpoint protection and Copilot enables AI-driven response.",
            "Timeline": "4–5 weeks"
        })

    if recent_incident:
        recommendations.append({
            "Solutio

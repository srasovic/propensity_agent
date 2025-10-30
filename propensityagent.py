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
            "Solution Area": "SecOps",
            "Primary Offer": "Security Copilot Accelerator (including Agentic)",
            "Follow-up Offer": "Unified Threat Protection (Sentinel, TI, Defender XDR, Copilot)",
            "Rationale": "Recent incident suggests detection and response gaps. AI-assisted Security Copilot accelerator enables faster triage and remediation.",
            "Timeline": "3–4 weeks"
        })

    # === Cloud Security Recommendations ===
    if multicloud and cloud_maturity in ["medium", "low"]:
        recommendations.append({
            "Solution Area": "Cloud Security",
            "Primary Offer": "Cloud Security Optimization (CSPM)",
            "Follow-up Offer": "Cloud Security Modernization (CWPP)",
            "Rationale": "Detected multi-cloud setup with incomplete CSPM/CWPP coverage. Optimize visibility and modernize workload protection.",
            "Timeline": "4–6 weeks"
        })

    elif propensity >= 60 and cloud_maturity == "high":
        recommendations.append({
            "Solution Area": "Cloud Security",
            "Primary Offer": "Cloud Security Modernization (CWPP)",
            "Follow-up Offer": "Cloud Security Optimization (CSPM)",
            "Rationale": "High E5 readiness and mature cloud environment. Focus on CWPP to secure workloads and containers at scale.",
            "Timeline": "4–6 weeks"
        })

    # === Cross Solution Recommendations ===
    if propensity >= 70 and len(recommendations) >= 3:
        recommendations.append({
            "Solution Area": "Cross-Solution Security",
            "Primary Offer": "Zero Trust Maturity Roadmap",
            "Follow-up Offer": "Microsoft Security Factory Integration",
            "Rationale": "Multiple security signals detected. Recommend cross-solution Zero Trust roadmap to align IAM, SecOps, Data, and Cloud modernization.",
            "Timeline": "6–8 weeks"
        })

    return recommendations


# -----------------------
# STREAMLIT UI
# -----------------------

st.set_page_config(page_title="Microsoft Security Recommendation Agent", page_icon="🧠", layout="wide")
st.title("🧠 Microsoft Security Recommendation Agent")
st.markdown("Generate intelligent solution recommendations based on E3/E5 propensity and security posture across IAM, SecOps, Data & AI, and Cloud Security.")

with st.form("client_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        client_name = st.text_input("Client Name", "Contoso Ltd")
        e5_propensity = st.slider("E5 Propensity (%)", 0, 100, 75)
        industry = st.selectbox("Industry", ["General", "Finance", "Healthcare", "Energy", "Manufacturing", "Retail"])
    with col2:
        identity_maturity = st.selectbox("Identity Maturity", ["Weak", "Average", "Good", "Strong"])
        defender_active = st.checkbox("Defender Active?", True)
        sentinel_active = st.checkbox("Sentinel Active?", False)
        data_risk = st.selectbox("Data Risk Level", ["Low", "Medium", "High", "Very High"])
    with col3:
        recent_incident = st.checkbox("Recent Security Incident?", False)
        multicloud = st.checkbox("Multi-Cloud Environment?", False)
        cloud_maturity = st.selectbox("Cloud Maturity", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Generate Recommendations")

if submitted:
    client_data = {
        "client_name": client_name,
        "e5_propensity": e5_propensity,
        "identity_maturity": identity_maturity,
        "defender_active": defender_active,
        "sentinel_active": sentinel_active,
        "industry": industry,
        "recent_incident": recent_incident,
        "multicloud": multicloud,
        "data_risk": data_risk,
        "cloud_maturity": cloud_maturity
    }

    recs = evaluate_rules(client_data)
    st.subheader(f"🔎 Recommendations for {client_name}")

    if not recs:
        st.info("No specific recommendations found for this profile. Try adjusting the inputs.")
    else:
        for rec in recs:
            with st.expander(f"✅ {rec['Solution Area']} – {rec['Primary Offer']}"):
                st.write(f"**Follow-up Offer:** {rec['Follow-up Offer']}")
                st.write(f"**Rationale:** {rec['Rationale']}")
                st.write(f"**Timeline:** {rec['Timeline']}")

    st.markdown("---")
    st.subheader("📦 Offer Catalog")
    for category, offers in OFFER_CATALOG.items():
        with st.expander(f"{category}"):
            for offer in offers:
                st.write(f"- {offer}")

st.markdown("---")
st.caption("Avanade | Microsoft Security Sales Intelligence Assistant – powered by Streamlit 🚀")

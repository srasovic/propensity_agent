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
    Rule-based engine mapping client propensity, ACR, and posture
    to solution areas + offers.
    """

    propensity = client.get("e5_propensity", 0)
    security_acr = client.get("security_acr", "medium").lower()
    sentinel_acr = client.get("sentinel_acr", "medium").lower()
    identity_maturity = client.get("identity_maturity", "unknown").lower()
    defender_active = client.get("defender_active", False)
    sentinel_active = client.get("sentinel_active", False)
    industry = client.get("industry", "general").lower()
    recent_incident = client.get("recent_incident", False)
    multicloud = client.get("multicloud", False)
    data_risk = client.get("data_risk", "medium").lower()
    cloud_maturity = client.get("cloud_maturity", "medium").lower()

    recs = []

    # === IAM Recommendations ===
    if propensity < 40 or identity_maturity in ["weak", "none", "poor"]:
        recs.append({
            "Solution Area": "IAM",
            "Primary Offer": "Identity Diagnostics",
            "Follow-up Offer": "Identity Modernization",
            "Rationale": "Low identity maturity or limited E5 readiness. Begin with diagnostics to identify Entra security gaps before modernization.",
            "Timeline": "2–4 weeks"
        })
    elif 40 <= propensity < 80 and identity_maturity in ["average", "good"]:
        recs.append({
            "Solution Area": "IAM",
            "Primary Offer": "Identity Modernization",
            "Follow-up Offer": "Identity Diagnostics",
            "Rationale": "Moderate readiness with decent identity posture. Focus on Conditional Access, PIM automation, and governance.",
            "Timeline": "4–6 weeks"
        })

    # === Data & AI Security ===
    if data_risk in ["high", "very high"]:
        recs.append({
            "Solution Area": "Data & AI Security",
            "Primary Offer": "Data & AI Security Diagnostics",
            "Follow-up Offer": "Data Protection Modernization",
            "Rationale": "High data risk detected. Run diagnostic to assess labeling, insider risk, and AI data protection.",
            "Timeline": "3–5 weeks"
        })
    elif propensity >= 60 and data_risk == "medium":
        recs.append({
            "Solution Area": "Data & AI Security",
            "Primary Offer": "Data Protection Modernization",
            "Follow-up Offer": "Data & AI Security Diagnostics",
            "Rationale": "Moderate data risk with E5 potential. Prioritize modernization to extend Microsoft Purview and Insider Risk tools.",
            "Timeline": "4–6 weeks"
        })

    # === SecOps ===
    if (security_acr in ["large", "very large"] or sentinel_acr in ["large", "very large"]) and propensity >= 70:
        recs.append({
            "Solution Area": "SecOps",
            "Primary Offer": "Unified Threat Protection (Sentinel, TI, Defender XDR, Copilot)",
            "Follow-up Offer": "Security Copilot Accelerator (including Agentic)",
            "Rationale": "High ACR and E5 readiness suggest opportunity for integrated SOC. Deploy unified detection and AI-assisted incident response.",
            "Timeline": "4–6 weeks"
        })
    elif propensity >= 80 and (defender_active or sentinel_active):
        recs.append({
            "Solution Area": "SecOps",
            "Primary Offer": "RED Sentinel",
            "Follow-up Offer": "Unified Threat Protection (Sentinel, TI, Defender XDR, Copilot)",
            "Rationale": "High E5 and security ACR levels with active Defender or Sentinel. Deploy RED Sentinel to accelerate modernization.",
            "Timeline": "4–6 weeks"
        })
    elif 40 <= propensity < 80 and security_acr in ["small", "medium"] and not sentinel_active:
        recs.append({
            "Solution Area": "SecOps",
            "Primary Offer": "RED Defender",
            "Follow-up Offer": "Security Copilot Accelerator (including Agentic)",
            "Rationale": "Mid-level E5 readiness and medium security ACR. Start with Defender hardening and introduce Copilot for AI-driven detection.",
            "Timeline": "4–5 weeks"
        })

    # === Cloud Security ===
    if multicloud and cloud_maturity in ["medium", "low"]:
        recs.append({
            "Solution Area": "Cloud Security",
            "Primary Offer": "Cloud Security Optimization (CSPM)",
            "Follow-up Offer": "Cloud Security Modernization (CWPP)",
            "Rationale": "Multi-cloud setup with incomplete visibility. Optimize CSPM and extend CWPP workload protection.",
            "Timeline": "4–6 weeks"
        })
    elif cloud_maturity == "high" and propensity >= 60:
        recs.append({
            "Solution Area": "Cloud Security",
            "Primary Offer": "Cloud Security Modernization (CWPP)",
            "Follow-up Offer": "Cloud Security Optimization (CSPM)",
            "Rationale": "High E5 readiness with mature cloud environment. Focus on CWPP for advanced container and workload protection.",
            "Timeline": "4–6 weeks"
        })

    # === Cross-Solution ===
    if propensity >= 70 and (security_acr in ["large", "very large"]) and len(recs) >= 3:
        recs.append({
            "Solution Area": "Cross-Solution Security",
            "Primary Offer": "Zero Trust Maturity Roadmap",
            "Follow-up Offer": "Microsoft Security Factory Integration",
            "Rationale": "Multiple solution areas active. Recommend Zero Trust roadmap to integrate IAM, Data, Cloud, and SecOps programs.",
            "Timeline": "6–8 weeks"
        })

    return recs


# -----------------------
# STREAMLIT UI
# -----------------------

st.set_page_config(page_title="Microsoft Security Recommendation Agent", page_icon="🧠", layout="wide")

st.title("🧠 Microsoft Security Recommendation Agent")
st.markdown("Generate security solution recommendations based on E3/E5 propensity, ACR, and security posture across IAM, Data & AI, SecOps, and Cloud Security.")

with st.form("client_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        client_name = st.text_input("Client Name", "Contoso Ltd")
        e5_propensity = st.slider("E5 Propensity (%)", 0, 100, 75)
        industry = st.selectbox("Industry", ["General", "Finance", "Healthcare", "Energy", "Manufacturing", "Retail"])
        security_acr = st.selectbox("Security ACR Size", ["Small", "Medium", "Large", "Very Large"])
    with col2:
        sentinel_acr = st.selectbox("Sentinel ACR Size", ["Small", "Medium", "Large", "Very Large"])
        identity_maturity = st.selectbox("Identity Maturity", ["Weak", "Average", "Good", "Strong"])
        defender_active = st.checkbox("Defender Active?", True)
        sentinel_active = st.checkbox("Sentinel Active?", False)
    with col3:
        data_risk = st.selectbox("Data Risk Level", ["Low", "Medium", "High", "Very High"])
        cloud_maturity = st.selectbox("Cloud Maturity", ["Low", "Medium", "High"])
        multicloud = st.checkbox("Multi-Cloud Environment?", False)
        recent_incident = st.checkbox("Recent Security Incident?", False)

    submitted = st.form_submit_button("Generate Recommendations")

if submitted:
    client_data = {
        "client_name": client_name,
        "e5_propensity": e5_propensity,
        "security_acr": security_acr,
        "sentinel_acr": sentinel_acr,
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

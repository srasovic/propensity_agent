import streamlit as st
import pandas as pd

# -----------------------
# RULE ENGINE DEFINITION
# -----------------------

def evaluate_rules(client):
    """
    Simple rule-based engine for mapping client propensity data
    to recommended Microsoft Security offers.
    """

    propensity = client.get("e5_propensity", 0)
    identity_maturity = client.get("identity_maturity", "unknown").lower()
    defender_active = client.get("defender_active", False)
    sentinel_active = client.get("sentinel_active", False)
    industry = client.get("industry", "general").lower()
    recent_incident = client.get("recent_incident", False)
    multicloud = client.get("multicloud", False)

    recommendations = []

    # R1 - High E5, Sentinel present but underutilized
    if propensity >= 80 and sentinel_active:
        recommendations.append({
            "Rule": "R1",
            "Offer": "RED Sentinel – Premium",
            "Rationale": "High E5 readiness with Sentinel already deployed. Premium upgrade enables advanced analytics, Defender XDR integration, and automation playbooks.",
            "Timeline": "4–6 weeks",
            "Next Steps": ["Run Sentinel health check", "Integrate Defender XDR", "Schedule pilot kickoff"]
        })

    # R2 - High E5, Defender active but no Sentinel
    elif propensity >= 80 and defender_active and not sentinel_active:
        recommendations.append({
            "Rule": "R2",
            "Offer": "RED Sentinel – Standard + Defender XDR Integration",
            "Rationale": "Strong E5 foundation with Defender in place. Deploy Sentinel Standard to consolidate SOC operations and accelerate detection.",
            "Timeline": "4 weeks",
            "Next Steps": ["Map Defender connectors", "Deploy baseline analytics rules"]
        })

    # R3 - Medium E5, strong identity, no XDR
    elif 40 <= propensity < 80 and identity_maturity in ["good", "strong"]:
        recommendations.append({
            "Rule": "R3",
            "Offer": "RED Sentinel – Standard",
            "Rationale": "Moderate E5 readiness and strong identity posture. Sentinel Standard provides centralized visibility and faster detection.",
            "Timeline": "4–5 weeks",
            "Next Steps": ["Connect AAD & M365 data", "Deploy essential workbooks"]
        })

    # R4 - Medium E5, weak identity
    elif 40 <= propensity < 80 and identity_maturity in ["weak", "none", "poor"]:
        recommendations.append({
            "Rule": "R4",
            "Offer": "Entra Security Hardening + IAM Diagnostics",
            "Rationale": "Identity weaknesses detected. Start with Entra hardening and IAM diagnostics before broader deployment.",
            "Timeline": "2–3 weeks",
            "Next Steps": ["Assess MFA/CA gaps", "Prepare Entra rollout plan"]
        })

    # R5 - Low E5, E3-only
    elif propensity < 40 and not defender_active and not sentinel_active:
        recommendations.append({
            "Rule": "R5",
            "Offer": "IAM Diagnostics Assessment",
            "Rationale": "Low E5 adoption and limited security signals. Assessment builds the business case for E5 upgrade.",
            "Timeline": "2 weeks",
            "Next Steps": ["Collect tenant data", "Create risk heatmap"]
        })

    # R6 - High E5, Entra + Defender active, no Sentinel
    elif propensity >= 80 and not sentinel_active and identity_maturity in ["good", "strong"]:
        recommendations.append({
            "Rule": "R6",
            "Offer": "RED Sentinel – Premium + Security Copilot Integration",
            "Rationale": "Strong E5 foundation; adding Sentinel + Copilot delivers unified detection and AI-assisted investigation.",
            "Timeline": "4–6 weeks",
            "Next Steps": ["Deploy Sentinel", "Integrate Copilot"]
        })

    # R7 - Regulated industries
    if industry in ["finance", "healthcare", "energy"]:
        recommendations.append({
            "Rule": "R7",
            "Offer": "RED Sentinel – Premium + Compliance Pack",
            "Rationale": "Regulated industry identified. Add compliance workbooks and audit dashboards for reporting.",
            "Timeline": "6 weeks",
            "Next Steps": ["Configure compliance analytics", "Deliver executive compliance reports"]
        })

    # R9 - Low E5, but recent breach
    if recent_incident and propensity < 60:
        recommendations.append({
            "Rule": "R9",
            "Offer": "Incident Response Readiness Workshop + Rapid Sentinel Deployment (Lite)",
            "Rationale": "Recent incident detected. Rapid deployment improves containment and visibility.",
            "Timeline": "3–4 weeks",
            "Next Steps": ["Deploy Sentinel Lite", "Enable core log ingestion"]
        })

    # R10 - Multi-cloud environment
    if multicloud and propensity >= 60:
        recommendations.append({
            "Rule": "R10",
            "Offer": "RED Sentinel – Premium (Multi-Cloud)",
            "Rationale": "Multi-cloud detected. Sentinel Premium enables cross-cloud visibility and threat correlation.",
            "Timeline": "6 weeks",
            "Next Steps": ["Configure AWS/GCP connectors", "Deploy hybrid dashboards"]
        })

    return recommendations


# -----------------------
# STREAMLIT UI
# -----------------------

st.set_page_config(page_title="Microsoft Security Recommendation Agent", page_icon="🧠", layout="wide")

st.title("🧠 Microsoft Security Recommendation Agent")
st.markdown("Upload client data or enter it manually to generate solution recommendations based on E3/E5 propensity and security posture.")

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
    with col3:
        recent_incident = st.checkbox("Recent Security Incident?", False)
        multicloud = st.checkbox("Multi-Cloud Environment?", False)
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
        "multicloud": multicloud
    }

    recs = evaluate_rules(client_data)
    st.subheader(f"🔎 Recommendations for {client_name}")

    if not recs:
        st.info("No specific recommendations found for this profile. Try adjusting the inputs.")
    else:
        for rec in recs:
            with st.expander(f"✅ {rec['Offer']} ({rec['Rule']})"):
                st.write(f"**Rationale:** {rec['Rationale']}")
                st.write(f"**Timeline:** {rec['Timeline']}")
                st.write("**Next Steps:**")
                for step in rec["Next Steps"]:
                    st.write(f"- {step}")

st.markdown("---")
st.caption("Avanade | Microsoft Security Sales Intelligence Assistant – powered by Streamlit 🚀")

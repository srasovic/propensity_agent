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

# -----

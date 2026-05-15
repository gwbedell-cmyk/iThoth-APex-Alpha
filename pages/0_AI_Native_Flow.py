import streamlit as st
import json
from services.evaluator import evaluate_action
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

def load_css():
    with open("assets/css.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

with open("data/scenarios.json") as f:
    actions = json.load(f)

scenario_map = {
    "Invoice_ACME_Approved_18K.pdf": "ACT-002",
    "Invoice_Duplicate_125K.pdf": "ACT-001",
    "Vendor_Bank_Update_Request.pdf": "ACT-003",
    "Treasury_Transfer_Exception.csv": "ACT-008",
    "Executive_Exception_Request.pdf": "ACT-004"
}

artifact_metadata = {
    "Invoice_ACME_Approved_18K.pdf": {
        "vendor": "ACME Industrial",
        "amount": "$18,000",
        "objective": "Approve Supplier Payment"
    },
    "Invoice_Duplicate_125K.pdf": {
        "vendor": "Global Supply Corp",
        "amount": "$125,000",
        "objective": "Approve Supplier Payment"
    },
    "Vendor_Bank_Update_Request.pdf": {
        "vendor": "NorthBridge Logistics",
        "amount": "$92,000",
        "objective": "Update Vendor Banking"
    },
    "Treasury_Transfer_Exception.csv": {
        "vendor": "Treasury Operations",
        "amount": "$250,000",
        "objective": "Release Treasury Transfer"
    },
    "Executive_Exception_Request.pdf": {
        "vendor": "Strategic Vendor",
        "amount": "$175,000",
        "objective": "Approve Exception Payment"
    }
}

st.markdown("""
<h1 style='color:#1e5eff; margin-bottom:0.2rem;'>
AI-native Enterprise Flow
</h1>
<p style='color:#4a90e2; font-size:1.05rem; margin-top:0;'>
Enterprise context enters. AI proposes. APex governs.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<h3 style='color:#2563eb;'>
Click an Artifact to Upload
</h3>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

selected_artifact = None

with col1:
    if st.button("📄 Invoice_ACME_Approved_18K.pdf"):
        selected_artifact = "Invoice_ACME_Approved_18K.pdf"

with col2:
    if st.button("📄 Invoice_Duplicate_125K.pdf"):
        selected_artifact = "Invoice_Duplicate_125K.pdf"

with col3:
    if st.button("📄 Vendor_Bank_Update_Request.pdf"):
        selected_artifact = "Vendor_Bank_Update_Request.pdf"

with col4:
    if st.button("📊 Treasury_Transfer_Exception.csv"):
        selected_artifact = "Treasury_Transfer_Exception.csv"

with col5:
    if st.button("📄 Executive_Exception_Request.pdf"):
        selected_artifact = "Executive_Exception_Request.pdf"

st.markdown("---")

st.file_uploader(
    "Production artifact ingestion interface",
    disabled=True
)

if selected_artifact:
    selected_id = scenario_map[selected_artifact]

    proposed = next(
        a for a in actions
        if a["id"] == selected_id
    )

    evaluation = evaluate_action(proposed)
    color = decision_color(evaluation["decision"])
    artifact = artifact_metadata[selected_artifact]

    st.success(f"Artifact uploaded: {selected_artifact}")

    st.markdown("---")

    st.markdown("""
    <h3 style='color:#2563eb;'>
    Structured Extraction
    </h3>
    """, unsafe_allow_html=True)

    st.write(f"Vendor: {artifact['vendor']}")
    st.write(f"Transaction Amount: {artifact['amount']}")
    st.write(f"AI Proposed Objective: {artifact['objective']}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <h3 style='color:#2563eb;'>
        Proposed Autonomous Action
        </h3>
        """, unsafe_allow_html=True)

        st.write(f"Action: {proposed['action_type']}")
        st.write(f"Vendor: {proposed['vendor_name']}")
        st.write(f"Amount: ${proposed['amount']:,.0f}")
        st.write(f"Agent Confidence: {int(proposed['confidence'] * 100)}%")

    with col2:
        st.markdown("""
        <h3 style='color:#2563eb;'>
        APex Trust Evaluation
        </h3>
        """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:20px;
                border-radius:16px;
                color:white;
                text-align:center;
            ">
                <h2>{evaluation['decision']}</h2>
                <h3>APex Risk Score: {evaluation['risk_score']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown("""
    <h3 style='color:#2563eb;'>
    Triggered Findings
    </h3>
    """, unsafe_allow_html=True)

    for finding in evaluation["explanations"]:
        st.write(f"• {finding}")

    st.markdown("---")

    if evaluation["risk_score"] <= 25:
        if st.button("Execute"):
            st.success("Execution initiated.")
    else:
        if st.button("Escalate to APex Governance"):
            st.success("Execution proposal escalated to governance control plane.")
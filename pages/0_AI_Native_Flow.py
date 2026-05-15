import streamlit as st
import json
from services.evaluator import evaluate_action
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

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

st.title("AI-native Enterprise Flow")
st.caption("Enterprise context enters. AI proposes. APex governs.")

st.markdown("---")

uploaded_file = st.file_uploader(
    "Drag & drop a demo enterprise artifact",
    accept_multiple_files=False
)

if uploaded_file is None:
    st.info("Upload one of the APex demo artifacts to initiate governed autonomous execution.")

else:
    filename = uploaded_file.name

    if filename not in scenario_map:
        st.error("Artifact recognized, but no matching APex demo scenario is available.")
    else:
        selected_id = scenario_map[filename]

        proposed = next(
            a for a in actions
            if a["id"] == selected_id
        )

        evaluation = evaluate_action(proposed)
        color = decision_color(evaluation["decision"])
        artifact = artifact_metadata[filename]

        st.success(f"Artifact recognized: {filename}")

        st.markdown("---")

        st.subheader("Structured Extraction")

        st.write(f"Vendor: {artifact['vendor']}")
        st.write(f"Transaction Amount: {artifact['amount']}")
        st.write(f"AI Proposed Objective: {artifact['objective']}")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Proposed Autonomous Action")
            st.write(f"Action: {proposed['action_type']}")
            st.write(f"Vendor: {proposed['vendor_name']}")
            st.write(f"Amount: ${proposed['amount']:,.0f}")
            st.write(f"Agent Confidence: {int(proposed['confidence'] * 100)}%")

        with col2:
            st.markdown("### APex Trust Evaluation")

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

        st.subheader("Triggered Findings")

        for finding in evaluation["explanations"]:
            st.write(f"• {finding}")

        st.markdown("---")

        if evaluation["risk_score"] == 0:
            if st.button("Execute"):
                st.success("Execution initiated.")
        else:
            if st.button("Escalate to APex Governance"):
                st.success("Execution proposal escalated to governance control plane.")
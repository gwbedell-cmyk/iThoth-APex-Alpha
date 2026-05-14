import streamlit as st
import json
from services.evaluator import evaluate_action
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

scenario_map = {
    "Clean Payment": "ACT-002",
    "Duplicate Invoice Fraud": "ACT-001",
    "Vendor Account Takeover": "ACT-003",
    "Treasury Anomaly": "ACT-008",
    "Executive Exception": "ACT-004"
}

st.title("AI-native Enterprise Flow")
st.caption("Enterprise context enters. AI proposes. APex governs.")

st.markdown("---")

preset = st.selectbox(
    "Demo Scenario Preset",
    list(scenario_map.keys())
)

uploaded_files = st.file_uploader(
    "Drop invoices, contracts, ERP exports, or vendor records here",
    accept_multiple_files=True
)

workflow_prompt = st.text_area(
    "Execution Objective",
    placeholder="Review enterprise artifacts, identify execution candidates, and generate a governed proposal."
)

st.markdown("---")

if st.button("Generate Execution Proposal"):
    selected_id = scenario_map[preset]

    proposed = next(
        a for a in actions
        if a["id"] == selected_id
    )

    evaluation = evaluate_action(proposed)
    color = decision_color(evaluation["decision"])

    st.success("Execution proposal generated from enterprise context.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Proposed Autonomous Action")
        st.write(f"Action: {proposed['action_type']}")
        st.write(f"Vendor: {proposed['vendor_name']}")
        st.write(f"Amount: ${proposed['amount']:,.0f}")
        st.write(f"Agent Confidence: {int(proposed['confidence'] * 100)}%")

    with col2:
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
                <h3>Risk Score: {evaluation['risk_score']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("Triggered Findings")

    for finding in evaluation["explanations"]:
        st.write(f"• {finding}")

    st.markdown("---")

    if st.button("Forward to APex Governance"):
        st.success("Execution proposal forwarded to governance control plane.")
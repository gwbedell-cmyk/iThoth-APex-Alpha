import streamlit as st
import json
from services.evaluator import evaluate_action
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

st.title("AI-native Enterprise Flow")
st.caption("Enterprise context enters. AI proposes. APex governs.")

st.markdown("---")

uploaded_files = st.file_uploader(
    "Drop invoices, contracts, ERP exports, or vendor records here",
    accept_multiple_files=True
)

workflow_prompt = st.text_area(
    "Execution Objective",
    placeholder="Example: Review attached invoices, validate vendor consistency, identify payment candidates, and generate an execution proposal."
)

st.markdown("---")

if st.button("Generate Execution Proposal"):
    st.success("Execution proposal generated from enterprise context.")

    with open("data/scenarios.json") as f:
        actions = json.load(f)

    proposed = actions[0]
    evaluation = evaluate_action(proposed)
    color = decision_color(evaluation["decision"])

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

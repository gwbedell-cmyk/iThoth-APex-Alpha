import streamlit as st
import json
from services.evaluator import evaluate_action
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Scenario Control")
st.caption("Interactive autonomous execution test environment")

selected = st.selectbox(
    "Select Scenario",
    actions,
    format_func=lambda x: f"{x['id']} — {x['action_type']} — {x['vendor_name']}"
)

evaluation = evaluate_action(selected)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Autonomous Agent Proposal")

    st.write(f"**Agent ID:** {selected['agent_id']}")
    st.write(f"**Action Type:** {selected['action_type']}")
    st.write(f"**Vendor:** {selected['vendor_name']}")
    st.write(f"**Invoice:** {selected['invoice_id']}")
    st.write(f"**Amount:** ${selected['amount']:,.0f}")
    st.write(f"**Confidence:** {int(selected['confidence'] * 100)}%")

with col2:
    st.subheader("APex Trust Evaluation")

    color = decision_color(evaluation["decision"])

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

for item in evaluation["explanations"]:
    st.write(f"• {item}")

st.markdown("---")

st.subheader("Triggered Policies")

for policy in evaluation["triggered_policies"]:
    st.write(f"• {policy}")
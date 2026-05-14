import streamlit as st
import json
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Decision Analysis")

selected = st.selectbox(
    "Select Autonomous Action",
    actions,
    format_func=lambda x: f"{x['id']} — {x['vendor_name']}"
)

evaluation = evaluate_action(selected)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Proposed Action")
    st.write(f"Agent: {selected['agent_id']}")
    st.write(f"Vendor: {selected['vendor_name']}")
    st.write(f"Invoice: {selected['invoice_id']}")
    st.write(f"Amount: ${selected['amount']:,.0f}")

with col2:
    st.subheader("APex Verdict")
    st.metric("Decision", evaluation["decision"])
    st.metric("Risk Score", evaluation["risk_score"])

st.markdown("---")

st.subheader("Findings")

for item in evaluation["explanations"]:
    st.write(f"• {item}")
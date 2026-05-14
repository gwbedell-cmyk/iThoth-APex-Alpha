import streamlit as st
import json
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

evaluations = [evaluate_action(a) for a in actions]

blocked = sum(1 for e in evaluations if e["decision"] in ["BLOCK", "HARD BLOCK"])
review = sum(1 for e in evaluations if e["decision"] == "REVIEW")
total_value = sum(a["amount"] for a in actions)

st.title("Executive Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Autonomous Actions Today", len(actions))

with col2:
    st.metric("Protected Enterprise Value", f"${total_value:,.0f}")

with col3:
    st.metric("Blocked Executions", blocked)

with col4:
    st.metric("Review Queue", review)

st.markdown("---")

st.subheader("Live Trust Evaluations")

for action, evaluation in zip(actions, evaluations):
    with st.expander(f"{action['vendor_name']} — {evaluation['decision']}"):
        st.write(f"Action: {action['action_type']}")
        st.write(f"Amount: ${action['amount']:,.0f}")
        st.write(f"Risk Score: {evaluation['risk_score']}")

        st.write("Findings:")
        for item in evaluation["explanations"]:
            st.write(f"• {item}")
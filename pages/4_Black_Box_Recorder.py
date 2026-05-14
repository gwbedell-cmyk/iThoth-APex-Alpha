import streamlit as st
import json
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Black Box Recorder for Cognitive Intelligence™")

for action in actions:
    evaluation = evaluate_action(action)

    with st.expander(f"{action['id']} — {evaluation['decision']}"):
        st.write(f"Timestamp: Simulated")
        st.write(f"Agent: {action['agent_id']}")
        st.write(f"Decision: {evaluation['decision']}")
        st.write(f"Risk Score: {evaluation['risk_score']}")

        st.subheader("Triggered Policies")
        for policy in evaluation["triggered_policies"]:
            st.write(f"• {policy}")
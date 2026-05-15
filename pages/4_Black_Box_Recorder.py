import streamlit as st
import json
from datetime import datetime, timedelta
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Black Box Recorder for Cognitive Intelligence™")
st.caption("Forensic execution testimony for autonomous enterprise actions")

base_time = datetime.utcnow()

for idx, action in enumerate(actions):
    evaluation = evaluate_action(action)

    event_time = base_time - timedelta(minutes=(idx * 7))

    with st.expander(f"{action['id']} — {evaluation['decision']}"):
        st.write(f"Captured Event: {event_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        st.write(f"Agent: {action['agent_id']}")
        st.write(f"Decision: {evaluation['decision']}")
        st.write(f"APex Risk Score: {evaluation['risk_score']}")

        st.subheader("Triggered Policies")
        for policy in evaluation["triggered_policies"]:
            st.write(f"• {policy}")
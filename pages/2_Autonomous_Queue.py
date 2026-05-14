import streamlit as st
import json
import pandas as pd
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

rows = []

for action in actions:
    evaluation = evaluate_action(action)

    rows.append({
        "Action ID": action["id"],
        "Agent": action["agent_id"],
        "Action": action["action_type"],
        "Vendor": action["vendor_name"],
        "Amount": f"${action['amount']:,.0f}",
        "Confidence": f"{int(action['confidence'] * 100)}%",
        "Decision": evaluation["decision"],
        "Risk Score": evaluation["risk_score"]
    })

st.title("Autonomous Execution Queue")
st.caption("Live autonomous actions awaiting governance evaluation")

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)
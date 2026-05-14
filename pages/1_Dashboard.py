import streamlit as st
import json
import pandas as pd
import plotly.express as px

from services.evaluator import evaluate_action
from services.audit import record_decision

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

evaluations = []

for action in actions:
    evaluation = evaluate_action(action)
    record_decision(action, evaluation)
    evaluations.append(evaluation)

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

rows = []

for action, evaluation in zip(actions, evaluations):
    rows.append({
        "Vendor": action["vendor_name"],
        "Decision": evaluation["decision"],
        "Risk Score": evaluation["risk_score"],
        "Amount": action["amount"]
    })

df = pd.DataFrame(rows)

left, right = st.columns(2)

with left:
    st.subheader("Decision Distribution")

    fig = px.pie(
        df,
        names="Decision"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Risk Scores by Vendor")

    fig = px.bar(
        df,
        x="Vendor",
        y="Risk Score"
    )

    st.plotly_chart(fig, use_container_width=True)

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
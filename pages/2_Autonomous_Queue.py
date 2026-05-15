import streamlit as st
import json
from services.evaluator import evaluate_action

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Live Governance Queue")
st.caption("Human governance control for autonomous enterprise execution")

if "execution_queue" not in st.session_state:
    queue = []

    for action in actions:
        evaluation = evaluate_action(action)

        if evaluation["risk_score"] <= 25:
            status = "Ready"
        elif evaluation["risk_score"] < 75:
            status = "Review Required"
        else:
            status = "Blocked"

        queue.append({
            "id": action["id"],
            "agent": action["agent_id"],
            "action": action["action_type"],
            "vendor": action["vendor_name"],
            "amount": action["amount"],
            "decision": evaluation["decision"],
            "risk": evaluation["risk_score"],
            "status": status
        })

    st.session_state.execution_queue = queue

queue = st.session_state.execution_queue

if not queue:
    st.success("No autonomous actions currently awaiting governance review.")

for idx, item in enumerate(queue.copy()):
    st.markdown("---")

    st.subheader(f"{item['id']} — {item['action']}")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.write(f"Vendor: {item['vendor']}")
        st.write(f"Amount: ${item['amount']:,.0f}")

    with c2:
        st.write(f"Agent: {item['agent']}")
        st.write(f"APex Risk Score: {item['risk']}")

    with c3:
        st.write(f"Decision: {item['decision']}")
        st.write(f"Status: {item['status']}")

    with c4:
        if item["status"] == "Ready":
            if st.button("Execute", key=f"execute_{idx}"):
                st.session_state.execution_queue.remove(item)
                st.success(f"{item['id']} executed.")
                st.rerun()

            if st.button("Hold", key=f"hold_{idx}"):
                item["status"] = "Held"
                st.rerun()

        elif item["status"] == "Review Required":
            if st.button("Execute", key=f"execute_review_{idx}"):
                st.session_state.execution_queue.remove(item)
                st.success(f"{item['id']} executed.")
                st.rerun()

            if st.button("Hold", key=f"hold_review_{idx}"):
                item["status"] = "Held"
                st.rerun()

            if st.button("Escalate", key=f"escalate_{idx}"):
                item["status"] = "Escalated"
                st.rerun()

        elif item["status"] == "Blocked":
            if st.button("Override", key=f"override_{idx}"):
                st.session_state.execution_queue.remove(item)
                st.success(f"{item['id']} override approved and executed.")
                st.rerun()

            if st.button("Escalate", key=f"blocked_escalate_{idx}"):
                item["status"] = "Escalated"
                st.rerun()

        elif item["status"] == "Escalated":
            if st.button("Execute", key=f"execute_escalated_{idx}"):
                st.session_state.execution_queue.remove(item)
                st.success(f"{item['id']} executed.")
                st.rerun()

            if st.button("Block", key=f"block_escalated_{idx}"):
                item["status"] = "Blocked"
                st.rerun()

        elif item["status"] == "Held":
            if st.button("Resume", key=f"resume_{idx}"):
                item["status"] = "Ready"
                st.rerun()

            if st.button("Cancel", key=f"cancel_{idx}"):
                st.session_state.execution_queue.remove(item)
                st.warning(f"{item['id']} cancelled.")
                st.rerun()
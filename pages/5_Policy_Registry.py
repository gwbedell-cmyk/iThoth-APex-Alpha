import streamlit as st
import json

st.set_page_config(layout="wide")

LOCKED_POLICIES = {
    "P-06": "Enterprise trust intelligence module required",
    "P-08": "Treasury systems integration required",
    "P-19": "ERP connector required",
    "P-20": "Contract intelligence module required"
}

with open("data/policies.json") as f:
    policies = json.load(f)

st.title("Policy Control Center")
st.caption("Governance controls for autonomous enterprise execution")

for policy in policies:
    locked = policy["id"] in LOCKED_POLICIES
    toggle_key = f"toggle_{policy['id']}"

    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])

        with col1:
            st.write(f"### {policy['id']}")

        with col2:
            st.write(f"**{policy['name']}**")
            st.write(policy["description"])
            st.write(f"Risk Weight: {policy['weight']}")

            if locked:
                st.caption(f"🔒 {LOCKED_POLICIES[policy['id']]}")

        with col3:
            if locked:
                st.toggle(
                    "Disabled",
                    value=False,
                    key=f"locked_{policy['id']}",
                    disabled=True
                )
            else:
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = policy["enabled"]

                current_state = st.session_state[toggle_key]

                st.toggle(
                    "Enabled" if current_state else "Disabled",
                    key=toggle_key
                )

        st.markdown("---")
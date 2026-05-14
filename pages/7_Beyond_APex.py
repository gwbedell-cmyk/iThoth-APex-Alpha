import streamlit as st

st.set_page_config(layout="wide")

st.title("Beyond APex")
st.caption("The expansion path from AP trust controls to universal autonomous economic execution")

st.markdown("---")

st.markdown("""
<div style="
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow: 0 8px 24px rgba(15,23,42,0.08);
">
    <h2 style="text-align:center; color:#0f172a;">APex Architecture Stack</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Layer 1
st.markdown("""
<div style="
    background:#0f172a;
    padding:24px;
    border-radius:18px;
    color:white;
    text-align:center;
">
    <h2>APex</h2>
    <p style="color:white;">
        Independent Trust Control for Autonomous Enterprise Execution
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>↓</h1>",
    unsafe_allow_html=True
)

# Layer 2
st.markdown("""
<div style="
    background:#1e293b;
    padding:24px;
    border-radius:18px;
    color:white;
    text-align:center;
">
    <h2>EPCs</h2>
    <p style="color:white;">
        Transaction-scoped programmable treasury execution
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>↓</h1>",
    unsafe_allow_html=True
)

# Layer 3
st.markdown("""
<div style="
    background:#334155;
    padding:24px;
    border-radius:18px;
    color:white;
    text-align:center;
">
    <h2>SettlementOS</h2>
    <p style="color:white;">
        Governed liquidity-agnostic economic execution infrastructure
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.subheader("Strategic Expansion")

st.write("""
APex begins as independent trust control for autonomous enterprise execution.

The same governance architecture extends naturally into transaction-scoped
programmable treasury execution (EPCs), and ultimately into SettlementOS:
a universal governed substrate for autonomous economic workflows.
""")

import streamlit as st

st.set_page_config(page_title="Test App", layout="wide")

st.sidebar.title("🎯 Test Sidebar")
st.sidebar.write("If you see this, the app is working!")

role = st.sidebar.selectbox("Select Role:", ["Director", "Support Officer", "IT Admin"])

st.title("Main Content Area")
st.write(f"Selected role: **{role}**")
st.success("✓ App is rendering correctly!")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Test Metric 1", "100%")
with col2:
    st.metric("Test Metric 2", "85%")
with col3:
    st.metric("Test Metric 3", "95%")

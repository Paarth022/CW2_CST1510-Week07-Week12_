import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Multi-Domain Intelligence Platform")
st.markdown("---")

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state.current_user = None
    
if "current_role" not in st.session_state:
    st.session_state.current_role = None

# Check if user is logged in
if st.session_state.current_user is None:
    st.info("👈 Please log in using the Login page to access the platform.")
    
    st.markdown("---")
    st.subheader("Welcome to the Platform")
    st.write("""
    This Multi-Domain Intelligence Platform provides integrated tools for:
    
    - **🔐 Authentication**: Secure user management and login
    - **🛡️ Cybersecurity**: Incident tracking and management
    - **📊 Data Science**: Dataset analysis and exploration
    - **💻 IT Operations**: Support ticket management
    - **🤖 AI Assistant**: Intelligent conversation and analysis
    """)
else:
    st.success(f"✅ Logged in as: **{st.session_state.current_user}** (Role: {st.session_state.current_role})")
    
    st.markdown("---")
    st.subheader("📋 Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🛡️ Security", "Module", "Active")
    
    with col2:
        st.metric("📊 Analytics", "Module", "Active")
    
    with col3:
        st.metric("💻 IT Ops", "Module", "Active")
    
    with col4:
        st.metric("🤖 AI", "Module", "Active")
    
    with col5:
        st.metric("👤 Users", "Status", "Online")
    
    st.markdown("---")
    st.info("Use the sidebar to navigate to different modules.")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.current_user = None
        st.session_state.current_role = None
        st.rerun()
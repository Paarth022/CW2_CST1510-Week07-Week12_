import streamlit as st

st.set_page_config(
    page_title="Settings",
    page_icon="gear",
    layout="wide"
)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")

st.title("Settings")

tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "About"])

with tab1:
    st.subheader("User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Username:")
        st.write(f"`{st.session_state.username}`")
        
        st.write("Role:")
        st.write(f"`{st.session_state.role.upper()}`")
    
    with col2:
        st.write("Account Status:")
        st.success("Active")
        
        st.write("Last Login:")
        st.write("Today at 9:10 PM")
    
    st.divider()
    
    st.subheader("Security")
    
    if st.button("Change Password"):
        st.info("Password change feature coming soon")
    
    if st.button("Enable Two-Factor Authentication"):
        st.info("2FA feature coming soon")

with tab2:
    st.subheader("Preferences")
    
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    notifications = st.checkbox("Enable Notifications", value=True)
    auto_refresh = st.checkbox("Auto-refresh Data", value=True)
    
    if auto_refresh:
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 300, 60)
    
    if st.button("Save Preferences"):
        st.success("Preferences saved!")

with tab3:
    st.subheader("About")
    
    st.markdown("""
    ### Multi-Domain Intelligence Platform
    
    Version: 1.0.0 (Week 9)
    
    Technology Stack:
    - Frontend: Streamlit
    - Backend: Python 3.10+
    - Database: SQLite
    - Authentication: bcrypt
    - Visualization: Plotly
    
    Features:
    - Secure user authentication
    - Multi-page dashboard
    - Real-time data analysis
    - Role-based access control
    - Interactive visualizations
    
    Credits:
    - Course: CST1510 - Coursework 2
    - Institution: Multi-Domain Intelligence Platform
    - Instructor: Teaching Guide
    
    Support: For technical issues, contact your instructor.
    """)
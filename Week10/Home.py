import streamlit as st
import sqlite3
from datetime import datetime
from app.services.user_service import login_user, register_user


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# SESSION STATE INITIALIZATION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""


# LOGIN / REGISTER PAGE
def login_page():
    """Authentication page with login and registration tabs"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 Multi-Domain Intelligence Platform")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Welcome Back")
            with st.form("login_form"):
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                    key="login_username"
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                submit_button = st.form_submit_button("Login", use_container_width=True)
                
                if submit_button:
                    if not username or not password:
                        st.error("❌ Username and password are required")
                    else:
                        success, message = login_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.role = message
                            st.success(f"✅ Login successful! Welcome, {username}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            st.markdown("---")
            st.markdown("Don't have an account? Switch to **Register** tab →")
        
        with tab2:
            st.subheader("Create New Account")
            with st.form("register_form"):
                new_username = st.text_input(
                    "Username",
                    placeholder="Choose a username (3-20 characters)",
                    key="register_username"
                )
                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password (6+ characters)",
                    key="register_password"
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                    key="confirm_password"
                )
                role = st.selectbox(
                    "Select Role",
                    ["user", "analyst", "admin"],
                    key="select_role"
                )
                submit_reg = st.form_submit_button("Register", use_container_width=True)
                
                if submit_reg:
                    if not new_username or not new_password:
                        st.error("❌ All fields are required")
                    elif len(new_username) < 3 or len(new_username) > 20:
                        st.error("❌ Username must be 3-20 characters")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        success, message = register_user(new_username, new_password, role)
                        if success:
                            st.success(f"✅ {message}")
                            st.info("ℹ️ You can now log in with your credentials")
                        else:
                            st.error(f"❌ {message}")
            
            st.markdown("---")
            st.markdown("**🔒 Secure Authentication with bcrypt**")


# MAIN DASHBOARD PAGE
def dashboard_page():
    """Main dashboard with domain navigation"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 User Info")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role.upper()}")
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()
    
    # Main title
    st.title("🔐 Intelligence Platform")
    st.markdown("---")
    
    # Domain selector buttons
    st.markdown("### Select Domain")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔐 Cybersecurity", use_container_width=True, key="cyber_nav"):
            st.switch_page("pages/1_Cybersecurity.py")
    
    with col2:
        if st.button("📊 Data Science", use_container_width=True, key="data_nav"):
            st.switch_page("pages/2_DataScience.py")
    
    with col3:
        if st.button("🔧 IT Operations", use_container_width=True, key="it_nav"):
            st.switch_page("pages/3_ITOperations.py")
    
    st.markdown("---")
    
    # Welcome info
    st.markdown("""
    ### 👋 Welcome to Intelligence Platform
    
    Select a domain above to manage:
    - **🔐 Cybersecurity**: Manage security incidents and threats
    - **📊 Data Science**: Manage datasets and analytics
    - **🔧 IT Operations**: Manage IT tickets and support requests
    
    Each domain includes:
    - 📊 **Overview**: Key metrics and data tables
    - ⚙️ **CRUD Operations**: Create, Read, Update, Delete records
    - 📈 **Analysis**: Charts and insights
    """)
    
    # Statistics
    st.divider()
    st.markdown("### 📊 Platform Statistics")
    
    try:
        conn = sqlite3.connect('intelligence_platform.db')
        cursor = conn.cursor()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
            incidents = cursor.fetchone()[0]
            st.metric("🔐 Incidents", incidents)
        
        with col2:
            cursor.execute("SELECT COUNT(*) FROM it_tickets")
            tickets = cursor.fetchone()[0]
            st.metric("🎫 Tickets", tickets)
        
        with col3:
            cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
            datasets = cursor.fetchone()[0]
            st.metric("📊 Datasets", datasets)
        
        conn.close()
    except Exception as e:
        st.warning("⚠️ Could not load statistics")


# MAIN APPLICATION LOGIC
def main():
    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
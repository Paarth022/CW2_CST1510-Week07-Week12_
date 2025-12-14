import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import openai

# PAGE CONFIG & AUTHENTICATION
st.set_page_config(page_title="Cybersecurity", page_icon="🔐", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please log in first!")
    st.stop()


# OPENAI CONFIG
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("❌ OPENAI_API_KEY not found in secrets.toml")
    st.stop()


# DATABASE CONNECTION
def connect_db():
    conn = sqlite3.connect('intelligence_platform.db')
    conn.row_factory = sqlite3.Row
    return conn

# AI HELPER FUNCTION
def get_ai_response(user_message, context):
    """Get response from OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a Cybersecurity AI Assistant. Help analyze security incidents and provide threat intelligence. {context}"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error getting AI response: {str(e)}"


# SIDEBAR & HEADER
with st.sidebar:
    st.write(f"👤 **{st.session_state.username}**")
    st.write(f"🔑 Role: {st.session_state.role.upper()}")
    st.divider()
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("Home.py")

st.title("🔐 Cybersecurity Domain")
st.markdown("---")


# TABS STRUCTURE

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ CRUD Operations", "📈 Analysis", "🤖 AI Chatbot"])
# tab-1
with tab1:
    st.subheader("Cybersecurity Dashboard Overview")
    
    try:
        conn = connect_db()
        incidents_df = pd.read_sql_query(
            "SELECT * FROM cyber_incidents",
            conn
        )
        conn.close()
        
        if not incidents_df.empty:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Incidents", len(incidents_df))
            with col2:
                critical = len(incidents_df[incidents_df['severity'].str.lower() == 'critical'])
                st.metric("🔴 Critical", critical)
            with col3:
                high = len(incidents_df[incidents_df['severity'].str.lower() == 'high'])
                st.metric("🟠 High", high)
            with col4:
                resolved = len(incidents_df[incidents_df['status'].str.lower() == 'resolved'])
                st.metric("✅ Resolved", resolved)
            
            st.divider()
            st.write("### 📋 All Incidents")
            st.dataframe(incidents_df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No incidents data available")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")


# TAB 2: CRUD OPERATIONS
with tab2:
    st.subheader("Incident CRUD Operations")
    
    crud_op = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"],
        key="cyber_crud_op"
    )
    
    st.divider()
    
    # CREATE
    if crud_op == "Create":
        st.write("### ➕ Create New Incident")
        
        with st.form("create_incident_form"):
            title = st.text_input("Incident Title", placeholder="e.g., Phishing Email Campaign")
            description = st.text_area("Description", placeholder="Detailed incident description")
            
            col1, col2 = st.columns(2)
            with col1:
                incident_type = st.selectbox(
                    "Incident Type",
                    ["Phishing", "Malware", "DDoS", "SQL Injection", "Data Breach", "Ransomware", "Social Engineering"]
                )
            with col2:
                severity = st.selectbox(
                    "Severity",
                    ["low", "medium", "high", "critical"]
                )
            
            col3, col4 = st.columns(2)
            with col3:
                status = st.selectbox("Status", ["open", "investigating", "resolved"])
            with col4:
                reported_by = st.text_input("Reported By", placeholder="e.g., user@company.com")
            
            if st.form_submit_button("Create Incident", use_container_width=True):
                if not all([title, description, reported_by]):
                    st.error("❌ All fields are required")
                else:
                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO cyber_incidents 
                            (date, incident_type, severity, status, description, reported_by)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (datetime.now().date(), incident_type, severity, status, description, reported_by))
                        conn.commit()
                        conn.close()
                        st.success("✅ Incident created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # READ
    elif crud_op == "Read":
        st.write("### 📖 View All Incidents")
        
        try:
            conn = connect_db()
            incidents = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
            conn.close()
            
            if not incidents.empty:
                st.dataframe(incidents, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No incidents found")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # UPDATE
    elif crud_op == "Update":
        st.write("### ✏️ Update Incident")
        
        incident_id = st.number_input("Incident ID to Update", min_value=1, step=1)
        
        with st.form("update_incident_form"):
            severity = st.selectbox("Severity", ["low", "medium", "high", "critical", "skip"], index=4)
            status = st.selectbox("Status", ["open", "investigating", "resolved", "skip"], index=3)
            
            if st.form_submit_button("Update Incident", use_container_width=True):
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    
                    updates = []
                    params = []
                    
                    if severity != "skip":
                        updates.append("severity = ?")
                        params.append(severity)
                    if status != "skip":
                        updates.append("status = ?")
                        params.append(status)
                    
                    if not updates:
                        st.warning("⚠️ No fields to update")
                    else:
                        params.append(incident_id)
                        query = f"UPDATE cyber_incidents SET {', '.join(updates)} WHERE id = ?"
                        cursor.execute(query, params)
                        conn.commit()
                        conn.close()
                        st.success("✅ Incident updated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # DELETE
    elif crud_op == "Delete":
        st.write("### 🗑️ Delete Incident")
        
        incident_id = st.number_input("Incident ID to Delete", min_value=1, step=1, key="delete_incident_id")
        
        if st.button("Delete Incident", use_container_width=True, type="secondary"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
                conn.commit()
                conn.close()
                st.success("✅ Incident deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# TAB 3: ANALYSIS

with tab3:
    st.subheader("Analysis & Insights")
    
    
    st.write("### 📊 Graph Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_chart_type = st.selectbox("Severity Chart Type", ["Bar", "Pie", "Line"], key="severity_chart")
    with col2:
        status_chart_type = st.selectbox("Status Chart Type", ["Pie", "Bar", "Donut"], key="status_chart")
    with col3:
        type_chart_type = st.selectbox("Type Chart Type", ["Bar", "Pie", "Horizontal"], key="type_chart")
    
    st.divider()
    
    try:
        conn = connect_db()
        incidents_df = pd.read_sql_query(
            "SELECT * FROM cyber_incidents",
            conn
        )
        conn.close()
        
        if not incidents_df.empty:
            col1, col2 = st.columns(2)
            
# Chart 1: Incidents by Severity
            with col1:
                st.write("#### 📊 Incidents by Severity")
                try:
                    severity_counts = incidents_df['severity'].value_counts()
                    
                    if severity_chart_type == "Bar":
                        fig1 = px.bar(
                            x=severity_counts.index,
                            y=severity_counts.values,
                            labels={'x': 'Severity', 'y': 'Count'},
                            color=severity_counts.index,
                            color_discrete_map={
                                'critical': '#d62728',
                                'high': '#ff7f0e',
                                'medium': '#ffbb78',
                                'low': '#2ca02c'
                            }
                        )
                        fig1.update_layout(showlegend=False, xaxis_title="Severity", yaxis_title="Count")
                    elif severity_chart_type == "Pie":
                        fig1 = px.pie(
                            values=severity_counts.values,
                            names=severity_counts.index,
                            title="Severity Distribution"
                        )
                    else:  # Line
                        fig1 = px.line(
                            x=severity_counts.index,
                            y=severity_counts.values,
                            markers=True,
                            labels={'x': 'Severity', 'y': 'Count'}
                        )
                        fig1.update_layout(xaxis_title="Severity", yaxis_title="Count")
                    
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not create severity chart: {str(e)}")
            
# Chart 2: Incidents by Status
            with col2:
                st.write("#### 🔄 Incidents by Status")
                try:
                    status_counts = incidents_df['status'].value_counts()
                    
                    if status_chart_type == "Pie":
                        fig2 = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            title="Status Distribution"
                        )
                    elif status_chart_type == "Bar":
                        fig2 = px.bar(
                            x=status_counts.index,
                            y=status_counts.values,
                            labels={'x': 'Status', 'y': 'Count'},
                            color=status_counts.index
                        )
                        fig2.update_layout(showlegend=False)
                    else:  # Donut
                        fig2 = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            hole=0.3,
                            title="Status Distribution"
                        )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not create status chart: {str(e)}")
            
            st.divider()
            
            # Chart 3: Incidents by Type
            st.write("#### 🎯 Incidents by Type")
            try:
                if 'incident_type' in incidents_df.columns:
                    type_counts = incidents_df['incident_type'].value_counts()
                    
                    if type_chart_type == "Bar":
                        fig3 = px.bar(
                            x=type_counts.index,
                            y=type_counts.values,
                            labels={'x': 'Type', 'y': 'Count'},
                            color=type_counts.values,
                            color_continuous_scale="Reds"
                        )
                        fig3.update_layout(xaxis_title="Incident Type", yaxis_title="Count", showlegend=False)
                    elif type_chart_type == "Pie":
                        fig3 = px.pie(
                            values=type_counts.values,
                            names=type_counts.index,
                            title="Type Distribution"
                        )
                    else:  # Horizontal
                        fig3 = px.bar(
                            y=type_counts.index,
                            x=type_counts.values,
                            orientation='h',
                            labels={'x': 'Count', 'y': 'Type'},
                            color=type_counts.values,
                            color_continuous_scale="Reds"
                        )
                        fig3.update_layout(yaxis_title="Incident Type", xaxis_title="Count", showlegend=False)
                    
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("ℹ️ No incident_type column available")
            except Exception as e:
                st.warning(f"⚠️ Could not create type chart: {str(e)}")
        else:
            st.info("ℹ️ No data available for analysis")
    except Exception as e:
        st.error(f"❌ Error loading analysis: {str(e)}")


# TAB 4: AI CHATBOT
with tab4:
    st.subheader("🤖 AI Assistant (Powered by GPT-4 Turbo)")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Ask AI to analyze your security incidents:**")
    with col2:
        if st.button("🧠 Load Context", use_container_width=True):
            try:
                conn = connect_db()
                incidents_df = pd.read_sql_query(
                    "SELECT * FROM cyber_incidents",
                    conn
                )
                conn.close()
                
                critical_count = len(incidents_df[incidents_df['severity'].str.lower() == 'critical'])
                high_count = len(incidents_df[incidents_df['severity'].str.lower() == 'high'])
                
                context = f"""
Current Security Data:
- Total Incidents: {len(incidents_df)}
- Critical: {critical_count}
- High: {high_count}
- Resolved: {len(incidents_df[incidents_df['status'].str.lower() == 'resolved'])}
- Top Threat Types: {', '.join(incidents_df['incident_type'].value_counts().head(3).index.tolist()) if 'incident_type' in incidents_df.columns else 'N/A'}
                """
                
                st.session_state.ai_context_cyber = context
                st.success("✅ Context loaded! Ask any security question below.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Chatbot Interface
    st.write("### 💬 Chat with GPT-4 Turbo")
    
    # Initialize chat history
    if "messages_cyber" not in st.session_state:
        st.session_state.messages_cyber = [
            {"role": "assistant", "message": "👋 Hello! I'm your Cybersecurity AI Assistant powered by GPT-4 Turbo. Click 'Load Context' above first, then ask me anything about threats, incident analysis, or security recommendations!"}
        ]
    
    if "ai_context_cyber" not in st.session_state:
        st.session_state.ai_context_cyber = "No data loaded yet. Click 'Load Context' first."
    
    # Display chat history
    for msg in st.session_state.messages_cyber:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["message"])
        else:
            st.chat_message("assistant").write(msg["message"])
    
    # Chat input
    user_input = st.chat_input("Ask me about security incidents...", key="chat_input_cyber")
    
    if user_input:
        # Add user message
        st.session_state.messages_cyber.append({"role": "user", "message": user_input})
        st.chat_message("user").write(user_input)
        
        # Get AI response from OpenAI
        with st.spinner("🤔 Analyzing with GPT-4..."):
            ai_response = get_ai_response(user_input, st.session_state.ai_context_cyber)
        
        # Add AI response
        st.session_state.messages_cyber.append({"role": "assistant", "message": ai_response})
        st.chat_message("assistant").write(ai_response)
        st.rerun()
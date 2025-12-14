import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")
    st.divider()

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
    .metric-card-critical {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .metric-card-high {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    .metric-card-success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .metric-label {
        font-size: 14px;
        font-weight: 600;
        margin: 0 0 10px 0;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 40px;
        font-weight: 800;
        margin: 0;
    }
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-header h2 {
        margin: 0;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")

def connect_db():
    conn = sqlite3.connect('intelligence_platform.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_incidents():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM cyber_incidents")
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching incidents: {str(e)}")
        return []
    finally:
        conn.close()

def get_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM it_tickets")
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching tickets: {str(e)}")
        return []
    finally:
        conn.close()

tab1, tab2 = st.tabs(["🔐 Incidents", "🎫 Tickets"])

with tab1:
    st.markdown('''<div class="section-header"><h2>🔐 Cyber Incidents Analytics</h2></div>''', unsafe_allow_html=True)
    
    incidents = get_incidents()
    
    if incidents:
        df_incidents = pd.DataFrame([dict(row) for row in incidents])
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(df_incidents)
        critical = len(df_incidents[df_incidents['severity'] == 'critical']) if 'severity' in df_incidents.columns else 0
        high = len(df_incidents[df_incidents['severity'] == 'high']) if 'severity' in df_incidents.columns else 0
        resolved = len(df_incidents[df_incidents['status'] == 'resolved']) if 'status' in df_incidents.columns else 0
        
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <p class="metric-label">📊 Total Incidents</p>
                    <p class="metric-value">{total}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card metric-card-critical">
                    <p class="metric-label">🔴 Critical</p>
                    <p class="metric-value">{critical}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card metric-card-high">
                    <p class="metric-label">🟠 High</p>
                    <p class="metric-value">{high}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="metric-card metric-card-success">
                    <p class="metric-label">✅ Resolved</p>
                    <p class="metric-value">{resolved}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            if st.button("⚙️ Manage Incidents", use_container_width=True, key="manage_incidents"):
                st.session_state.crud_operation_type = "Cyber Incidents"
                st.switch_page("pages/3_CRUD_operations.py")
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'severity' in df_incidents.columns:
                severity_counts = df_incidents['severity'].value_counts()
                fig_severity = px.pie(
                    values=severity_counts.values,
                    names=severity_counts.index,
                    title="📈 Incidents by Severity",
                    color_discrete_sequence=["#FF6B6B", "#FFA07A", "#FFD93D", "#6BCB77"]
                )
                fig_severity.update_layout(
                    font=dict(size=12),
                    title_font_size=16,
                    title_x=0.5,
                    margin=dict(t=50, l=0, r=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            if 'status' in df_incidents.columns:
                status_counts = df_incidents['status'].value_counts()
                fig_status = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title="📊 Incidents by Status",
                    labels={'x': 'Status', 'y': 'Count'},
                    color_discrete_sequence=["#FF6B6B", "#FFD93D", "#6BCB77"]
                )
                fig_status.update_layout(
                    font=dict(size=12),
                    title_font_size=16,
                    title_x=0.5,
                    margin=dict(t=50, l=0, r=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.1)')
                )
                st.plotly_chart(fig_status, use_container_width=True)
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        st.subheader("📋 Incidents Data")
        st.dataframe(df_incidents, use_container_width=True, hide_index=True)
    
    else:
        st.info("No incidents found in database")

with tab2:
    st.markdown('''<div class="section-header"><h2>🎫 IT Tickets Analytics</h2></div>''', unsafe_allow_html=True)
    
    tickets = get_tickets()
    
    if tickets:
        df_tickets = pd.DataFrame([dict(row) for row in tickets])
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(df_tickets)
        open_t = len(df_tickets[df_tickets['status'] == 'open']) if 'status' in df_tickets.columns else 0
        in_progress = len(df_tickets[df_tickets['status'] == 'in_progress']) if 'status' in df_tickets.columns else 0
        closed = len(df_tickets[df_tickets['status'] == 'closed']) if 'status' in df_tickets.columns else 0
        
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <p class="metric-label">📊 Total Tickets</p>
                    <p class="metric-value">{total}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card metric-card-critical">
                    <p class="metric-label">🔴 Open</p>
                    <p class="metric-value">{open_t}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card metric-card-high">
                    <p class="metric-label">⏳ In Progress</p>
                    <p class="metric-value">{in_progress}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="metric-card metric-card-success">
                    <p class="metric-label">✅ Closed</p>
                    <p class="metric-value">{closed}</p>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            if st.button("⚙️ Manage Tickets", use_container_width=True, key="manage_tickets"):
                st.session_state.crud_operation_type = "IT Tickets"
                st.switch_page("pages/3_CRUD_operations.py")
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'priority' in df_tickets.columns:
                priority_counts = df_tickets['priority'].value_counts()
                fig_priority = px.pie(
                    values=priority_counts.values,
                    names=priority_counts.index,
                    title="📈 Tickets by Priority",
                    color_discrete_sequence=["#FF6B6B", "#FFD93D", "#6BCB77"]
                )
                fig_priority.update_layout(
                    font=dict(size=12),
                    title_font_size=16,
                    title_x=0.5,
                    margin=dict(t=50, l=0, r=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_priority, use_container_width=True)
        
        with col2:
            if 'status' in df_tickets.columns:
                status_counts = df_tickets['status'].value_counts()
                fig_status = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title="📊 Tickets by Status",
                    labels={'x': 'Status', 'y': 'Count'},
                    color_discrete_sequence=["#FF6B6B", "#FFD93D", "#6BCB77"]
                )
                fig_status.update_layout(
                    font=dict(size=12),
                    title_font_size=16,
                    title_x=0.5,
                    margin=dict(t=50, l=0, r=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.1)')
                )
                st.plotly_chart(fig_status, use_container_width=True)
        
        st.markdown('<hr style="border: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); margin: 30px 0;">', unsafe_allow_html=True)
        
        st.subheader("📋 Tickets Data")
        st.dataframe(df_tickets, use_container_width=True, hide_index=True)
    
    else:
        st.info("No tickets found in database")
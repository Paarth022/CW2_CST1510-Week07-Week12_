import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import openai


# PAGE CONFIG & AUTHENTICATION
st.set_page_config(page_title="IT Operations", page_icon="🔧", layout="wide")

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
                    "content": f"You are an IT Operations AI Assistant. Help analyze ticket data and provide insights. {context}"
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

st.title("🔧 IT Operations Domain")
st.markdown("---")


# TABS STRUCTURE
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ CRUD Operations", "📈 Analysis", "🤖 AI Chatbot"])


# TAB 1: OVERVIEW
with tab1:
    st.subheader("IT Operations Dashboard Overview")
    
    try:
        conn = connect_db()
        tickets_df = pd.read_sql_query(
            "SELECT * FROM it_tickets",
            conn
        )
        conn.close()
        
        if not tickets_df.empty:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎫 Total Tickets", len(tickets_df))
            with col2:
                open_tickets = len(tickets_df[tickets_df['status'].str.lower() == 'open'])
                st.metric("📖 Open", open_tickets)
            with col3:
                in_progress = len(tickets_df[tickets_df['status'].str.lower() == 'in-progress'])
                st.metric("⏳ In Progress", in_progress)
            with col4:
                closed = len(tickets_df[tickets_df['status'].str.lower() == 'closed'])
                st.metric("✅ Closed", closed)
            
            st.divider()
            st.write("### 📋 All Tickets")
            st.dataframe(tickets_df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No tickets available")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")


# TAB 2: CRUD OPERATIONS
with tab2:
    st.subheader("IT Ticket CRUD Operations")
    
    crud_op = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"],
        key="it_crud_op"
    )
    
    st.divider()
    
    # CREATE
    if crud_op == "Create":
        st.write("### ➕ Create New Ticket")
        
        with st.form("create_ticket_form"):
            title = st.text_input("Ticket Title", placeholder="e.g., Printer not working")
            
            col1, col2 = st.columns(2)
            with col1:
                priority = st.selectbox(
                    "Priority",
                    ["low", "medium", "high", "urgent"]
                )
            with col2:
                status = st.selectbox("Status", ["open", "in-progress", "closed"])
            
            if st.form_submit_button("Create Ticket", use_container_width=True):
                if not title:
                    st.error("❌ Title is required")
                else:
                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO it_tickets 
                            (title, priority, status, created_date)
                            VALUES (?, ?, ?, ?)
                        """, (title, priority, status, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ Ticket created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # READ
    elif crud_op == "Read":
        st.write("### 📖 View All Tickets")
        
        try:
            conn = connect_db()
            tickets = pd.read_sql_query("SELECT * FROM it_tickets", conn)
            conn.close()
            
            if not tickets.empty:
                st.dataframe(tickets, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No tickets found")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # UPDATE
    elif crud_op == "Update":
        st.write("### ✏️ Update Ticket")
        
        ticket_id = st.number_input("Ticket ID to Update", min_value=1, step=1)
        
        with st.form("update_ticket_form"):
            status = st.selectbox("Status", ["open", "in-progress", "closed", "skip"], index=3)
            priority = st.selectbox("Priority", ["low", "medium", "high", "urgent", "skip"], index=4)
            
            if st.form_submit_button("Update Ticket", use_container_width=True):
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    
                    updates = []
                    params = []
                    
                    if status != "skip":
                        updates.append("status = ?")
                        params.append(status)
                    if priority != "skip":
                        updates.append("priority = ?")
                        params.append(priority)
                    
                    if not updates:
                        st.warning("⚠️ No fields to update")
                    else:
                        params.append(ticket_id)
                        query = f"UPDATE it_tickets SET {', '.join(updates)} WHERE id = ?"
                        cursor.execute(query, params)
                        conn.commit()
                        conn.close()
                        st.success("✅ Ticket updated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # DELETE
    elif crud_op == "Delete":
        st.write("### 🗑️ Delete Ticket")
        
        ticket_id = st.number_input("Ticket ID to Delete", min_value=1, step=1, key="delete_ticket_id")
        
        if st.button("Delete Ticket", use_container_width=True, type="secondary"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
                conn.commit()
                conn.close()
                st.success("✅ Ticket deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# TAB 3: ANALYSIS
with tab3:
    st.subheader("Analysis & Insights")
    
    # Graph Type Selector
    st.write("### 📊 Graph Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        status_chart_type = st.selectbox("Status Chart Type", ["Bar", "Pie", "Horizontal"], key="status_chart")
    with col2:
        priority_chart_type = st.selectbox("Priority Chart Type", ["Pie", "Bar", "Donut"], key="priority_chart")
    with col3:
        summary_metric = st.selectbox("Summary View", ["Metrics", "Bar Chart", "Pie Chart"], key="summary_view")
    
    st.divider()
    
    try:
        conn = connect_db()
        tickets_df = pd.read_sql_query(
            "SELECT * FROM it_tickets",
            conn
        )
        conn.close()
        
        if not tickets_df.empty:
            col1, col2 = st.columns(2)
            
            # Chart 1: Tickets by Status
            with col1:
                st.write("#### 📊 Tickets by Status")
                try:
                    status_counts = tickets_df['status'].value_counts()
                    
                    if status_chart_type == "Bar":
                        fig1 = px.bar(
                            x=status_counts.index,
                            y=status_counts.values,
                            labels={'x': 'Status', 'y': 'Count'},
                            color=status_counts.index,
                            color_discrete_map={
                                'open': '#1f77b4',
                                'in-progress': '#ff7f0e',
                                'closed': '#2ca02c'
                            }
                        )
                        fig1.update_layout(xaxis_title="Status", yaxis_title="Count", showlegend=False)
                    elif status_chart_type == "Pie":
                        fig1 = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            title="Status Distribution"
                        )
                    else:  # Horizontal
                        fig1 = px.bar(
                            y=status_counts.index,
                            x=status_counts.values,
                            orientation='h',
                            labels={'x': 'Count', 'y': 'Status'},
                            color=status_counts.index,
                            color_discrete_map={
                                'open': '#1f77b4',
                                'in-progress': '#ff7f0e',
                                'closed': '#2ca02c'
                            }
                        )
                        fig1.update_layout(yaxis_title="Status", xaxis_title="Count", showlegend=False)
                    
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not create status chart: {str(e)}")
            
            # Chart 2: Tickets by Priority
            with col2:
                st.write("#### 🎯 Tickets by Priority")
                try:
                    priority_counts = tickets_df['priority'].value_counts()
                    
                    if priority_chart_type == "Pie":
                        fig2 = px.pie(
                            values=priority_counts.values,
                            names=priority_counts.index,
                            title="Priority Distribution"
                        )
                    elif priority_chart_type == "Bar":
                        fig2 = px.bar(
                            x=priority_counts.index,
                            y=priority_counts.values,
                            labels={'x': 'Priority', 'y': 'Count'},
                            color=priority_counts.values,
                            color_continuous_scale="Oranges"
                        )
                        fig2.update_layout(xaxis_title="Priority", yaxis_title="Count", showlegend=False)
                    else:  
                        fig2 = px.pie(
                            values=priority_counts.values,
                            names=priority_counts.index,
                            hole=0.3,
                            title="Priority Distribution"
                        )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not create priority chart: {str(e)}")
            
            st.divider()
            
            # Chart 3: Ticket Summary
            st.write("#### 📈 Ticket Summary")
            try:
                summary_data = {
                    'Total Tickets': len(tickets_df),
                    'Open': len(tickets_df[tickets_df['status'].str.lower() == 'open']),
                    'Closed': len(tickets_df[tickets_df['status'].str.lower() == 'closed']),
                }
                
                if summary_metric == "Metrics":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🎫 Total Tickets", summary_data['Total Tickets'])
                    with col2:
                        st.metric("📖 Open", summary_data['Open'])
                    with col3:
                        st.metric("✅ Closed", summary_data['Closed'])
                elif summary_metric == "Bar Chart":
                    summary_df = pd.DataFrame({
                        'Status': ['Total', 'Open', 'Closed'],
                        'Count': [summary_data['Total Tickets'], summary_data['Open'], summary_data['Closed']]
                    })
                    fig3 = px.bar(
                        summary_df,
                        x='Status',
                        y='Count',
                        color='Status',
                        title="Ticket Summary",
                        labels={'Count': 'Number of Tickets'}
                    )
                    fig3.update_layout(showlegend=False)
                    st.plotly_chart(fig3, use_container_width=True)
                else:  # Pie Chart
                    summary_df = pd.DataFrame({
                        'Status': ['Open', 'Closed'],
                        'Count': [summary_data['Open'], summary_data['Closed']]
                    })
                    fig3 = px.pie(
                        summary_df,
                        values='Count',
                        names='Status',
                        title="Ticket Status Distribution"
                    )
                    st.plotly_chart(fig3, use_container_width=True)
            except Exception as e:
                st.warning(f"⚠️ Could not create summary: {str(e)}")
        else:
            st.info("ℹ️ No data available for analysis")
    except Exception as e:
        st.error(f"❌ Error loading analysis: {str(e)}")


# TAB 4: AI CHATBOT
with tab4:
    st.subheader("🤖 AI Assistant (Powered by GPT-4 Turbo)")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Ask AI to analyze your IT operations:**")
    with col2:
        if st.button("🧠 Load Context", use_container_width=True):
            try:
                conn = connect_db()
                tickets_df = pd.read_sql_query(
                    "SELECT * FROM it_tickets",
                    conn
                )
                conn.close()
                
                open_count = len(tickets_df[tickets_df['status'].str.lower() == 'open'])
                closed_count = len(tickets_df[tickets_df['status'].str.lower() == 'closed'])
                in_progress = len(tickets_df[tickets_df['status'].str.lower() == 'in-progress'])
                
                context = f"""
Current IT Operations Data:
- Total Tickets: {len(tickets_df)}
- Open: {open_count}
- In Progress: {in_progress}
- Closed: {closed_count}
- Priority Breakdown: {dict(tickets_df['priority'].value_counts())}
                """
                
                st.session_state.ai_context = context
                st.success("✅ Context loaded! Ask any question below.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
# Chatbot Interface
    st.write("### 💬 Chat with GPT-4 Turbo")
    
#chat history
    if "messages_itops" not in st.session_state:
        st.session_state.messages_itops = [
            {"role": "assistant", "message": "👋 Hello! I'm your IT Operations AI Assistant powered by GPT-4 Turbo. Click 'Load Context' above first, then ask me anything about tickets, priorities, or operational insights!"}
        ]
    
    if "ai_context" not in st.session_state:
        st.session_state.ai_context = "No data loaded yet. Click 'Load Context' first."
    
    for msg in st.session_state.messages_itops:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["message"])
        else:
            st.chat_message("assistant").write(msg["message"])
    
    # Chat input
    user_input = st.chat_input("Ask me about your IT operations...", key="chat_input_itops")
    
    if user_input:
# Add user message
        st.session_state.messages_itops.append({"role": "user", "message": user_input})
        st.chat_message("user").write(user_input)
        
 # Get AI response from OpenAI
        with st.spinner("🤔 Analyzing with GPT-4..."):
            ai_response = get_ai_response(user_input, st.session_state.ai_context)
        
# Add AI response
        st.session_state.messages_itops.append({"role": "assistant", "message": ai_response})
        st.chat_message("assistant").write(ai_response)
        st.rerun()
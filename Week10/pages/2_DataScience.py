import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import openai


# PAGE CONFIG & AUTHENTICATION
st.set_page_config(page_title="Data Science", page_icon="📊", layout="wide")

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
                    "content": f"You are a Data Science AI Assistant. Help analyze datasets and provide data insights. {context}"
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

st.title("📊 Data Science Domain")
st.markdown("---")


# TABS STRUCTURE
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ CRUD Operations", "📈 Analysis", "🤖 AI Chatbot"])


# TAB 1: OVERVIEW
with tab1:
    st.subheader("Data Science Dashboard Overview")
    
    try:
        conn = connect_db()
        datasets_df = pd.read_sql_query(
            "SELECT * FROM datasets_metadata",
            conn
        )
        conn.close()
        
        if not datasets_df.empty:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Datasets", len(datasets_df))
            with col2:
                categories = datasets_df['category'].nunique() if 'category' in datasets_df.columns else 0
                st.metric("📁 Categories", categories)
            with col3:
                sources = datasets_df['source'].nunique() if 'source' in datasets_df.columns else 0
                st.metric("📍 Sources", sources)
            with col4:
                total_size = datasets_df['size'].sum() if 'size' in datasets_df.columns else 0
                st.metric("💾 Total Size (MB)", int(total_size / 1024) if total_size > 0 else 0)
            
            st.divider()
            st.write("### 📋 All Datasets")
            st.dataframe(datasets_df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No datasets available")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")


# TAB 2: CRUD OPERATIONS
with tab2:
    st.subheader("Dataset CRUD Operations")
    
    crud_op = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"],
        key="data_crud_op"
    )
    
    st.divider()
    
    # CREATE
    if crud_op == "Create":
        st.write("### ➕ Create New Dataset")
        
        with st.form("create_dataset_form"):
            name = st.text_input("Dataset Name", placeholder="e.g., Sales Data 2024")
            
            col1, col2 = st.columns(2)
            with col1:
                source = st.text_input("Source", placeholder="e.g., Cloud Storage")
            with col2:
                category = st.selectbox(
                    "Category",
                    ["Analytics", "Machine Learning", "Visualization", "Research", "Security", "Testing"]
                )
            
            size = st.number_input("Size (bytes)", min_value=0, step=1000, placeholder="e.g., 50000")
            
            if st.form_submit_button("Create Dataset", use_container_width=True):
                if not all([name, source]):
                    st.error("❌ All fields are required")
                else:
                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO datasets_metadata 
                            (name, source, category, size)
                            VALUES (?, ?, ?, ?)
                        """, (name, source, category, size))
                        conn.commit()
                        conn.close()
                        st.success("✅ Dataset created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # READ
    elif crud_op == "Read":
        st.write("### 📖 View All Datasets")
        
        try:
            conn = connect_db()
            datasets = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
            conn.close()
            
            if not datasets.empty:
                st.dataframe(datasets, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No datasets found")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # UPDATE
    elif crud_op == "Update":
        st.write("### ✏️ Update Dataset")
        
        dataset_id = st.number_input("Dataset ID to Update", min_value=1, step=1)
        
        with st.form("update_dataset_form"):
            name = st.text_input("Name (leave empty to skip)")
            category = st.selectbox("Category (skip)", ["Analytics", "Machine Learning", "Visualization", "Research", "Security", "Testing", "skip"], index=6)
            
            if st.form_submit_button("Update Dataset", use_container_width=True):
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    
                    updates = []
                    params = []
                    
                    if name:
                        updates.append("name = ?")
                        params.append(name)
                    if category != "skip":
                        updates.append("category = ?")
                        params.append(category)
                    
                    if not updates:
                        st.warning("⚠️ No fields to update")
                    else:
                        params.append(dataset_id)
                        query = f"UPDATE datasets_metadata SET {', '.join(updates)} WHERE id = ?"
                        cursor.execute(query, params)
                        conn.commit()
                        conn.close()
                        st.success("✅ Dataset updated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # DELETE
    elif crud_op == "Delete":
        st.write("### 🗑️ Delete Dataset")
        
        dataset_id = st.number_input("Dataset ID to Delete", min_value=1, step=1, key="delete_dataset_id")
        
        if st.button("Delete Dataset", use_container_width=True, type="secondary"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
                conn.commit()
                conn.close()
                st.success("✅ Dataset deleted successfully!")
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
        category_chart_type = st.selectbox("Category Chart Type", ["Bar", "Pie", "Horizontal"], key="category_chart")
    with col2:
        source_chart_type = st.selectbox("Source Chart Type", ["Pie", "Bar", "Donut"], key="source_chart")
    with col3:
        st.write("")
        st.write("")
    
    st.divider()
    
    try:
        conn = connect_db()
        datasets_df = pd.read_sql_query(
            "SELECT * FROM datasets_metadata",
            conn
        )
        conn.close()
        
        if not datasets_df.empty:
            col1, col2 = st.columns(2)
            
            # Chart 1: Datasets by Category
            with col1:
                st.write("#### 📊 Datasets by Category")
                try:
                    if 'category' in datasets_df.columns:
                        category_counts = datasets_df['category'].value_counts()
                        
                        if category_chart_type == "Bar":
                            fig1 = px.bar(
                                x=category_counts.index,
                                y=category_counts.values,
                                labels={'x': 'Category', 'y': 'Count'},
                                color=category_counts.values,
                                color_continuous_scale="Blues"
                            )
                            fig1.update_layout(xaxis_title="Category", yaxis_title="Count", showlegend=False)
                        elif category_chart_type == "Pie":
                            fig1 = px.pie(
                                values=category_counts.values,
                                names=category_counts.index,
                                title="Category Distribution"
                            )
                        else:  # Horizontal
                            fig1 = px.bar(
                                y=category_counts.index,
                                x=category_counts.values,
                                orientation='h',
                                labels={'x': 'Count', 'y': 'Category'},
                                color=category_counts.values,
                                color_continuous_scale="Blues"
                            )
                            fig1.update_layout(yaxis_title="Category", xaxis_title="Count", showlegend=False)
                        
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        st.info("ℹ️ No category column available")
                except Exception as e:
                    st.warning(f"⚠️ Could not create category chart: {str(e)}")
            
            # Chart 2: Datasets by Source
            with col2:
                st.write("#### 📍 Datasets by Source")
                try:
                    if 'source' in datasets_df.columns:
                        source_counts = datasets_df['source'].value_counts()
                        
                        if source_chart_type == "Pie":
                            fig2 = px.pie(
                                values=source_counts.values,
                                names=source_counts.index,
                                title="Source Distribution"
                            )
                        elif source_chart_type == "Bar":
                            fig2 = px.bar(
                                x=source_counts.index,
                                y=source_counts.values,
                                labels={'x': 'Source', 'y': 'Count'},
                                color=source_counts.values,
                                color_continuous_scale="Greens"
                            )
                            fig2.update_layout(xaxis_title="Source", yaxis_title="Count", showlegend=False)
                        else:  # Donut
                            fig2 = px.pie(
                                values=source_counts.values,
                                names=source_counts.index,
                                hole=0.3,
                                title="Source Distribution"
                            )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("ℹ️ No source column available")
                except Exception as e:
                    st.warning(f"⚠️ Could not create source chart: {str(e)}")
            
            st.divider()
            
            # Chart 3: Dataset Summary Statistics
            st.write("#### 📈 Dataset Summary Statistics")
            try:
                summary_data = {
                    'Total Datasets': len(datasets_df),
                    'Unique Sources': datasets_df['source'].nunique() if 'source' in datasets_df.columns else 0,
                    'Unique Categories': datasets_df['category'].nunique() if 'category' in datasets_df.columns else 0,
                }
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Datasets", summary_data['Total Datasets'])
                with col2:
                    st.metric("📍 Sources", summary_data['Unique Sources'])
                with col3:
                    st.metric("📁 Categories", summary_data['Unique Categories'])
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
        st.write("**Ask AI to analyze your data:**")
    with col2:
        if st.button("🧠 Load Context", use_container_width=True):
            try:
                conn = connect_db()
                datasets_df = pd.read_sql_query(
                    "SELECT * FROM datasets_metadata",
                    conn
                )
                conn.close()
                
                context = f"""
Current Data Science Metrics:
- Total Datasets: {len(datasets_df)}
- Categories: {datasets_df['category'].nunique() if 'category' in datasets_df.columns else 0}
- Sources: {datasets_df['source'].nunique() if 'source' in datasets_df.columns else 0}
- Top Categories: {', '.join(datasets_df['category'].value_counts().head(3).index.tolist()) if 'category' in datasets_df.columns else 'N/A'}
                """
                
                st.session_state.ai_context_ds = context
                st.success("✅ Context loaded! Ask any data science question below.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Chatbot Interface
    st.write("### 💬 Chat with GPT-4 Turbo")
    
    # Initialize chat history
    if "messages_ds" not in st.session_state:
        st.session_state.messages_ds = [
            {"role": "assistant", "message": "👋 Hello! I'm your Data Science AI Assistant powered by GPT-4 Turbo. Click 'Load Context' above first, then ask me about datasets, analytics, or data insights!"}
        ]
    
    if "ai_context_ds" not in st.session_state:
        st.session_state.ai_context_ds = "No data loaded yet. Click 'Load Context' first."
    
    # Display chat history
    for msg in st.session_state.messages_ds:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["message"])
        else:
            st.chat_message("assistant").write(msg["message"])
    
    # Chat input
    user_input = st.chat_input("Ask me about your data...", key="chat_input_ds")
    
    if user_input:
        # Add user message
        st.session_state.messages_ds.append({"role": "user", "message": user_input})
        st.chat_message("user").write(user_input)
        
        # Get AI response from OpenAI
        with st.spinner("🤔 Analyzing with GPT-4..."):
            ai_response = get_ai_response(user_input, st.session_state.ai_context_ds)
        
        # Add AI response
        st.session_state.messages_ds.append({"role": "assistant", "message": ai_response})
        st.chat_message("assistant").write(ai_response)
        st.rerun()
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="CRUD Operations", page_icon="⚙️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")
    st.divider()

st.title("⚙️ CRUD Operations Management")

# ============================================
# DATABASE CONNECTION
# ============================================

def connect_db():
    conn = sqlite3.connect('intelligence_platform.db')
    conn.row_factory = sqlite3.Row
    return conn

# ============================================
# CYBER INCIDENTS CRUD
# ============================================

def create_incident(title, description, severity, status, source_ip, target_ip):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cyber_incidents (title, description, severity, status, source_ip, target_ip, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, severity, status, source_ip, target_ip, datetime.now()))
        conn.commit()
        return True, "Incident created successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def read_incidents(limit=100):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM cyber_incidents LIMIT ?", (limit,))
        return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        conn.close()

def update_incident(incident_id, title=None, description=None, severity=None, status=None, source_ip=None, target_ip=None):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        
        if title: updates.append("title = ?"); params.append(title)
        if description: updates.append("description = ?"); params.append(description)
        if severity: updates.append("severity = ?"); params.append(severity)
        if status: updates.append("status = ?"); params.append(status)
        if source_ip: updates.append("source_ip = ?"); params.append(source_ip)
        if target_ip: updates.append("target_ip = ?"); params.append(target_ip)
        
        if not updates:
            return False, "No fields to update"
        
        params.append(incident_id)
        query = f"UPDATE cyber_incidents SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return True, "Incident updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_incident(incident_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
        conn.commit()
        return True, "Incident deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ============================================
# IT TICKETS CRUD
# ============================================

def create_ticket(title, description, status, priority, assigned_to, category):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO it_tickets (title, description, status, priority, assigned_to, category, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, assigned_to, category, datetime.now()))
        conn.commit()
        return True, "Ticket created successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def read_tickets(limit=100):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM it_tickets LIMIT ?", (limit,))
        return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        conn.close()

def update_ticket(ticket_id, title=None, description=None, status=None, priority=None, assigned_to=None, category=None):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        
        if title: updates.append("title = ?"); params.append(title)
        if description: updates.append("description = ?"); params.append(description)
        if status: updates.append("status = ?"); params.append(status)
        if priority: updates.append("priority = ?"); params.append(priority)
        if assigned_to: updates.append("assigned_to = ?"); params.append(assigned_to)
        if category: updates.append("category = ?"); params.append(category)
        
        if not updates:
            return False, "No fields to update"
        
        params.append(ticket_id)
        query = f"UPDATE it_tickets SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return True, "Ticket updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_ticket(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        return True, "Ticket deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ============================================
# DATASETS CRUD
# ============================================

def create_dataset(name, description, category, owner, format, file_path):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO datasets_metadata (name, description, category, owner, format, file_path, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, description, category, owner, format, file_path, datetime.now()))
        conn.commit()
        return True, "Dataset created successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def read_datasets(limit=100):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM datasets_metadata LIMIT ?", (limit,))
        return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        conn.close()

def update_dataset(dataset_id, name=None, description=None, category=None, owner=None, format=None, file_path=None):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        
        if name: updates.append("name = ?"); params.append(name)
        if description: updates.append("description = ?"); params.append(description)
        if category: updates.append("category = ?"); params.append(category)
        if owner: updates.append("owner = ?"); params.append(owner)
        if format: updates.append("format = ?"); params.append(format)
        if file_path: updates.append("file_path = ?"); params.append(file_path)
        
        if not updates:
            return False, "No fields to update"
        
        params.append(dataset_id)
        query = f"UPDATE datasets_metadata SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return True, "Dataset updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_dataset(dataset_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
        conn.commit()
        return True, "Dataset deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ============================================
# UI - CRUD TYPE SELECTOR
# ============================================

crud_type = st.selectbox(
    "Select Operation Type",
    ["Cyber Incidents", "IT Tickets", "Datasets"],
    key="crud_type"
)

st.divider()

# ============================================
# CYBER INCIDENTS UI
# ============================================

if crud_type == "Cyber Incidents":
    st.subheader("🔐 Cyber Incidents Management")
    
    operation = st.radio("Select Operation", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        st.write("### Create New Incident")
        with st.form("create_incident_form"):
            title = st.text_input("Title", placeholder="Incident title")
            description = st.text_area("Description", placeholder="Incident description")
            severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
            status = st.selectbox("Status", ["open", "in_progress", "resolved"])
            source_ip = st.text_input("Source IP", placeholder="192.168.1.100")
            target_ip = st.text_input("Target IP", placeholder="10.0.0.1")
            
            if st.form_submit_button("Create Incident", use_container_width=True):
                if not all([title, description, source_ip, target_ip]):
                    st.error("All fields are required")
                else:
                    success, msg = create_incident(title, description, severity, status, source_ip, target_ip)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    elif operation == "Read":
        st.write("### View All Incidents")
        incidents = read_incidents(limit=100)
        if incidents:
            df = pd.DataFrame([dict(row) for row in incidents])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No incidents found")
    
    elif operation == "Update":
        st.write("### Update Incident")
        incident_id = st.number_input("Incident ID", min_value=1)
        
        with st.form("update_incident_form"):
            title = st.text_input("Title (leave empty to skip)")
            description = st.text_area("Description (leave empty to skip)")
            severity = st.selectbox("Severity", ["low", "medium", "high", "critical", "skip"], index=4)
            status = st.selectbox("Status", ["open", "in_progress", "resolved", "skip"], index=3)
            source_ip = st.text_input("Source IP (leave empty to skip)")
            target_ip = st.text_input("Target IP (leave empty to skip)")
            
            if st.form_submit_button("Update Incident", use_container_width=True):
                success, msg = update_incident(
                    incident_id,
                    title if title else None,
                    description if description else None,
                    severity if severity != "skip" else None,
                    status if status != "skip" else None,
                    source_ip if source_ip else None,
                    target_ip if target_ip else None
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    elif operation == "Delete":
        st.write("### Delete Incident")
        incident_id = st.number_input("Incident ID to Delete", min_value=1)
        
        if st.button("Delete Incident", use_container_width=True, type="secondary"):
            success, msg = delete_incident(incident_id)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

# ============================================
# IT TICKETS UI
# ============================================

elif crud_type == "IT Tickets":
    st.subheader("🎫 IT Tickets Management")
    
    operation = st.radio("Select Operation", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        st.write("### Create New Ticket")
        with st.form("create_ticket_form"):
            title = st.text_input("Title", placeholder="Ticket title")
            description = st.text_area("Description", placeholder="Ticket description")
            status = st.selectbox("Status", ["open", "in_progress", "closed"])
            priority = st.selectbox("Priority", ["low", "medium", "high"])
            assigned_to = st.text_input("Assigned To", placeholder="Team member name")
            category = st.text_input("Category", placeholder="e.g., Hardware, Software")
            
            if st.form_submit_button("Create Ticket", use_container_width=True):
                if not all([title, description, assigned_to, category]):
                    st.error("All fields are required")
                else:
                    success, msg = create_ticket(title, description, status, priority, assigned_to, category)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    elif operation == "Read":
        st.write("### View All Tickets")
        tickets = read_tickets(limit=100)
        if tickets:
            df = pd.DataFrame([dict(row) for row in tickets])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No tickets found")
    
    elif operation == "Update":
        st.write("### Update Ticket")
        ticket_id = st.number_input("Ticket ID", min_value=1)
        
        with st.form("update_ticket_form"):
            title = st.text_input("Title (leave empty to skip)")
            description = st.text_area("Description (leave empty to skip)")
            status = st.selectbox("Status", ["open", "in_progress", "closed", "skip"], index=3)
            priority = st.selectbox("Priority", ["low", "medium", "high", "skip"], index=3)
            assigned_to = st.text_input("Assigned To (leave empty to skip)")
            category = st.text_input("Category (leave empty to skip)")
            
            if st.form_submit_button("Update Ticket", use_container_width=True):
                success, msg = update_ticket(
                    ticket_id,
                    title if title else None,
                    description if description else None,
                    status if status != "skip" else None,
                    priority if priority != "skip" else None,
                    assigned_to if assigned_to else None,
                    category if category else None
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    elif operation == "Delete":
        st.write("### Delete Ticket")
        ticket_id = st.number_input("Ticket ID to Delete", min_value=1)
        
        if st.button("Delete Ticket", use_container_width=True, type="secondary"):
            success, msg = delete_ticket(ticket_id)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

# ============================================
# DATASETS UI
# ============================================

elif crud_type == "Datasets":
    st.subheader("📊 Datasets Management")
    
    operation = st.radio("Select Operation", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        st.write("### Create New Dataset")
        with st.form("create_dataset_form"):
            name = st.text_input("Name", placeholder="Dataset name")
            description = st.text_area("Description", placeholder="Dataset description")
            category = st.text_input("Category", placeholder="e.g., Security, Sales")
            owner = st.text_input("Owner", placeholder="Dataset owner")
            format = st.selectbox("Format", ["CSV", "JSON", "XML", "Parquet", "Excel"])
            file_path = st.text_input("File Path", placeholder="/path/to/file")
            
            if st.form_submit_button("Create Dataset", use_container_width=True):
                if not all([name, description, category, owner, file_path]):
                    st.error("All fields are required")
                else:
                    success, msg = create_dataset(name, description, category, owner, format, file_path)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    elif operation == "Read":
        st.write("### View All Datasets")
        datasets = read_datasets(limit=100)
        if datasets:
            df = pd.DataFrame([dict(row) for row in datasets])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No datasets found")
    
    elif operation == "Update":
        st.write("### Update Dataset")
        dataset_id = st.number_input("Dataset ID", min_value=1)
        
        with st.form("update_dataset_form"):
            name = st.text_input("Name (leave empty to skip)")
            description = st.text_area("Description (leave empty to skip)")
            category = st.text_input("Category (leave empty to skip)")
            owner = st.text_input("Owner (leave empty to skip)")
            format = st.selectbox("Format", ["CSV", "JSON", "XML", "Parquet", "Excel", "skip"], index=5)
            file_path = st.text_input("File Path (leave empty to skip)")
            
            if st.form_submit_button("Update Dataset", use_container_width=True):
                success, msg = update_dataset(
                    dataset_id,
                    name if name else None,
                    description if description else None,
                    category if category else None,
                    owner if owner else None,
                    format if format != "skip" else None,
                    file_path if file_path else None
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    elif operation == "Delete":
        st.write("### Delete Dataset")
        dataset_id = st.number_input("Dataset ID to Delete", min_value=1)
        
        if st.button("Delete Dataset", use_container_width=True, type="secondary"):
            success, msg = delete_dataset(dataset_id)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
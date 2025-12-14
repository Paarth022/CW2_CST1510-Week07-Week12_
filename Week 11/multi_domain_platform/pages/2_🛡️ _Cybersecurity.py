import streamlit as st
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Cybersecurity", page_icon="🛡️")

st.title("🛡️ Cybersecurity Management")
st.markdown("---")

# Check if user is logged in
if st.session_state.get("current_user") is None:
    st.error("❌ Please log in first!")
    st.stop()

# Initialize database
db = DatabaseManager("database/platform.db")
db.connect()

tab1, tab2 = st.tabs(["View Incidents", "Create Incident"])

with tab1:
    st.subheader("Security Incidents")
    
    try:
        rows = db.fetch_all(
            "SELECT id, incident_type, severity, status, description FROM security_incidents ORDER BY id DESC"
        )
        
        if rows:
            incidents = [
                SecurityIncident(row[0], row[1], row[2], row[3], row[4])
                for row in rows
            ]
            
            for incident in incidents:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{incident.get_incident_type()}**")
                        st.write(f"Description: {incident.get_description()}")
                    
                    with col2:
                        severity_color = {
                            "low": "🟢",
                            "medium": "🟡",
                            "high": "🔴",
                            "critical": "⚫"
                        }
                        color = severity_color.get(incident.get_severity().lower(), "⚪")
                        st.write(f"{color} **{incident.get_severity().upper()}**")
                        st.write(f"Level: {incident.get_severity_level()}/4")
                    
                    with col3:
                        status_badge = {
                            "Open": "🔴",
                            "In Progress": "🟡",
                            "Resolved": "🟢"
                        }
                        badge = status_badge.get(incident.get_status(), "⚪")
                        st.write(f"{badge} {incident.get_status()}")
                        
                        if st.button(f"Update Incident {incident.get_id()}", key=f"update_{incident.get_id()}"):
                            new_status = st.selectbox(
                                f"New status for Incident {incident.get_id()}",
                                ["Open", "In Progress", "Resolved"],
                                key=f"status_{incident.get_id()}"
                            )
                            if st.button(f"Confirm Update {incident.get_id()}", key=f"confirm_{incident.get_id()}"):
                                db.execute_query(
                                    "UPDATE security_incidents SET status = ? WHERE id = ?",
                                    (new_status, incident.get_id())
                                )
                                st.success(f"✅ Incident {incident.get_id()} updated!")
                                st.rerun()
        else:
            st.info("📭 No security incidents found.")
    
    except Exception as e:
        st.error(f"❌ Error loading incidents: {str(e)}")

with tab2:
    st.subheader("Report New Incident")
    
    incident_type = st.selectbox(
        "Incident Type",
        ["Malware Detection", "SQL Injection", "DDoS Attack", "Unauthorized Access", "Data Breach", "Other"]
    )
    
    severity = st.selectbox(
        "Severity Level",
        ["low", "medium", "high", "critical"]
    )
    
    description = st.text_area("Description", height=100)
    
    if st.button("Report Incident"):
        if not description:
            st.error("❌ Please enter a description")
        else:
            try:
                db.execute_query(
                    "INSERT INTO security_incidents (incident_type, severity, status, description) VALUES (?, ?, ?, ?)",
                    (incident_type, severity, "Open", description)
                )
                st.success("✅ Incident reported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error reporting incident: {str(e)}")

db.close()
import streamlit as st
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket

st.set_page_config(page_title="IT Operations", page_icon="💻")

st.title("💻 IT Operations & Support")
st.markdown("---")

# Check if user is logged in
if st.session_state.get("current_user") is None:
    st.error("❌ Please log in first!")
    st.stop()

# Initialize database
db = DatabaseManager("database/platform.db")
db.connect()

tab1, tab2 = st.tabs(["View Tickets", "Create Ticket"])

with tab1:
    st.subheader("Support Tickets")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.multiselect(
            "Filter by Status",
            ["Open", "In Progress", "Closed"],
            default=["Open", "In Progress"]
        )
    with col2:
        filter_priority = st.multiselect(
            "Filter by Priority",
            ["low", "medium", "high", "critical"],
            default=["high", "critical"]
        )
    
    try:
        rows = db.fetch_all(
            "SELECT id, title, priority, status, assigned_to FROM it_tickets ORDER BY id DESC"
        )
        
        if rows:
            tickets = [
                ITTicket(row[0], row[1], row[2], row[3], row[4])
                for row in rows
            ]
            
            # Apply filters
            filtered_tickets = [
                t for t in tickets
                if t.get_status() in filter_status and t.get_priority() in filter_priority
            ]
            
            if filtered_tickets:
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Tickets", len(filtered_tickets))
                with col2:
                    open_count = sum(1 for t in filtered_tickets if t.get_status() == "Open")
                    st.metric("Open", open_count)
                with col3:
                    in_progress = sum(1 for t in filtered_tickets if t.get_status() == "In Progress")
                    st.metric("In Progress", in_progress)
                with col4:
                    closed_count = sum(1 for t in filtered_tickets if t.get_status() == "Closed")
                    st.metric("Closed", closed_count)
                
                st.markdown("---")
                
                for ticket in filtered_tickets:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{ticket.get_title()}**")
                            st.caption(f"Assigned to: {ticket.get_assigned_to()}")
                        
                        with col2:
                            priority_color = {
                                "low": "🟢",
                                "medium": "🟡",
                                "high": "🔴",
                                "critical": "⚫"
                            }
                            color = priority_color.get(ticket.get_priority(), "⚪")
                            st.write(f"{color} **{ticket.get_priority().upper()}**")
                        
                        with col3:
                            status_emoji = {
                                "Open": "🔴",
                                "In Progress": "🟡",
                                "Closed": "🟢"
                            }
                            emoji = status_emoji.get(ticket.get_status(), "⚪")
                            st.write(f"{emoji} {ticket.get_status()}")
                            
                            if st.button(f"Update Ticket {ticket.get_id()}", key=f"update_{ticket.get_id()}"):
                                new_status = st.selectbox(
                                    f"New status for Ticket {ticket.get_id()}",
                                    ["Open", "In Progress", "Closed"],
                                    key=f"status_{ticket.get_id()}"
                                )
                                if st.button(f"Confirm Update {ticket.get_id()}", key=f"confirm_{ticket.get_id()}"):
                                    db.execute_query(
                                        "UPDATE it_tickets SET status = ? WHERE id = ?",
                                        (new_status, ticket.get_id())
                                    )
                                    st.success(f"✅ Ticket {ticket.get_id()} updated!")
                                    st.rerun()
            else:
                st.info("📭 No tickets matching the filters.")
        else:
            st.info("📭 No support tickets found.")
    
    except Exception as e:
        st.error(f"❌ Error loading tickets: {str(e)}")

with tab2:
    st.subheader("Create New Ticket")
    
    title = st.text_input("Ticket Title")
    description = st.text_area("Description", height=100)
    priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
    assigned_to = st.text_input("Assign to (staff name)")
    
    if st.button("Create Ticket"):
        if not title or not description:
            st.error("❌ Please fill in all fields")
        else:
            try:
                db.execute_query(
                    "INSERT INTO it_tickets (title, priority, status, assigned_to) VALUES (?, ?, ?, ?)",
                    (title, priority, "Open", assigned_to)
                )
                st.success("✅ Ticket created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating ticket: {str(e)}")

db.close()
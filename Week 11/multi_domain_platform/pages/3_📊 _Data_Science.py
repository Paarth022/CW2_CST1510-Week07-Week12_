import streamlit as st
from services.database_manager import DatabaseManager
from models.dataset import Dataset

st.set_page_config(page_title="Data Science", page_icon="📊")

st.title("📊 Data Science & Analytics")
st.markdown("---")

# Check if user is logged in
if st.session_state.get("current_user") is None:
    st.error("❌ Please log in first!")
    st.stop()

# Initialize database
db = DatabaseManager("database/platform.db")
db.connect()

tab1, tab2 = st.tabs(["View Datasets", "Upload Dataset"])

with tab1:
    st.subheader("Available Datasets")
    
    try:
        rows = db.fetch_all(
            "SELECT id, name, size_bytes, rows, source FROM datasets ORDER BY id DESC"
        )
        
        if rows:
            datasets = [
                Dataset(row[0], row[1], row[2], row[3], row[4])
                for row in rows
            ]
            
            # Display as metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Datasets", len(datasets))
            with col2:
                total_mb = sum(d.calculate_size_mb() for d in datasets)
                st.metric("Total Size", f"{total_mb:.2f} MB")
            with col3:
                total_rows = sum(d.get_rows() for d in datasets)
                st.metric("Total Rows", f"{total_rows:,}")
            with col4:
                avg_rows = total_rows // len(datasets) if datasets else 0
                st.metric("Avg Rows", f"{avg_rows:,}")
            
            st.markdown("---")
            
            # Display datasets
            for dataset in datasets:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{dataset.get_name()}**")
                        st.caption(f"Source: {dataset.get_source()}")
                    
                    with col2:
                        st.metric("Size", f"{dataset.calculate_size_mb():.2f} MB")
                        st.metric("Rows", f"{dataset.get_rows():,}")
                    
                    with col3:
                        st.metric("ID", dataset.get_id())
                        if st.button(f"Download {dataset.get_id()}", key=f"download_{dataset.get_id()}"):
                            st.info(f"📥 Downloading {dataset.get_name()}...")
                            st.success("✅ Download started!")
        else:
            st.info("📭 No datasets found.")
    
    except Exception as e:
        st.error(f"❌ Error loading datasets: {str(e)}")

with tab2:
    st.subheader("Upload New Dataset")
    
    dataset_name = st.text_input("Dataset Name")
    dataset_source = st.selectbox(
        "Data Source",
        ["MySQL Database", "Kafka Stream", "CSV Upload", "API Endpoint", "Other"]
    )
    
    # Simulated file upload
    size_mb = st.number_input("Size (MB)", min_value=0.1, value=1.0)
    num_rows = st.number_input("Number of Rows", min_value=1, value=1000, step=100)
    
    if st.button("Register Dataset"):
        if not dataset_name:
            st.error("❌ Please enter a dataset name")
        else:
            try:
                size_bytes = int(size_mb * 1024 * 1024)
                db.execute_query(
                    "INSERT INTO datasets (name, size_bytes, rows, source) VALUES (?, ?, ?, ?)",
                    (dataset_name, size_bytes, int(num_rows), dataset_source)
                )
                st.success(f"✅ Dataset '{dataset_name}' registered successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error registering dataset: {str(e)}")

db.close()
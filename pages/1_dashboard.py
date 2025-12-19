import streamlit as st
import pandas as pd
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.metadatas import get_all_datasets_metadata
from app_model.db import get_connection

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Authentication Check
# -----------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("You are logged in!")

# -----------------------------
# Load Data
# -----------------------------
conn = get_connection()
data = get_all_cyber_incidents(conn)

st.title("Cybersecurity Incident Response Dashboard")

# -----------------------------
# Data Preparation
# -----------------------------
data['timestamp'] = pd.to_datetime(data['timestamp'])

if 'resolved_at' in data.columns:
    data['resolved_at'] = pd.to_datetime(data['resolved_at'])
    data['resolution_time_hrs'] = (
        (data['resolved_at'] - data['timestamp'])
        .dt.total_seconds() / 3600
    )
else:
    data['resolution_time_hrs'] = None

# -----------------------------
# Sidebar Filters
# -----------------------------
with st.sidebar:
    st.header("Filters")
    severity_ = st.selectbox(
        'Severity Level',
        sorted(data['severity'].unique())
    )

filtered_data = data[data['severity'] == severity_]

# -----------------------------
# SECTION 1: Threat Trend Analysis (Phishing Spike)
# -----------------------------
st.subheader("🚨 Threat Trend Analysis – Phishing Spike")

phishing_data = filtered_data[
    filtered_data['category'].str.lower() == 'phishing'
]

if not phishing_data.empty:
    phishing_trend = (
        phishing_data
        .set_index('timestamp')
        .resample('D')
        .size()
        .rename("Phishing Incidents")
    )

    st.line_chart(phishing_trend)

    recent_avg = phishing_trend.tail(7).mean()
    previous_avg = phishing_trend.shift(7).tail(7).mean()

    if recent_avg > previous_avg:
        st.warning(
            f"📈 Phishing spike detected! "
            f"Recent 7-day avg: {recent_avg:.1f}, "
            f"Previous: {previous_avg:.1f}"
        )
else:
    st.info("No phishing incidents found for selected severity.")

# -----------------------------
# SECTION 2: Response Bottleneck Analysis
# -----------------------------
st.subheader("⏱️ Incident Response Bottleneck Analysis")

resolved_only = filtered_data.dropna(subset=['resolution_time_hrs'])

if not resolved_only.empty:
    bottleneck = (
        resolved_only
        .groupby('category')['resolution_time_hrs']
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(bottleneck)

    worst_category = bottleneck.idxmax()
    worst_time = bottleneck.max()

    st.error(
        f"🚧 Response Bottleneck Identified: "
        f"**{worst_category}** "
        f"(Avg Resolution Time: {worst_time:.1f} hrs)"
    )
else:
    st.info("No resolved incidents available for bottleneck analysis.")

# -----------------------------
# SECTION 3: High-Severity Backlog
# -----------------------------
st.subheader("🔥 High-Severity Unresolved Backlog")

if 'status' in filtered_data.columns:
    backlog = filtered_data[
        filtered_data['status'].str.lower() != 'resolved'
    ]

    st.metric(
        label="Unresolved High-Severity Incidents",
        value=len(backlog)
    )

    st.dataframe(backlog)
else:
    st.info("Incident status data not available.")

# -----------------------------
# Raw Data View
# -----------------------------
st.subheader("📄 Filtered Incident Data")
st.dataframe(filtered_data)

# =========================================================
# DATA SCIENCE: DATA GOVERNANCE & DISCOVERY
# (ALIGNED WITH ACTUAL DATABASE SCHEMA)
# =========================================================
st.divider()
st.title("📊 Data Governance & Discovery")

# -----------------------------
# New DB connection (safe)
# -----------------------------
conn_meta = get_connection()
datasets = get_all_datasets_metadata(conn_meta)

if datasets.empty:
    st.info("No dataset metadata available.")
else:
    # -----------------------------
    # Data Preparation
    # -----------------------------
    datasets['upload_date'] = pd.to_datetime(datasets['upload_date'])

    # Derive department from uploader
    def map_department(user):
        if 'cyber' in user.lower():
            return 'Cyber'
        return 'IT / Data'

    datasets['department'] = datasets['uploaded_by'].apply(map_department)

    # Resource consumption proxy
    datasets['cell_count'] = datasets['rows'] * datasets['columns']

    # Dataset age
    datasets['days_since_upload'] = (
        pd.Timestamp.now() - datasets['upload_date']
    ).dt.days

    # -----------------------------
    # Resource Consumption Analysis
    # -----------------------------
    st.subheader("💾 Dataset Resource Consumption")

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(
            datasets.groupby('department')['cell_count'].sum()
        )

    with col2:
        st.bar_chart(
            datasets.set_index('name')['cell_count']
        )

    # -----------------------------
    # Data Source Dependency
    # -----------------------------
    st.subheader("🔗 Data Source Dependency")

    dependency = datasets.groupby('department').agg(
        total_datasets=('dataset_id', 'count'),
        total_cells=('cell_count', 'sum')
    )

    st.dataframe(dependency)

    # -----------------------------
    # Governance & Archiving Policy
    # -----------------------------
    st.subheader("🏛 Governance & Archiving Recommendations")

    def governance_policy(row):
        if row['department'] == 'Cyber':
            return "Retain (Security / Compliance)"
        if row['cell_count'] > 5_000_000:
            return "Review (High Resource Usage)"
        if row['days_since_upload'] > 180 and row['cell_count'] < 100_000:
            return "Archive"
        return "Active Dataset"

    datasets['governance_action'] = datasets.apply(
        governance_policy, axis=1
    )

    st.dataframe(
        datasets[
            [
                'name',
                'department',
                'rows',
                'columns',
                'cell_count',
                'days_since_upload',
                'governance_action'
            ]
        ].sort_values(by='cell_count', ascending=False)
    )


import streamlit as st
from db.db_connection import get_connection

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("Placement Eligibility App")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["Eligibility Checker", "Insights Dashboard"])

conn = get_connection()
cursor = conn.cursor()

# ------------------ ELIGIBILITY CHECKER -------------------
if menu == "Eligibility Checker":
    st.subheader("Check Eligible Students")
    
    if st.button("Show All Students"):
        cursor.execute("SELECT * FROM tbl_students")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])  # Convert sqlite3.Row to dict
    
    st.markdown("#### Filter Students")
    age_filter = st.slider("Minimum Age", 18, 25, 20)
    batch_filter = st.selectbox("Select Batch", ["Batch-1", "Batch-2", "Batch-3", "Batch-4", "Batch-5"])
    
    if st.button("Filter Students"):
        cursor.execute("SELECT * FROM tbl_students WHERE age >= ? AND course_batch = ?", 
                      (age_filter, batch_filter))
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])

# ------------------ INSIGHTS DASHBOARD -------------------
elif menu == "Insights Dashboard":
    st.subheader("Placement Statistics")
    
    tabs = st.tabs(["Students", "Programming", "Soft Skills", "Placements"])
    
    with tabs[0]:
        st.markdown("### All Students Data")
        cursor.execute("SELECT * FROM tbl_students")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])
    
    with tabs[1]:
        st.markdown("### Programming Skills")
        cursor.execute("SELECT * FROM tbl_programming WHERE problems_solved > 50")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])
    
    with tabs[2]:
        st.markdown("### Soft Skills")
        cursor.execute("SELECT * FROM tbl_softskills WHERE communication > 70")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])
    
    with tabs[3]:
        st.markdown("### Placement Status")
        cursor.execute("SELECT * FROM tbl_placements")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])

conn.close()
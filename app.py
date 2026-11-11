import streamlit as st
from supabase import create_client
from datetime import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("Attendance Tracker")

# Employee Name
name = st.text_input("Employee Name")

# Time In Button
if st.button("Time In"):

    if not name:
        st.error("Please enter your name.")
    else:

        current_time = datetime.now()

        supabase.table("attendance").insert({
            "name": name,
            "date": current_time.strftime("%Y-%m-%d"),
            "time_in": current_time.strftime("%H:%M:%S")
        }).execute()

        st.success(
            f"{name} timed in at {current_time.strftime('%H:%M:%S')}"
        )

# Display records
st.subheader("Attendance Records")

records = supabase.table("attendance").select("*").execute()

if records.data:
    st.dataframe(records.data)

import streamlit as st
from supabase import create_client
from datetime import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("Attendance Tracker")

# Employee Name
name = st.text_input("Employee Name")

# Manual Time Input
time_in = st.text_input(
    "Time In (HH:MM)",
    placeholder="08:30"
)

# Save Record
if st.button("Submit Attendance"):

    if not name:
        st.error("Please enter your name.")
    else:
        try:
            # Validate HH:MM format
            datetime.strptime(time_in, "%H:%M")

            response = supabase.table("attendance").insert({
                "name": name,
                "time_in": time_in,
                "date": datetime.now().strftime("%Y-%m-%d")
            }).execute()

            st.success(f"Attendance recorded for {name}")

        except ValueError:
            st.error("Time must be in HH:MM format (example: 08:30)")

# View Raw Records
st.subheader("Raw Attendance Data")

records = supabase.table("attendance").select("*").execute()

if records.data:
    st.dataframe(records.data)

import streamlit as st
from supabase import create_client
from datetime import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("Attendance Tracker")

name = st.text_input("Enter Name")

if st.button("Time In"):
    supabase.table("attendance").insert({
        "name": name,
        "time_in": datetime.now().isoformat()
    }).execute()

    st.success(f"{name} timed in successfully!")

records = supabase.table("attendance").select("*").execute()

st.subheader("Attendance Records")
st.dataframe(records.data)

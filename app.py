import streamlit as st
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

PH_TIMEZONE = ZoneInfo("Asia/Manila")

st.title("Attendance Tracker")

name = st.text_input("Employee Name")

# Display success message after rerun
if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])


@st.dialog("Confirm Attendance")
def confirm_timein():

    st.write("Are you sure you want to log your attendance?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Confirm"):

            current_time = datetime.now(PH_TIMEZONE)
            today = current_time.strftime("%Y-%m-%d")

            existing = (
                supabase.table("attendance")
                .select("*")
                .eq("name", name.strip())
                .eq("date", today)
                .execute()
            )

            if existing.data:
                st.session_state["success_message"] = (
                    f"{name} has already timed in today."
                )
            else:

                supabase.table("attendance").insert({
                    "name": name.strip(),
                    "date": today,
                    "time_in": current_time.strftime("%I:%M:%S %p")
                }).execute()

                st.session_state["success_message"] = (
                    f"✅ {name} timed in successfully at "
                    f"{current_time.strftime('%I:%M:%S %p')}"
                )

            st.rerun()

    with col2:
        if st.button("❌ Cancel"):
            st.rerun()


if st.button("Time In"):

    if not name.strip():
        st.error("Please enter your name.")
    else:
        confirm_timein()

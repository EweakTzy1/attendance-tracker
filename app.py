import streamlit as st
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo

# Supabase Connection
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# Philippines Timezone
PH_TIMEZONE = ZoneInfo("Asia/Manila")

st.title("Attendance Tracker")

# Employee Name
name = st.text_input("Employee Name")

# Time In Button
if st.button("Time In"):

    if not name.strip():
        st.error("Please enter your name.")
    else:

        current_time = datetime.now(PH_TIMEZONE)
        today = current_time.strftime("%Y-%m-%d")

        # Check if employee already timed in today
        existing = (
            supabase.table("attendance")
            .select("*")
            .eq("name", name)
            .eq("date", today)
            .execute()
        )

        if existing.data:
            st.warning(
                f"{name} has already timed in today."
            )
        else:

            supabase.table("attendance").insert({
                "name": name,
                "date": today,
                "time_in": current_time.strftime("%I:%M:%S %p")
            }).execute()

            st.success(
                f"{name} timed in successfully at "
                f"{current_time.strftime('%I:%M:%S %p')}"
            )

# Show Current Philippines Time
st.info(
    f"Current Philippines Time: "
    f"{datetime.now(PH_TIMEZONE).strftime('%Y-%m-%d %I:%M:%S %p')}"
)

# Attendance Records
st.subheader("Attendance Records")

records = (
    supabase.table("attendance")
    .select("*")
    .order("date", desc=True)
    .execute()
)

if records.data:
    st.dataframe(records.data, use_container_width=True)
else:
    st.info("No attendance records found.")

import streamlit as st
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================
# Supabase Connection
# ==========================================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# ==========================================
# Philippines Timezone
# ==========================================
PH_TIMEZONE = ZoneInfo("Asia/Manila")

# ==========================================
# Page Title
# ==========================================
st.title("Attendance Tracker")

# ==========================================
# Current Time
# ==========================================
current_time = datetime.now(PH_TIMEZONE)

st.info(
    f"Current Philippines Time: "
    f"{current_time.strftime('%Y-%m-%d %I:%M:%S %p')}"
)

# ==========================================
# Employee Name
# ==========================================
name = st.text_input("Employee Name")

# ==========================================
# Initial Time In Button
# ==========================================
if st.button("Time In"):
    st.session_state["confirm_timein"] = True

# ==========================================
# Confirmation Section
# ==========================================
if st.session_state.get("confirm_timein", False):

    st.warning("⚠️ Are you sure you want to log your attendance?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes, Confirm"):

            if not name.strip():
                st.error("Please enter your name.")

            else:

                current_time = datetime.now(PH_TIMEZONE)
                today = current_time.strftime("%Y-%m-%d")

                # Check if employee already timed in today
                existing = (
                    supabase.table("attendance")
                    .select("*")
                    .eq("name", name.strip())
                    .eq("date", today)
                    .execute()
                )

                if existing.data:

                    st.warning(
                        f"{name} has already timed in today."
                    )

                else:

                    supabase.table("attendance").insert({
                        "name": name.strip(),
                        "date": today,
                        "time_in": current_time.strftime("%I:%M:%S %p")
                    }).execute()

                    st.success(
                        f"{name} timed in successfully at "
                        f"{current_time.strftime('%I:%M:%S %p')}"
                    )

                st.session_state["confirm_timein"] = False

    with col2:
        if st.button("❌ Cancel"):
            st.session_state["confirm_timein"] = False
            st.info("Time In cancelled.")

# ==========================================
# Attendance Records
# ==========================================
st.subheader("Attendance Records")

try:

    records = (
        supabase.table("attendance")
        .select("*")
        .order("date", desc=True)
        .execute()
    )

    if records.data:
        st.dataframe(
            records.data,
            use_container_width=True
        )
    else:
        st.info("No attendance records found.")

except Exception as e:
    st.error(f"Error loading records: {e}")

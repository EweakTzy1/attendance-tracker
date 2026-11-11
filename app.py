import streamlit as st
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Attendance Tracker",
    page_icon="⏰",
    layout="centered"
)

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
# Team Members
# ==========================================
teams = {
    "TQA": [
        "Michelle Carpio",
        "Joshua Tubeo",
        "Alvin Balmis",
        "Chastine Rose Hamor",
        "Emmarie Presente",
        "Mykee Dalmacio",
        "Jeromyr Canlapan",
        "Cesar Malali",
        "Aubrey Sapico"
    ],
    "SAT": [
        "Aubey Dulva",
        "Dhia Peralta",
        "Exequiel Ian Prado",
        "Grace Elicanal",
        "Geraldine Gando"
    ],
    "Crawler": [
        "Rheanette Dumduma",
        "Aubrey Magalona"
    ],
    "QM": [
        "CJ Carino",
        "Sonny Escol Jr.",
        "Mark Anthony Angcay",
        "Danielle Klare Romero",
        "Abigael Mangarin",
        "Patrick Allan Arcinas",
        "Eric Ebreo"
    ],
    "UAM": [
        "JP Concepcion"
    ]
}

# ==========================================
# Header
# ==========================================
st.title("⏰ Attendance Tracker")

current_time = datetime.now(PH_TIMEZONE)

st.info(
    f"Current Philippines Time: "
    f"{current_time.strftime('%B %d, %Y %I:%M:%S %p')}"
)

# ==========================================
# Team Selection
# ==========================================
selected_team = st.selectbox(
    "Select Your Team",
    [""] + sorted(teams.keys())
)

# ==========================================
# Employee Selection
# ==========================================
selected_name = ""

if selected_team:
    selected_name = st.selectbox(
        "Select Your Name",
        [""] + sorted(teams[selected_team])
    )

# ==========================================
# Success Message
# ==========================================
if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])

# ==========================================
# Confirmation Dialog
# ==========================================
@st.dialog("Confirm Attendance")
def confirm_timein():

    st.write(
        f"Are you sure you want to log attendance for **{selected_name}**?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Confirm", use_container_width=True):

            current_time = datetime.now(PH_TIMEZONE)
            today = current_time.strftime("%Y-%m-%d")

            existing = (
                supabase.table("attendance")
                .select("*")
                .eq("name", selected_name)
                .eq("date", today)
                .execute()
            )

            if existing.data:

                st.session_state["success_message"] = (
                    f"⚠️ {selected_name} has already timed in today."
                )

            else:

                supabase.table("attendance").insert({
                    "name": selected_name,
                    "team": selected_team,
                    "date": today,
                    "time_in": current_time.strftime("%I:%M:%S %p")
                }).execute()

                st.session_state["success_message"] = (
                    f"✅ {selected_name} timed in successfully at "
                    f"{current_time.strftime('%I:%M:%S %p')}"
                )

            st.rerun()

    with col2:

        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

# ==========================================
# Time In Button
# ==========================================
if st.button("Time In", use_container_width=True):

    if not selected_team:
        st.error("Please select your team.")

    elif not selected_name:
        st.error("Please select your name.")

    else:
        confirm_timein()

# ==========================================
# Today's Attendance Data
# ==========================================
today = datetime.now(PH_TIMEZONE).strftime("%Y-%m-%d")

attendance_today = (
    supabase.table("attendance")
    .select("*")
    .eq("date", today)
    .execute()
)

timed_in_names = {
    record["name"]
    for record in attendance_today.data
}

# ==========================================
# Not Yet Timed In
# ==========================================
st.divider()
st.subheader("❌ Employees Without Time In")

total_pending = 0

for team, members in teams.items():

    not_timed_in = [
        member
        for member in members
        if member not in timed_in_names
    ]

    total_pending += len(not_timed_in)

    with st.expander(
        f"{team} ({len(not_timed_in)} pending)",
        expanded=False
    ):

        if not_timed_in:

            for person in sorted(not_timed_in):
                st.write(f"🔴 {person}")

        else:
            st.success("✅ Everyone has timed in.")

st.info(f"Total Pending Attendance: {total_pending}")

# ==========================================
# Timed In Today
# ==========================================
st.divider()
st.subheader("✅ Timed In Today")

if attendance_today.data:

    for record in sorted(
        attendance_today.data,
        key=lambda x: x["name"]
    ):

        st.write(
            f"✅ {record['name']} "
            f"({record['team']}) - "
            f"{record['time_in']}"
        )

else:
    st.warning("No attendance records for today.")

# ==========================================
# Attendance Summary
# ==========================================
total_members = sum(
    len(members)
    for members in teams.values()
)

total_timed_in = len(timed_in_names)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Members", total_members)

with col2:
    st.metric("Timed In", total_timed_in)

with col3:
    st.metric("Pending", total_members - total_timed_in)

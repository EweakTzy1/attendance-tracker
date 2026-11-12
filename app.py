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

st.set_option("client.toolbarMode", "viewer")

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
    ],
    "DM": [
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
# Manual Time Input
# ==========================================
time_in_value = st.text_input(
    "Time In (HH:MM)",
    placeholder="08:30"
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
        f"Are you sure you want to log attendance for "
        f"**{selected_name}** at **{time_in_value}**?"
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

       

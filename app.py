import streamlit as st

st.title("Attendance Tracker")

name = st.text_input("Enter Name")

if st.button("Time In"):
    st.success(f"{name} timed in successfully!")
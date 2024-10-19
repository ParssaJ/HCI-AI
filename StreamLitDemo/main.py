import streamlit as st

st.image("./Assets/static/images/front_logo.png", width=400)

left_column, right_column = st.columns(2)

with left_column:
    search_input = st.text_input(label="Search Item")

options = ("Test1", "Test2")

with right_column:
    selected_box = st.selectbox(label="Please choose your schemata.sql", options=options)
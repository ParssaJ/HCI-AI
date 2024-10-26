import streamlit as st
import configparser

config = configparser.ConfigParser()
config.read('./Assets/static/strings/labels.ini')

# 3 Columns, then use the middle one to assert that image is centered
left_col, middle_col, right_col = st.columns(3)
with middle_col:
    logo_header = config["headers"]["logo_header"]
    st.image("./Assets/static/images/front_logo.png", caption=logo_header)

search_input_label = config["labels"]["search_input_label"]
search_input = st.text_input(label=search_input_label)

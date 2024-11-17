import streamlit as st
import configparser
import os

#https://huggingface.co/stabilityai/stable-code-3b/discussions/6
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate


def show_title_image():
    # 3 Columns, then use the middle one to assert that image is centered
    left_col, middle_col, right_col = st.columns(3)
    with middle_col:
        logo_header = config["headers"]["logo_header"]
        st.image("./Assets/static/images/front_logo.png", caption=logo_header)


def show_selectbox_and_return_selection():
    select_box_caption = config["labels"]["select_box_label"]
    selected_db = st.selectbox(select_box_caption,
                               db_labels, index=2)
    return selected_db


def show_selected_db_schema():
    with open("./Assets/datasets/spider_data/database/" + seletected_database + "/schema.sql") as f:
        selected_schema_content = f.read()
        st.session_state.selected_schema_content = selected_schema_content
    st.image("./Assets/datasets/spider_data/database/" + seletected_database + f"/{seletected_database}.png")


def execute_query():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path="./Assets/models/llama-3.2-3b-instruct-q8_0.gguf",
        callback_manager=callback_manager,
        n_ctx=2048,
        verbose=True,
    )

    template_schema_str = "Based on the following schema: " + st.session_state["selected_schema_content"]

    template = template_schema_str + ("You are the ultimate Database-SQL-Query Constructor."
                                      "Construct a SQL-Query for a Sqlite Database, for {query} ."
                                      "Only output the result-query, nothing else."
                                      "The result-query should be syntactically correct "
                                      "and reflect the structure given the schema."
                                      "Keep the query as simple as possible, no unnecessary joins."
                                      "The select statement should preferably limit itself to one table only."
                                      "The used columns should always be written correctly.Always assert "
                                      "that the referred to columns are actually in your referred table."
                                      "You only output one-query, no semi-cola until the end. Your result-query"
                                      "should reflect the users intend only."
                                      "<|endoftext|>")

    prompt = PromptTemplate(input_variables=["query"], template=template)
    result_query = llm(prompt.format(query=search_input))
    st.session_state.result_query = result_query


config = configparser.ConfigParser()
config.read('./Assets/static/strings/labels.ini')

show_title_image()

db_labels = os.listdir("./Assets/datasets/spider_data/database/")
if ".DS_Store" in db_labels:
    db_labels.remove(".DS_Store")

seletected_database = show_selectbox_and_return_selection()

show_selected_db_schema()

search_input_label = config["labels"]["search_input_label"]
search_input = st.text_input(label=search_input_label)
search_button_submit = st.button(label="Sumbit", on_click=execute_query)

if "result_query" in st.session_state:
    st.header("_Generated_ Repsonse by :red[LLM]", divider="blue")
    st.code(st.session_state["result_query"], language="SQL", wrap_lines=True)


import streamlit as st
import configparser
import os

#https://huggingface.co/stabilityai/stable-code-3b/discussions/6
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate

import pprint
import chromadb
import ast
import json
import re
import io
import random


st.set_page_config(
    page_title="Streamlit Layouts Tutorial",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="collapsed",
)




if "llm" not in st.session_state:
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    st.session_state.llm = LlamaCpp(
        model_path="./Assets/models/llama-3.2-3b-instruct-q8_0.gguf",
        callback_manager=callback_manager,
        n_ctx=4096,
        verbose=True,
    )

llm = st.session_state.llm

if "rag" not in st.session_state:
    chroma_client = chromadb.PersistentClient(
        path="./AI_Training/Preprocessing/chroma_db"
    )

    st.session_state.chroma_collection = chroma_client.get_collection(
        name="train_questions_and_queries"
    )

rag = st.session_state.chroma_collection


def show_title_image():
    # 3 Columns, then use the middle one to assert that image is centered
    left_col, middle_col, right_col = st.columns(3)
    with middle_col:
        logo_header = config["headers"]["logo_header"]
        st.image("./Assets/static/images/front_logo.png", caption=logo_header)
    with left_col:
        logo_header = config["headers"]["logo_header"]

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


def extract_column_names(query):
    pattern = r'(?<=\.)\w+\b'
    results_that_use_aliases = set(re.findall(pattern, query))
    if len(results_that_use_aliases) == 0:
        return query
    return results_that_use_aliases


def clean_schema(schema_content):
    """
    By cleaning we refer to getting rid of the INSERT-Statements which are found in the schema.sql files
    :param schema_content: the schema_file we want to clean
    :return: the (modified) schema but without the INSERT-Statements
    """
    cleaned_schema = []
    for line in io.StringIO(schema_content):
        words_in_line = line.split(" ")
        if words_in_line[0] not in ["INSERT", "\n"]:
            line_to_be_cleaned = " ".join(words_in_line)
            cleaned_line = line_to_be_cleaned.replace("`", "\"")
            if cleaned_line == ");\n":
                cleaned_line += "\n"
            cleaned_schema.append(cleaned_line)

    cleaned_schema = " ".join(cleaned_schema)
    return cleaned_schema

def website_layout():
    col = st.columns([1,3,1]) # 0.2 0.6 0.2
    container_head = st.container(border=True)
    st.divider()
    container_body = st.container()
    with container_head:
        with col[0]:
            st.image("./Assets/static/images/front_logo.png", width=200)

        with col[1]:
            search_input = st.text_input("Searching....",placeholder = "Enter product name",disabled=False)

        with col[2]:
            st.markdown("<style>div.stButton {margin-top: 14px;}</style>", unsafe_allow_html=True)
            search_button = st.button("Submit",on_click=execute_query)
            if(search_button):
                st.session_state.random_zahl = random.randint(0, 100)

    with container_body:
        col = st.columns([1,2,2])  
        container_search_1 = st.container(border=True)
        
        with col[0]:
            st.write("### Optional Filters")
            st.checkbox("Filter 1")
            st.checkbox("Filter 2")
            st.checkbox("Filter 3")


        with container_search_1:
            with col[1]:
                st.markdown(
                    """
                    <div style="border: 2px solid #f0f0f0; padding: 10px; border-radius: 5px;">
                        <h4>{}</h4>
                    """.format(list[(st.session_state.random_zahl%2 == 1)]),
                    unsafe_allow_html=True
                )
                


        with col[2]:
            st.markdown(
                    """
                    <div style="border: 2px solid #f0f0f0; padding: 10px; border-radius: 5px;">
                        <h4>{}</h4>
                    </div>
                    <br>
                    """.format(list[(st.session_state.random_zahl%2 == 0)]),
                    unsafe_allow_html=True
            )
            for dog in dogs_data["dogs"]:
                # Darstellung der Hundedaten
                st.markdown(f"### {dog['breed']} ({dog['category']})")
                if "image" in dog:
                        st.image(dog["image"], caption=dog["breed"])
                st.write(f"**Preis:** {dog['price']}")
                st.write(f"**Geschlecht:** {dog['gender']}")
                st.write(f"**Geburtsdatum:** {dog.get('birthMonth', 'Unbekannt')}")
                #st.write(f"**Beschreibung:** {dog['description'][:150]}...")
                
                if "features" in dog:
                    with st.expander(f"Features zu {dog['breed']}"):
                        st.write("**Besondere Merkmale:**")
                        feature_html = ""
                        for feature in dog["features"]:
                            feature_html += f"""
                            <span style="
                                display: inline-block;
                                background-color: #f0f0f0;
                                border: 1px solid #ddd;
                                border-radius: 5px;
                                padding: 5px 10px;
                                margin: 5px;
                                font-size: 14px;
                                color: #333;
                                font-weight: bold;
                            ">{feature}</span>
                            """
                        st.markdown(feature_html, unsafe_allow_html=True)

                with st.expander(f"Mehr zu {dog['breed']}"):
                    st.markdown(f"#### Details zu {dog['breed']}")
                    st.write(dog["description"])


def execute_query():
    with st.spinner("Finding most similar training data"):
        results = rag.query(
            query_texts=[search_input],
            n_results=3
        )

    question_query_pairs = []
    for i in range(3):
        question = json.loads(results["documents"][0][i])["question"]
        query = json.loads(results["documents"][0][i])["query"]
        question_query_pair = (question, query)
        question_query_pairs.append(question_query_pair)

    first_question, first_query = question_query_pairs[0]
    first_pair = ("Question: " + pprint.pformat(first_question)[1:-1] + "\n" +
                  "Answer: " + pprint.pformat(first_query)[2:-2] + "\n")

    second_question, second_query = question_query_pairs[1]
    second_pair = ("Question: " + pprint.pformat(second_question)[1:-1] + "\n" +
                   "Answer: " + pprint.pformat(second_query)[1:-1] + "\n")

    third_question, third_query = question_query_pairs[2]
    third_pair = ("Question: " + pprint.pformat(third_question)[1:-1] + "\n" +
                  "Answer: " + pprint.pformat(third_query)[1:-1] + "\n")

    cleaned_schema = clean_schema(st.session_state["selected_schema_content"])

    st.success("Examples loaded successfully!")

    with st.spinner("Generating Response. Please stand by..."):
        template = (
            """
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            \nYou are a helpful AI assistant that answers in SQL-Queries only.
            \nThe schema that the user works with is as follows:
            """
            + "\n" + cleaned_schema + "\n"
            + "Here are 3 questions and the corresponding queries generated you can"
            + " consider as examples:\n"
            + "\n" + "First-Example:\n" + first_pair + "\n" + "\nSecond-Example:\n" + second_pair
            + "\nThird-Example:\n" + third_pair +
            """
            \n<|eot_id|><|start_header_id|>user<|end_header_id|>{query}<|eot_id|>\n
            \n<|start_header_id|>assistant<|end_header_id|>\n
            """
        )

        prompt = PromptTemplate(input_variables=["query"], template=template)
        prompt_formatted = prompt.format(query=search_input)
        result_query = llm(prompt_formatted)
        st.session_state.result_query = result_query
        st.session_state.prompt_formatted = prompt_formatted


config = configparser.ConfigParser()
config.read('./Assets/static/strings/labels.ini')

if "random_zahl" not in st.session_state:
    st.session_state.random_zahl = random.randint(0, 100)

db_labels = os.listdir("./Assets/datasets/spider_data/database/")
if ".DS_Store" in db_labels:
    db_labels.remove(".DS_Store")


with open("./Assets/static/database_dog.json", "r", encoding="utf-8") as f:
    dogs_data = json.load(f)

website_layout()

list = ["Search-Results with static Template", "Search-Results with SQI"]

st.write(len(dogs_data["dogs"]))

seletected_database = show_selectbox_and_return_selection()

show_selected_db_schema()


if "result_query" in st.session_state:
    st.header("_Generated_ Repsonse by :red[LLM]", divider="blue")
    st.code(st.session_state["result_query"], language="SQL", wrap_lines=True)

if "prompt_formatted" in st.session_state:
    st.header("System-Prompt used:")
    st.code(st.session_state.prompt_formatted)

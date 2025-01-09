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
import sqlite3
from PIL import Image
from Levenshtein import distance

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
    with open("./Assets/static/database/database_dog.json", "r", encoding="utf-8") as f:
        dogs_data = json.load(f)
    container_head = st.container(border=True)
    st.divider()
    container_body = st.container()
    with container_head:

        with col_head_left:
            col_picture_left,col_picture_middle,col_picture_right = st.columns([1,3,1])
            with col_picture_middle:
                st.write("#### SQI:Search-Query-Interpreter")
                st.image("./Assets/static/images/front_logo.png", width=200)

        with col_head_middle:
            st.write("####")
            st.session_state.search_input = st.text_input("Searching....",placeholder = "Enter product name",disabled=False)
            #st.markdown('<div class="center-input"></div>', unsafe_allow_html=True)
        with col_head_right:
            st.write("####")
            st.markdown("<style>div.stButton {margin-top: 14px;}</style>", unsafe_allow_html=True)
            search_button = st.button("Submit",on_click=execute_query)

    with container_body: 
        container_search_1 = st.container(border=True)

        with col_body_left:
            st.write("### Optional Filters")
            st.session_state.price = st.slider(
                "Wähle einen Preis(€):",  
                min_value=100,         
                max_value=1200,       
                value=(100, 1200),            
                step=1               
            )
            options = ['Rüde', 'Hüdin']
            st.session_state.gender = st.multiselect(
                "Wähle ein Geschlecht:",  # Beschriftung
                options,                        
                default=[] ,
                placeholder = "Wähle Geschlecht"  
            )

            options = ["Mini (bis 25cm)","Klein (bis 40cm)","Mittel (bis 50cm)", "Mittelgroß (bis 60cm) ","Groß (über 60cm)"]
            st.session_state.size = st.multiselect(
                "Wähle eine Größe:",  # Beschriftung
                options,                        
                default=[] ,
                placeholder = "Wähle Größe"  
            )

            options = ["Welpe (bis 3 Monate)", "Junghund (bis 6 Monate)","Subadult (bis 1 Jahr)","Jung Erwachsen (bis 3 Jahre)","Erwachsen (ab 3 Jahre)"]
            st.session_state.age = st.multiselect(
                "Wähle eine Alter:",  # Beschriftung
                options,                        
                default=[] ,
                placeholder = "Wähle Alter"  
            )

            breeds = []
            features = []
            colors = []
            for dog in dogs_data["dogs"]:
                breeds.append(dog["breed"])
                colors.append(dog["color"])
                for feature in dog["features"]:
                    features.append(feature)

            breeds = list(set(breeds))
            breeds.sort()
            selected_merkmale = st.multiselect(
                "Wähle eine Rasse:",  # Beschriftung
                breeds,                        
                default=[] ,
                placeholder = "Wähle Rasse"  
            )

            features = list(set(features))
            features.sort()
            selected_merkmale = st.multiselect(
                "Wähle ein Merkmal:",  # Beschriftung
                features,                        
                default=[] ,
                placeholder = "Wähle Merkmale"  
            )

            colors = list(set(colors))
            colors.sort()
            selected_merkmale = st.multiselect(
                "Wähle eine Farbe:",  # Beschriftung
                colors,                        
                default=[] ,
                placeholder = "Wähle Farbe"  
            )

            with container_search_1:
                with col_body_middle:
                    st.markdown(
                        """
                        <div style="border: 2px solid #f0f0f0; padding: 10px; border-radius: 5px;">
                            <h4>Search-Results with SQI</h4>
                        """,
                        unsafe_allow_html=True
                    )

        with col_body_right:
            st.markdown(
                    """
                    <div style="border: 2px solid #f0f0f0; padding: 10px; border-radius: 5px;">
                        <h4> Search-Results with static Template </h4>
                    </div>
                    <br>
                    """,
                unsafe_allow_html=True
            )

def resize_image(image_path, size=(200, 200)):
    image = Image.open(image_path)
    return image.resize(size)

def execute_query():
    # tokens statt similar      x
    # shuffle entfernen         x
    # center bild               x
    # Title                     x
    # sql lite                  x
    # expander für Merkmale      x
    # filter 
    # size
    # mehr Bilder in einer Zeile 
    
    conn = sqlite3.connect("./Assets/static/database/hund_database.db")
    st.session_state.cursor = conn.cursor()
    if st.session_state.search_input:
        sql_query = f"""SELECT DISTINCT  Hund.* FROM (SELECT * FROM HundFTS WHERE description MATCH '{st.session_state.search_input}') AS matched JOIN Hund on matched.id = Hund.id JOIN Feature_Hund on Feature_Hund.Hund_id = Hund.id LEFT JOIN Feature on Feature.id = Feature_Hund.Feature_id WHERE Hund.price >= {st.session_state.price[0]}  AND {st.session_state.price[1]} >= Hund.price """
    else:
        sql_query = f"""SELECT Hund.* FROM Hund WHERE Hund.price >= {st.session_state.price[0]}  AND {st.session_state.price[1]} >= Hund.price"""
        
    if st.session_state.gender:
        sql_query = f"""SELECT Hund.* FROM (SELECT * FROM HundFTS WHERE description MATCH '{st.session_state.search_input}') AS matched JOIN Hund on matched.id = Hund.id WHERE"""
        if(len(st.session_state.gender) == 1):
            sql_query = f"""SELECT Hund.* FROM (SELECT * FROM HundFTS WHERE description MATCH '{st.session_state.search_input}') AS matched JOIN Hund on matched.id = Hund.id WHERE Hund.gender = '{st.session_state.gender[0].replace("'", "''")}'"""
        else:    
            for i,var in enumerate(st.session_state.gender):
                sql_query = sql_query + f""" Hund.gender = '{var.replace("'", "''")}'"""
                if((i+1) != len(st.session_state.gender)):
                    sql_query = sql_query + " OR"


    sql_query = sql_query + ";"

    st.session_state.cursor.execute(sql_query)
    results = st.session_state.cursor.fetchall()
    print(len(results))
    with col_body_right:
        #print(results[0])  # 8
        for dog in results:
            st.markdown(f"### {dog[1]} ({dog[3]})")
            st.image(dog[9], caption=dog[3])
            st.write(f"**Preis:** {dog[2]}")
            st.write(f"**Geschlecht:** {dog[4]}")
            st.write(f"**Geburtsdatum:** {dog[5]}")
            with st.expander(f"Mehr zu {dog[3]}"):
                st.markdown(f"#### Details zu {dog[3]}")
                st.write(dog[8])
            sql_query = "SELECT Feature.name FROM Hund LEFT JOIN Feature_Hund on Feature_Hund.Hund_id = Hund.id LEFT JOIN Feature on Feature.id = Feature_Hund.Feature_id WHERE Hund.id IS ?;"
            st.session_state.cursor.execute(sql_query,(dog[0],))
            features = st.session_state.cursor.fetchall()
            with st.expander(f"Features zu {dog[3]}"):
                    st.write("**Besondere Merkmale:**")
                    feature_html = ""
                    for feature in features:
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
                            ">{feature[0]}</span>
                            """
                    st.markdown(feature_html, unsafe_allow_html=True)
    
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
search_input = ""




db_labels = os.listdir("./Assets/datasets/spider_data/database/")
if ".DS_Store" in db_labels:
    db_labels.remove(".DS_Store")



with open("./Assets/static/database/database_dog.json", "r", encoding="utf-8") as f:
    dogs_data = json.load(f)

input_text = ""
col_head_left,col_head_middle,col_head_right = st.columns([1,3,1])
col_body_left,col_body_middle,col_body_right = st.columns([1,2,2]) 
website_layout()

st.write(len(dogs_data["dogs"]))

seletected_database = show_selectbox_and_return_selection()

show_selected_db_schema()

if "result_query" in st.session_state:
    st.header("_Generated_ Repsonse by :red[LLM]", divider="blue")
    st.code(st.session_state["result_query"], language="SQL", wrap_lines=True)

if "prompt_formatted" in st.session_state:
    st.header("System-Prompt used:")
    st.code(st.session_state.prompt_formatted)

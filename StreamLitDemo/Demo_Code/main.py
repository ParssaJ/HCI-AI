import streamlit as st

from Util.DatabaseConnectionProvider import DatabaseConnectionProvider
from Util.ModelLoader import ModelLoader
from Util.PageConfigInitialiser import load_page_config
from Views.ColumnManager import ColumnManager


def load_website_layout():
    column_manager = ColumnManager(st)

    column_manager.display_head_container()
    column_manager.display_body_container()


if __name__ == '__main__':
    load_page_config(st)

    db_connection = DatabaseConnectionProvider()

    base_query = ("SELECT h.*, GROUP_CONCAT(F.Name) FROM Hund h INNER JOIN main.Feature_Hund FH on h.id = "
                     "FH.Hund_id INNER JOIN main.Feature F on F.id = FH.Feature_id")

    query_suffix = " GROUP BY h.id LIMIT 50;"

    #st.session_state.results = db_connection.execute_query(base_query)

    llm = ModelLoader.cache_and_load_llm_model()

    if "search_input" in st.session_state:
        like_clauses = " OR ".join([f"h.description LIKE '%{token}%'" for token in st.session_state.search_input.split(" ")])

        # SQL-Query
        query = base_query + f" WHERE {like_clauses}" + query_suffix

        st.session_state.results = db_connection.execute_query(query)
    else:
        query = base_query + query_suffix
        st.session_state.results = db_connection.execute_query(query)

    load_website_layout()

    #if "search_input" in st.session_state and st.session_state.search_input:
    #    template = """
    #    <|system|> You are a helpful AI assistant <|end|><|user|>{search_input}<|end|><|assistant|>
    #    """

    #    prompt = PromptTemplate(input_variables=["search_input"], template=template)
    #    prompt_formatted = prompt.format(search_input=st.session_state.search_input)
    #    result = llm.invoke(prompt_formatted)
    #    st.code(result)

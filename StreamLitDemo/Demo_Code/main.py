import streamlit as st

from Util.DatabaseConnectionProvider import DatabaseConnectionProvider
from Util.ModelLoader import ModelLoader
from Util.PageConfigInitialiser import load_page_config
from Views.ColumnManager import ColumnManager
from langchain.prompts import PromptTemplate

import re


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

    if "search_input" in st.session_state and not st.session_state.search_input.isspace() and st.session_state.search_input:
        like_clauses = " OR ".join(
            [f"h.description LIKE '%{token}%'" for token in st.session_state.search_input.split(" ")])

        # SQL-Query
        static_template_query = base_query + f" WHERE {like_clauses}" + query_suffix

        print(f"Statisches-Template: {static_template_query}")

        st.session_state.static_template_results = db_connection.execute_query(static_template_query)

        template = """
            <|system|>You are a system that completes sqlite queries, based on the users input.
            The Schema of the database is as follows:
            
                CREATE TABLE IF NOT EXISTS Hund (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,          
                    category TEXT,
                    price INTEGER,          
                    breed TEXT,               
                    gender TEXT,            
                    age INTEGER,
                    color TEXT,                
                    birthCountry TEXT,        
                    description TEXT,                 
                    image TEXT,             
                    Webseite TEXT,           
                    image_link TEXT,
                    size TEXT          
                );
                
                
                CREATE TABLE IF NOT EXISTS Feature (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,            
                    Name TEXT UNIQUE         
                );
                
                CREATE TABLE IF NOT EXISTS Feature_Hund (
                    Hund_id INT,                      
                    Feature_id INT,                   
                    PRIMARY KEY (Hund_id, Feature_id),
                    FOREIGN KEY (Hund_id) REFERENCES Hund (id) ON DELETE CASCADE,
                    FOREIGN KEY (Feature_id) REFERENCES Feature (id) ON DELETE CASCADE
                );
                
                CREATE VIRTUAL TABLE IF NOT EXISTS HundFTS USING fts5(id UNINDEXED, description); The following 
                values are stored in the database: 
                categories: Rassehunde, Mischlingshunde, Deckrüden 
                breeds: Australian Shepherd,Toypudel Bolonka Zwetna,Mischling,Labrador Retriever,Golden Doodle, Jack Russel 
                Terrier Mix,Deutscher Schäferhund,Border Collie Mix,Pudel,Zwergpudel Dackel Chihuahua Mix Beagle 
                Cockapoo Cocker Spaniel Labrador Labradoodle Golden Retriever Schnoodle Maltipoo Berner Sennenhund 
                Puggle Border Collie Goldendoodle Havaneser Dobermann Pekinese Chihuahua Jackapoo Französische 
                Bulldogge Dalmatiner Mops Schäferhund-Mix Labrador-Mix Border Collie-Mix Cocker Spaniel-Mix Shiba Inu 
                Jack Russell-Mix Husky Dobermann-Mix Husky-Mix Corgi-Mix Rottweiler Mops-Mix Collie-Mix Terrier-Mix 
                Boxer-Mix Retriever-Mix Golden Retriever-Mix Jack Russell Terrier Deutsch Langhaar Zwergspitz 
                Malteser Labrador-Husky-Mix Dackel-Mix Cavalier King Charles Spaniel Yorkshire Terrier Spitz-Mix 
                Schäferhund-Collie-Mix Bernedoodle Pinscher-Mix Englische Bulldogge Akita Inu Beagle-Mix 
                Husky-Schäferhund-Mix Leonberger-Mix Bordeaux Dogge Papillon-Mix Samojede Australian Shepherd-Border 
                Collie-Mix Australian Shepherd-Border Collie Mix 
                gender: Rüde, Hüdin 
                color: Black-Tri,Weiß Schwarz, 
                Schwarz,Gelb,Braun,Weiß-Braun,Schwarz-Braun,Schwarz-Weiß,Grau Braun,Tricolor,Apricot Weiß 
                Schwarz-Tricolor Fawn Gold Gold-Braun Braun-Weiß Schwarz-braun Creme Dreifarbig Schwarz-weiß 
                Schokoladenbraun Weiß-schwarz getupft Barun Blue Merle Beige Braun-schwarz Weiß mit schwarzen Punkten 
                Orange Grau-weiß Schwarz mit braunen Abzeichen Gold-weiß Weiß-braun Golden Braun-weiß Gestromt Weiß 
                mit braunen Flecken Braun-Schwarz Braun mit Weiß Grau-Weiß Blenheim Cream Blau-Gold Rot-Weiß 
                Schwarz-Weiß-Braun Schwarz-Braun-Weiß Rot-Gold Rot-Braun Orange-Weiß 
                birthCountry: Deutschland,
                Rumänien,Frankreich,Spanien,Schweiz,Österreich,Italien,Belgien,Portugal,Niederlande,Polen Japan 
                Finnland Tschechien Norwegen Schweden Dänemark Irland Kroatien Australien Kanada England Ungarn 
                Griechenland
                size: Mittelgroß (bis 60cm),Mini (bis 25cm), Groß (ab 60cm), Klein (bis 40cm), Mittel (40-60cm)
                features: Allergikerfreundlich,Jagdtrieb,Kinderfreundlich, Stubenrein,Tierschutzgesetz §11, Welpenwurf
                abenteuerlustig, aktiv, anhänglich, arbeitsfreudig, aufmerksam, aus dem Tierheim, ausdauernd,charmant
                energiegeladen, energisch, entspannt, entwurmt,familienfreundlich, familienorientiert, familientauglich
                freundlich, für Anfänger geeignet, für Familien geeignet, für Hundeanfänger geeignet, für Senioren geeignet
                für aktive Familien, für aktive Menschen, für aktive Menschen geeignet, für erfahrene Halter, für erfahrene Hundehalter
                gechipt, geduldig, geimpft (mind. Pflichtimpfungen), gemütlich, intelligent, kinderfreundlich, kinderlieb
                klug, lebhaft, lernbereit, lernfreudig, lernfähig, lernwillig, liebenswert, loyal, mit EU-Heimtierausweis
                mutig, neugierig, nur für erfahrene Hundehalter, ruhig, sanft, sauber, selbstbewusst, selbstsicher, sozial
                sportlich, spürhundqualitäten, tapfer, treu, unabhängig, verschmust, verspielt, verträglich mit Katzen, 
                verträglich mit anderen Hunden, wachsam

                
                Do not output any additional information/text/notes besides the query.
            <|end|><|user|>{search_input}<|end|><|assistant|>{base_query}
            """

        prompt = PromptTemplate(input_variables=["search_input", "base_query"], template=template)
        prompt_formatted = prompt.format(search_input=st.session_state.search_input, base_query=base_query)
        llm_query = llm.invoke(prompt_formatted)
        llm_query = base_query + llm_query
        cleaned_llm_query = re.split(r';', llm_query, maxsplit=1)[0] + ';'

        print(f"Template mit KI: {cleaned_llm_query}")
        st.session_state.llm_results = db_connection.execute_query(cleaned_llm_query)
    else:
        default_query = base_query + query_suffix
        st.session_state.default_results = db_connection.execute_query(default_query)

    load_website_layout()

    #if "search_input" in st.session_state and st.session_state.search_input:
    #    template = """
    #    <|system|> You are a helpful AI assistant <|end|><|user|>{search_input}<|end|><|assistant|>
    #    """

    #    prompt = PromptTemplate(input_variables=["search_input"], template=template)
    #    prompt_formatted = prompt.format(search_input=st.session_state.search_input)
    #    result = llm.invoke(prompt_formatted)
    #    st.code(result)

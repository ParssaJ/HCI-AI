import anthropic
import configparser


if __name__ == '__main__':
    config_parser = configparser.ConfigParser()
    config_parser.read("../../Assets/static/api_keys/config.ini")
    api_key = config_parser["api_keys"]["claude"]
    client = anthropic.Anthropic(api_key=api_key)

    base_query = ("SELECT h.*, GROUP_CONCAT(F.Name) FROM Hund h INNER JOIN main.Feature_Hund FH on h.id = "
            "FH.Hund_id INNER JOIN main.Feature F on F.id = FH.Feature_id")

    database_schema = """
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
                
                CREATE VIRTUAL TABLE IF NOT EXISTS HundFTS USING fts5(id UNINDEXED, description);
    """

    database_features = """
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
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system="Du bist ein System das natürliche Sprache in SQLite-Queries übersetzt. Das Schema der Datenbank ist "
               "wie folgt:" + database_schema + "\n. Folgende Ausprägungen sind in der Datenbank: " + database_features + ". Komplettiere die folgende SQL-Anfrage, basierend auf dem Input des Users: " + base_query + "\n. Gib immer nur die komplettierte SQL-Anfrage zurück.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Alle Shepherds die Lust auf Arbeit haben"
                    }
                ]
            }
        ]
    )
    print(message.content[0].text)

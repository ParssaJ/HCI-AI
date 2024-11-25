# HCI-AI
> [!Caution]
> Um eine Lauffähige Umgebung zu haben, muss man sich eine gguf-Datei aus huggingface herunterladen und diese im model
> Order in den Assets ablegen. Das Model das ich für die Demo benutzt habe findet ihr unter: (https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF/tree/main).
> Hintergrund ist der, dass das Model mit 3.4 GB zu groß für Github ist


> [!Important]
> Eine lauffähige Umgebung kann man mit der Dockerfile erstellen. Hierfür bitte Docker-Desktop herunterladen (vorher nicht vergessen
> die llm in Assets/models abzulegen). Sicherstellen das Docker-Desktop läuft und dann im Oberordner HCI-AI den folgenden Befehl ausführen:
> "docker build -t streamlitdemo ." Damit wird das Image erstellt. Danach kann man das image ausführen mit dem Befehl: "docker run -p 8501:8501 streamlitdemo".
> Die Anwendung sollte nun über localhost:8501 erreichbar sein.


Hallo Ihr beiden,
Wie besprochen, das Repo um zusammen zu coden. Damit das Repo initial nicht zu leer aussieht, hier nochmal die besprochenen Themen im Teamcontract:
- Wir treffen uns im Discord (vorraussichtlich am Wochenende)
- Bei Entscheidungen berücksichtigen wir einen Konsens
- Jeder bewältigt die ihm zugeordneten Aufgaben (wenn man Hilfe braucht einfach auf die anderen zukommen)
- Wir verfolgen die sogenannte Feature-Branching Strategie. Dabei starten wir alle vom Master und wenn wir der Meinung sind,
  dass das Feature das wir auf dem abgebranchten Branch fertig gestellt haben, nun mit dem Master gemerged werden kann, nehmen wir den Merge nicht selbst vor,
  sondern stellen vorher eine Pull-Request(PR). Damit erhält man wertvolles Feedback und es ist eigentlich immer sinnvoll, wenn noch eine weitere
  Person über den Code schaut :)

Habe ich was vergessen? Dann updatet einfach die README

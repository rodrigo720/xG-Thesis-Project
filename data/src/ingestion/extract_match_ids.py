import json
from pathlib import Path

def extract_match_ids():
    
    #prendo i file dentro il percorso .json
    file_richiesti = Path(r"data/raw/matches").glob("*.json")
    lista_file = list(file_richiesti)
    #lista senza duplicati col set()
    tutti_id = set()

    #apro la lista  e li carico 
    for file in lista_file:
        with file.open('r',encoding='utf-8') as f:
            partite=json.load(f)

            #per ogni partita dentro partite, prendo il suo match_id e mettilo in lista
            new_list = [p["match_id"] for p in partite]
            #accumula nella lista principale
            tutti_id.update(new_list)
    





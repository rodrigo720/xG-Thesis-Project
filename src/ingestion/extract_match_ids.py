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

            print(f"{file.name}: {len(partite)} matches")

            #per ogni partita dentro partite, prendo il suo match_id e mettilo in lista
            new_list = [p["match_id"] for p in partite]
            #accumula nella lista principale senza duplicare
            tutti_id.update(new_list)

    print(f"\nTotale match_id unici: {len(tutti_id)}")

    return list(tutti_id)



if __name__ == "__main__":
    match_ids = extract_match_ids()
    output_path= Path("data/processed/match_ids.json")
    output_path.parent.mkdir(parents=True,exist_ok=True)

    with output_path.open('w',encoding='utf-8') as f:
        json.dump(match_ids,f,ensure_ascii=False,indent=2)
    print(f"\nSalvato file: {output_path}")

    





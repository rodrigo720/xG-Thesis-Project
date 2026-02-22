import requests
from pathlib import Path
import json

TARGET_COMPETITIONS = [
        (43,3),        #FIFA World Cup 2018
        (43,106),      #FIFA World Cup 2022
        (55,43),       #UEFA Euro 2020
        (55,282),       #UEFA Euro 2024
]


#funzione che prepara la cartella di destinazione per un sola coppia target
def download_matches(competition_id,season_id):
    
    #percorso della cartella output e controllo/creazione del percorso
    base = Path(r"data/raw/matches")    
    base.mkdir(parents=True,exist_ok=True)

    #nome del file
    file_path = base/ f"{competition_id}_{season_id}.json"

    #controllo se esiste
    if file_path.exists():
        print("file gia presente")
        return file_path
    
    #variabile con l'url richiesta
    url= f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json"

    #check status per download |request|->richiesta di scaricamento
    risposta = requests.get(url,timeout=30)
    if risposta.status_code != 200:
        raise RuntimeError(f"Download fallito{risposta.status_code} per url {url}")
    
    dati_match=risposta.json()

    #salvataggio su file
    with file_path.open('w', encoding='utf-8') as f:  #with utile con i file , gestisce chiusura in automatico
        json.dump(dati_match, f, ensure_ascii=False ,indent=2)

    print("salvato",file_path)
    return file_path

"""
check per una singola coppia target:
if __name__ == "__main__":
    download_matches(43, 3)
"""
#itero per tutti i target
def download_all_matches():
    for competion_id, season_id in TARGET_COMPETITIONS:
        download_matches(competion_id,season_id)


#esecuzione
if __name__ == "__main__":
    download_all_matches()




import requests
import pandas as pd
import time

API_KEY = "SUA_CHAVE_GOOGLE_CLOUD_PLACES"

def buscar_clinicas_santos(termo):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{termo} em Santos SP",
        "key": API_KEY,
        "language": "pt-BR"
    }
    
    leads = []
    while True:
        res = requests.get(url, params=params).json()
        for place in res.get("results", []):
            place_id = place["place_id"]
            # Busca detalhes para pegar o telefone/WhatsApp
            detalhes_url = "https://maps.googleapis.com/maps/api/place/details/json"
            det_params = {
                "place_id": place_id,
                "fields": "name,formatted_address,formatted_phone_number,website",
                "key": API_KEY
            }
            det = requests.get(detalhes_url, params=det_params).json().get("result", {})
            leads.append({
                "Nome": det.get("name"),
                "Telefone": det.get("formatted_phone_number"),
                "Endereco": det.get("formatted_address"),
                "Site_Instagram": det.get("website")
            })
            
        next_page = res.get("next_page_token")
        if not next_page:
            break
        time.sleep(2) # Pausa obrigatória da API antes de pedir a próxima página
        params = {"pagetoken": next_page, "key": API_KEY}
        
    return pd.DataFrame(leads)

# Exemplo de uso:
df_estetica = buscar_clinicas_santos("clinica de estetica harmonizacao")
df_estetica.to_excel("leads_estetica_santos.xlsx", index=False)

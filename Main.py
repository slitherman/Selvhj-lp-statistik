import requests
import json
from datetime import datetime

NOTION_TOKEN = "secret_afo1D1DPc5bgfmk2rUjGPKcybaO7H84xpPdbuVACzWB"
DATABASE_ID = "c7618ad1e8534cbeb410c77d9b0d1a0a"
DELTAGERE_ID = "caa7335229c44532aa7a585570d995e"
GRUPPER_ID = "3c2dd74c18c247ddbbd072fe0109d185"
FRIVILLIGE_ID ="359d0831cf624a85a269328068cba71c"

title = "Selvhjaelp statistik"
text_content = "Statistik"
type_text = "Personer"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(data: dict):
    create_url = f"https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    try:
        res = requests.post(create_url, headers=headers, json=payload)
        res.raise_for_status()
        print("Oprettet")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP-fejl: {err.response.status_code} - {err.response.text}")
    except Exception as e:
        print(f"En fejl opstod: {e}")
         
    
    # print(res.status_code)
    # return res

Dato = "Jan 16, 2024"
dateTimeObj = datetime.strptime(Dato, "%b %d, %Y")
Deltagere = 11
Nye_Deltagere = 1
Mænd =  222
Kvinder = 21

Data = {
    "Dato": {"type": "date", "date": {"start": dateTimeObj.strftime("%Y-%m-%d")}},
    "Deltagere": {"type": "number", "number": Deltagere},
    "Nye deltagere": {"type": "number", "number": Nye_Deltagere},
    "Mænd": {"type": "number", "number": Mænd},
    "Kvinder": {"type": "number", "number": Kvinder},
}

 # create_page(Data)
# with open("sample.json", "w", encoding='UTF8') as outfile:
  #  json.dump(Data, outfile, indent= 4)


def get_pages(num_pages = None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    get_all = num_pages is None
    page_size = 199 if get_all else num_pages
    payload = {"page_size": page_size}
    res = requests.post(url, json=payload, headers=headers)
    res_data = res.json()
    
    output_data = {"payload": payload, "response_data": res_data}
    
    with open("sample.json", "w", encoding='UTF8') as outfile:
        json.dump(res_data, outfile, indent= 4)
    return output_data
    
pages = get_pages()



   


               
               
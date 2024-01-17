import requests
import json
from datetime import datetime
from crontab import CronTab
import os

NOTION_TOKEN = "secret_afo1D1DPc5bgfmk2rUjGPKcybaO7H84xpPdbuVACzWB"
DATABASE_ID = "c7618ad1e8534cbeb410c77d9b0d1a0a"
DELTAGERE_ID = "caa7335229c44532aa7a585570d995e9"
GRUPPER_ID = "3c2dd74c18c247ddbbd072fe0109d185"
FRIVILLIGE_ID = "359d0831cf624a85a269328068cba71c"

title = "Selvhjaelp statistik"
text_content = "Statistik"
type_text = "Personer"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def dumps_data(filepath, dictionary: dict): 
    with open(filepath, 'w', encoding='UTF8') as json_file:
        json.dump(dictionary, json_file, indent=4)

def get_from_source_and_post_to_destination():
 
    deltager_url = f"https://api.notion.com/v1/databases/{DELTAGERE_ID}/query"
    deltager_res = requests.post(deltager_url, headers=headers)
    deltager_data = deltager_res.json()
    dumps_data("deltager_data.json", deltager_data)


    grupper_url = f"https://api.notion.com/v1/databases/{GRUPPER_ID}/query"
    grupper_res = requests.post(grupper_url, headers=headers)
    grupper_data = grupper_res.json()
    dumps_data("grupper_data.json", grupper_data)


    frivillige_url = f"https://api.notion.com/v1/databases/{FRIVILLIGE_ID}/query"
    frivillige_res = requests.post(frivillige_url, headers=headers)
    frivillige_data = frivillige_res.json()
    dumps_data("frivillige_data.json", frivillige_data)
    
    today = datetime.today().strftime("%Y-%m-%d")

    statistik_data = {
        "Dato": {"type": "date", "date": {"start": today}},
        "Deltagere": {"type": "number", "number": deltager_data.get("total_gruppedeltagere", 0)},
        "Nye deltagere": {"type": "number", "number": deltager_data.get("nye_deltagere", 0)},
        "Mænd": {"type": "number", "number": deltager_data.get("antal_mænd", 0)},
        "Kvinder": {"type": "number", "number": deltager_data.get("antal_kvinder", 0)},
        "Børn": {"type": "rich_text", "rich_text": [{"text": {"content": str(deltager_data.get("antal_børn", 0))}}]},
        "Unge": {"type": "rich_text", "rich_text": [{"text": {"content": str(deltager_data.get("antal_unge", 0))}}]},
        "Voksne": {"type": "rich_text", "rich_text": [{"text": {"content": str(deltager_data.get("antal_voksne", 0))}}]},
        "Ældre": {"type": "rich_text", "rich_text": [{"text": {"content": str(deltager_data.get("antal_ældre", 0))}}]},
        "Grupper": {"type": "rich_text", "rich_text": [{"text": {"content" :str(grupper_data.get("total", 0))}}]},
        "Nye Grupper": {"type": "rich_text", "rich_text": [{"text": {"content": str(grupper_data.get("nye_frivillige", 0))}}]},
        "Frivillige i alt": {"type": "rich_text", "rich_text":[{"text": {"content": str(frivillige_data.get("antal_frivillige", 0))}}]},
        "Nye frivillige": {"type": "rich_text", "rich_text": [{"text": {"content": str(frivillige_data.get("nye_frivillige", 0))}}]}
    }

    create_url = f"https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": statistik_data}
    try:
        create_res = requests.post(create_url, headers=headers, json=payload)
        create_res.raise_for_status()
        print("Statistik opdateret")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP-fejl ved opdatering af statistik: {err.response.status_code} - {err.response.text}")
    except Exception as e:
        print(f"En fejl opstod ved opdatering af statistik: {e}")

get_from_source_and_post_to_destination()

script_path = os.path.abspath(__file__)

my_cron = CronTab()

job = my_cron.new(command=f"python {script_path}")

# Kører dagligt ved midnat, hver dag i måneden, hver måned og hver dag i ugen
job.setall('0 0 * * *')

cron_file_path = 'C:\\Cronjobs\\my_cron_file'

my_cron.write(filename=cron_file_path)

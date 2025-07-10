import json
import os
import time
import datetime
import requests
from dotenv import load_dotenv

load_dotenv("./.env")
# create a .env fine in the same directory as this file
# Add the following variable
ZONE_ID = os.getenv("ZONE_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
DOMAIN = os.getenv("DOMAIN")

def main():
    record_id = get_record_id()
    ip_addr = requests.get("https://checkip.amazonaws.com").text
    # r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records", headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"})
    # print(r.json())
    while True:
        update_ip(record_id,ip_addr)
        if ip_addr != requests.get("https://checkip.amazonaws.com").text:
            try:
                update_ip(ip_addr)
            except Exception as e:
                print(e)
                break
        time.sleep(60)

def get_record_id() -> str:
    r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records", headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"})
    for record in r.json()["result"]:
        if record["name"] == DOMAIN:
            return record["id"]
    else:
        raise Exception("No record found")

def update_ip(record_id:str, ip_addr:str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
    }
    data = {
        "name": DOMAIN,
        "type": "A",
        "comment": f"Last update {datetime.datetime.now()}",
        "content": ip_addr,
        "proxied": False
    }
    r = requests.put(f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}", headers=headers, data=json.dumps(data))
    print(r.json())

if __name__ == '__main__':
    main()
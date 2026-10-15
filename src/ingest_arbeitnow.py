import requests
import json
import datetime
import time
import os


def get_jobs(page):

    url = f"https://www.arbeitnow.com/api/job-board-api"

    params = {
        "page": page,
        "search": "data engineer"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    result = response.json()
    return result

def get_all_jobs():
    all_jobs = []
    page = 1
    while True:
        data = get_jobs(page)
        all_jobs += data["data"]
        if data["links"]["next"] == None:
            break 
        page += 1
        time.sleep(2)
    return all_jobs


def save_jobs(data: list) -> None:
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    os.makedirs('data/raw/arbeitnow', exist_ok=True)
    with open(f'data/raw/arbeitnow/data_{current_date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data = get_all_jobs()
    save_jobs(data)
import os
import requests
from dotenv import load_dotenv
import json
import datetime


load_dotenv() #download variablase from .env

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

def get_jobs(country: str, page: int = 1, role: str = 'data engineer', results_per_page = 50) -> dict:

    # 2. собрать параметры запроса
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": role,
        "permanent": 1,
        "full_time": 1,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    result = response.json()

    # print(f"Total jobs found: {result.get('count')}")
    # print(f"Jobs on this page: {len(result.get('results', []))}")
    # print(result)

    return result

def get_all_jobs(country: str, role: str = 'data engineer') -> list:

    all_jobs = []
    jobs_per_page = 50
    first_page = 1
    jobs_json = get_jobs('de', 1, 'data engineer', jobs_per_page)
    all_jobs += jobs_json["results"]
    total_jobs = jobs_json.get('count')

    total_pages = total_jobs // jobs_per_page + 1
    if total_pages > first_page:
        for page in range (first_page + 1, total_pages + 1):
            all_jobs += get_jobs('de', page, 'data engineer', jobs_per_page)["results"]

    return all_jobs


def save_jobs(data: list) -> None:
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    # print(current_date)
    with open(f'data/raw/adzuna/data_{current_date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    data = get_all_jobs('de', 'data engineer')
    save_jobs(data)


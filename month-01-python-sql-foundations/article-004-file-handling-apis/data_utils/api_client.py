# data_utils/api_client.py

import os
import requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Optional for higher rate limits
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

def fetch_news(query="India", api_key=None):
    key = api_key or NEWS_API_KEY
    url = f"https://newsapi.org/v2/top-headlines?q={query}&apiKey={key}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def fetch_github_repos(user, token=None):
    headers = {"Authorization": f"token {token or GITHUB_TOKEN}"} if (token or GITHUB_TOKEN) else {}
    resp = requests.get(f"https://api.github.com/users/{user}/repos", headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_weather(city="Mumbai", api_key=None):
    key = api_key or OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

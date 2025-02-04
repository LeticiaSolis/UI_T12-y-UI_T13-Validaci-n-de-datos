from django.conf import settings
import requests

GOOGLE_SEARCH_API = getattr(settings, 'GOOGLE_SEARCH_API', '')
ID_SEARCH_ENGINE = getattr(settings, 'ID_SEARCH_ENGINE', '')

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,
        "key": GOOGLE_SEARCH_API,
        "cx": ID_SEARCH_ENGINE
    }

    response = requests.get(url, params=params)
    return response.json()
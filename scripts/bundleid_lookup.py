from bs4 import BeautifulSoup
import requests

def get_google_play_name(bundle_id):
    url = f"https://play.google.com/store/apps/details?id={bundle_id}"

    try:
        response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            name_tag = soup.find(attrs={"itemprop": "name"})
            if name_tag and name_tag != 'None':
                return name_tag.text.strip()
            else:
                return "App name not found"
        elif response.status_code == 404:
            return "App not found"
        else:
            return f"HTTP error {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {e}"

def get_apple_store_name(bundle_id):
    url = f"https://itunes.apple.com/lookup?bundleId={bundle_id}"

    try:
        response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("resultCount", 0) > 0:
                return data["results"][0].get("trackName")
            else:
                return "App name not found"
        elif response.status_code == 404:
            return "App not found"
        else:
            return f"HTTP error {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {e}"

def get_galaxy_store_name(bundle_id):
    url = f"https://galaxystore.samsung.com/api/detail/{bundle_id}"

    try:
        response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            content_name = data.get('DetailMain', {}).get('contentName')
            if content_name:
                return content_name
            else:
                return "App name not found"
        elif response.status_code == 404:
            return "App not found"
        else:
            return f"HTTP error {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {e}"
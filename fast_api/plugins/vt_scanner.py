import requests
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv
import os
import base64

# Load the environment variables
enviroment_file_path = Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

VT_API_KEY = os.getenv("VT_API_KEY")
VT_UPLOAD_URL = os.getenv("VT_UPLOAD_URL")
VT_API_URL = os.getenv("VT_API_URL")
VT_ANALYSIS_URL = os.getenv("VT_ANALYSIS_URL")
VT_SEARCH_URL = os.getenv("VT_SEARCH_URL")
VT_LARGE_UPLOAD_FILE = os.getenv("VT_LARGE_UPLOAD_FILE")

def vt_upload(file_path: str) -> Dict:
    url = VT_UPLOAD_URL
    headers = {
        'x-apikey': VT_API_KEY,
    }
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}

def large_file_upload_url() -> Dict:
    url = VT_LARGE_UPLOAD_FILE
    headers = {
        'x-apikey': VT_API_KEY,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def get_large_file_upload_url() -> Dict:
    headers = {
        'x-apikey': VT_API_KEY,
    }
    try:
        response = requests.get(VT_LARGE_UPLOAD_FILE, headers=headers)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def upload_large_file(file_path: str, upload_url: str) -> Dict:
    headers = {
        'x-apikey': VT_API_KEY,
    }
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(upload_url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"File upload failed: {e}")
            return {}

def vt_report(analysis_id: str) -> Dict:
    url = f"{VT_ANALYSIS_URL}/{analysis_id}"
    headers = {
        'x-apikey': VT_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def hash_search(hash: str) -> Dict:
    if not hash or not VT_API_KEY:
        print("Hash or API key is missing")
        return {}
        
    url = f"{VT_UPLOAD_URL}/{hash}"
    headers = {
        'x-apikey': VT_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Hash search request failed: {e}")
        return {}

def url_search(url: str) -> Dict:
    if not url or not VT_API_KEY:
        print("URL or API key is missing")
        return {}
        
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
    search_url = f"{VT_SEARCH_URL}/{encoded_url}"
    
    headers = {
        'x-apikey': VT_API_KEY
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"URL search request failed: {e}")
        return {}
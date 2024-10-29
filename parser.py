import os
import requests
from bs4 import BeautifulSoup

API_KEY = 'API_KEY'
API_URL = 'https://api.curseforge.com'
HEADERS = {'x-api-key': API_KEY}

html_file = 'modlist.html'
download_folder = 'mods'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

with open(html_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')
links = soup.find_all('a')

def requestAPI(url):
    r = requests.get(API_URL + url, headers=HEADERS)
    return r

for i in range(len(links)):
    mod_slug = links[i].get('href').split('/')[-1]
    modId = requestAPI(f'/v1/mods/search?gameId=432&slug={mod_slug}').json()['data'][0]['id']

    try:
        file_data = requestAPI(f'/v1/mods/{modId}/files?modLoaderType=1&gameVersion=1.18.2').json()['data'][0]
        download_url = file_data['downloadUrl']
        file_name = os.path.join(download_folder, file_data['fileName'])

        file_response = requests.get(download_url)
        with open(file_name, 'wb') as f:
            f.write(file_response.content)

        print(f"Файл скачан: {file_name}")
    except Exception as e:
        print(f"Не удалось скачать файл: {mod_slug}, ошибка: {e}")

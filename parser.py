import requests
from bs4 import BeautifulSoup
import os
import time

def download_file(url: str, filepath: str):

    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()  # выкинет исключение, если статус != 200
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Файл сохранён: {filepath}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

def parse_freesound_ambient_wav(
    base_url: str,
    max_pages: int = 5,
    output_dir: str = "freesound_downloads"
):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; FreesoundScraper/1.0)"
    }

    for page_num in range(1, max_pages+1):
        page_url = f"{base_url}&page={page_num}#sound"
        print(f"Processing url: {page_url}")

        try:
            resp = session.get(page_url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error on {page_url}: {e}")
            break 

        soup = BeautifulSoup(resp.text, "html.parser")

        player_divs = soup.find_all("div", class_="bw-player")
        if not player_divs:
            print("No .bw-player. ")
            break

        for div in player_divs:
            title = div.get("data-title", "untitled_sound").strip()
            mp3_link = div.get("data-mp3")
            ogg_link = div.get("data-ogg")

            safe_title = "".join(c for c in title if c.isalnum() or c in " -_()[]{}").rstrip()
            if not safe_title:
                safe_title = f"sound_{int(time.time())}"

            if mp3_link:
                ext = os.path.splitext(mp3_link)[1] 
                filename = f"{safe_title}{ext}"
                filepath = os.path.join(output_dir, filename)
                print(f"   Found preview MP3: {mp3_link} -> {filename}")
                download_file(mp3_link, filepath)
            elif ogg_link:
                ext = os.path.splitext(ogg_link)[1] 
                filename = f"{safe_title}{ext}"
                filepath = os.path.join(output_dir, filename)
                print(f"   Found preview OGG: {ogg_link} -> {filename}")
                download_file(ogg_link, filepath)
            else:
                print(f"   Нет превью (mp3/ogg) у {title}")

        print(f"Page {page_num} done")


    print("Done!")

if __name__ == "__main__":
    url_with_filters = {
        "synthesizer": 
        "https://freesound.org/search/?q=&f=tag%253A%2522synthesizer%2522%2520samplerate%253A44100%2520channels%253A2&s=Date+added+%28newest+first%29&si_tags=0&si_name=0&si_description=0&si_packname=0&si_sound_id=0&si_username=0&d0=0&d1=30&ig=0&r=0&g=1&dp=0&cm=0&mm=0",
        "drum":
        "https://freesound.org/search/?q=&f=channels%253A2%2520samplerate%253A44100%2520tag%253A%2522drum%2522&s=Date+added+%28newest+first%29&si_tags=0&si_name=0&si_description=0&si_packname=0&si_sound_id=0&si_username=0&d0=0&d1=30&ig=0&r=0&g=1&dp=0&cm=0&mm=0",
        "water":
        "https://freesound.org/search/?q=&f=tag%253A%2522water%2522%2520channels%253A2%2520samplerate%253A44100&s=Date+added+%28newest+first%29&si_tags=0&si_name=0&si_description=0&si_packname=0&si_sound_id=0&si_username=0&d0=0&d1=30&ig=0&r=0&g=1&dp=0&cm=0&mm=0",
        "voice":
        "https://freesound.org/search/?q=&f=tag%253A%2522vocal%2522%2520channels%253A2%2520samplerate%253A44100&s=Date+added+%28newest+first%29&si_tags=0&si_name=0&si_description=0&si_packname=0&si_sound_id=0&si_username=0&d0=0&d1=30&ig=0&r=0&g=1&dp=0&cm=0&mm=0",
        
        }

    for key, url in url_with_filters.items():
        
    
        parse_freesound_ambient_wav(
            base_url=url,
            max_pages=17,
            output_dir=f"{key}_samples"
        )

import os
import requests


def delete(word):
    location = "C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/"
    path = os.path.join(location, word)
    os.remove(path)


def get_url(word):
    url = 'https://dictionary.cambridge.org/dictionary/english/' + word

    a = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }).text

    b = a.find('<source type="audio/mpeg" src="/media/english/uk_pron/')
    c = a[b:]
    d = c.find('"/>')
    e = c[:d]
    f = e.find('="/')
    return e[f + 2:]


def scrape(word):
    try:
        URL = "https://dictionary.cambridge.org/" + get_url(word)
        response = requests.get(URL, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        open(f"C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/{word}.mp3", "wb").write(response.content)
        return True
    except:
        return False

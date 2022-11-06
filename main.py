import os

import pypub
import requests
import unidecode
from bs4 import BeautifulSoup

url = "https://lightnovelfr.com/series/lord-of-the-mysteries/"


def download_novel(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    novel = {
        "title": soup.find('h1').text,
        "author": soup.find(class_='serval').text,
        "url": url,
        "synopsis": soup.find(class_='sersys').text,
        "volumes": []
    }

    volumes = soup.find_all(class_='eplisterfull')

    for volume in volumes:
        temp_volume = []

        for chapter in volume.find('ul').find_all('li'):
            temp = chapter.find(class_='epl-num').text.split(' ')
            num_volume, num_chapter = str(int(temp[1])), str(int(temp[3]))

            temp_volume.append({
                "num_volume": num_volume,
                "num_chapter": num_chapter,
                "name": chapter.find(class_='epl-title').text,
                "url": chapter.find('a')['href'],
                "date": chapter.find(class_='epl-date').text,
                "content": get_chap_content(chapter.find('a')['href'])
            })

        temp_volume.reverse()
        novel["volumes"].append(temp_volume)

    novel["volumes"].reverse()
    return novel


def strip_accents(s):
    return unidecode.unidecode(s).replace('«', '').replace('»', '').replace('<<', '"').replace('>>', '"')


def get_chap_content(url):
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup.find(class_='epcontent')


def create_epub_files(novel, filepath):
    epub = pypub.Epub(title=novel["title"], language="fr")

    for volume in novel["volumes"]:
        for chapter in volume:
            chapter_title = "Volume {} Chapitre {} : {}".format(chapter["num_volume"], chapter["num_chapter"],
                                                                chapter["name"])
            c = pypub.create_chapter_from_string(title=strip_accents(chapter_title), html=chapter["content"])
            epub.add_chapter(c)
    epub.create_epub()


novel = download_novel(url)

create_epub_files(novel, os.getcwd())

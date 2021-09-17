# -*- coding: utf-8 -*-
# import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib.parse import quote

from bs4 import BeautifulSoup
import orjson

# data dictionary
data_dict = {}

# Given words
first_word = "ab"
last_word = "zürriyet"

# Filenames
f_output = "output.json"
f_wordlist = "wordlist.txt"

# Request
def req(word):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    url = "https://www.nisanyansozluk.com/?k=" + quote(word) + "&lnk=1&view=annotated"
    session.mount(url, adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
        "accept-encoding": "gzip, deflate, br",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
    }
    r = session.get(url, headers=headers)
    # print(session.cookies.get_dict())
    return r.content


# Sometimes distortions occur when going sequentially in the table. e.g.: add -> "adem"
def back_forward():
    try:
        soup = BeautifulSoup(req(list(data_dict)[-2]), "html5lib")
        cell = soup.find("tr", {"class": "yaz hghlght"})
        nextt_word = cell.nextSibling.nextSibling.nextSibling.nextSibling.td["title"]

        print(
            "back_forward: "
            + list(data_dict)[-2]
            + " => \033[95m"
            + list(data_dict)[-1]
            + "\033[0m => "
            + nextt_word
        )
    except AttributeError:
        soup = BeautifulSoup(req(list(data_dict)[-3]), "html5lib")
        cell = soup.find("tr", {"class": "yaz hghlght"})
        nextt_word = cell.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.td[
            "title"
        ]
        print(
            "back_back_forward: "
            + list(data_dict)[-3]
            + " => \033[95m"
            + list(data_dict)[-2]
            + ", "
            + list(data_dict)[-1]
            + "\033[0m => "
            + nextt_word
        )
    gg(nextt_word)


# final message
def final_msg(msg):
    p_green = "\033[92m"
    p_blue = "\033[94m"
    p_endc = "\033[0m"

    print("-------------------------\n")
    print(p_blue + msg + p_endc + "\n")
    print(
        p_blue
        + "İlk kelime: "
        + p_green
        + list(data_dict)[0]
        + p_blue
        + ", Son kelime: "
        + p_green
        + list(data_dict)[-1]
    )
    print(p_blue + "Toplam kelime sayısı: " + p_green + str(len(data_dict)) + p_endc)
    print(p_blue + "Çıktı dosyası: " + p_green + f_output + p_endc)
    print(p_blue + "Kelime listesi dosyası: " + p_green + f_wordlist + p_endc)
    print("\a")


def export():
    # export data to .json file
    with open(f_output, "wb") as f:
        f.write(orjson.dumps(data_dict))

    # export wordlist to .txt file
    with open(f_wordlist, "w", encoding="utf-8") as f:
        f.write("\n".join(list(data_dict)))


# scrape the cell
def scrape_cell(cell):
    cell = cell
    kelime = cell.td["title"]
    tarih = cell.find("div", {"class": "maddetarih"}).text
    eskoken = cell.find_all("div", {"class": "eskoken"})
    baslik = (
        tarihce
    ) = koken = daha_fazla = ek_aciklama = benzer_sozcukler = maddeye_gonderenler = ""
    baslik = cell.td.a.text

    for i in eskoken:
        if i.div != None:
            title = i.div.text
            if "Tarihçe" in title:
                tarihce = str(i.p)
            elif "Köken" in title:
                koken = str(i.p)
            elif "Ek açıklama" in title:
                ek_aciklama = str(i.p)
            elif "Benzer sözcükler" in title:
                benzer_sozcukler = list(i.p.text.split(", "))
            elif "Bu maddeye gönderenler" in title:
                maddeye_gonderenler = list(i.p.text.strip().split(", "))
        elif "Daha fazla bilgi" in i.p.text:
            k = []
            a = i.p.find_all("a")
            for i in a:
                k.append(i.text)
            daha_fazla = k

    data = {
        "baslik": baslik,
        "tarihce": tarihce,
        "koken": koken,
        "daha_fazla": daha_fazla,
        "ek_aciklama": ek_aciklama,
        "benzer_sozcukler": benzer_sozcukler,
        "maddeye_gonderenler": maddeye_gonderenler,
        "tarih": tarih,
    }
    data_dict[kelime] = data
    print(kelime)


# Main function gg
def gg(first, last):
    word = first
    lastw = last
    print(word + " ➔ " + lastw + "\n")

    done = False

    while not done:
        content = req(word)
        soup = BeautifulSoup(content, "html5lib")
        cell = soup.find("tr", {"class": "yaz hghlght"})
        all_cells = soup.find_all("tr", {"class": "yaz hghlght"})

        # Wrong word
        if len(all_cells) == 0:
            print("Girilen kelime bulunamadı!")
            break
        # Double word e.g.: ram,RAM
        elif len(all_cells) > 1:
            for i in all_cells:
                scrape_cell(i)
        else:
            scrape_cell(cell)

        kelime = cell.td["title"]
        if kelime == lastw:
            done = True
        else:

            if (
                cell.nextSibling.nextSibling != None
                and cell.nextSibling.nextSibling.nextSibling.nextSibling != None
            ):
                if (
                    cell.nextSibling.nextSibling.find("div", {"class": "etymtxt"}).text
                    == ""
                ):
                    word = cell.nextSibling.nextSibling.nextSibling.nextSibling.td[
                        "title"
                    ]
                    continue
                word = cell.nextSibling.nextSibling.td["title"]
            else:
                back_forward()
    else:
        export()
        final_msg("Başarıyla tamamlandı...")
        exit()


def main(first=first_word, last=last_word):
    try:
        gg(first, last)
    except KeyboardInterrupt:
        export()
        final_msg("Liste tamamlanamadı!\nKeyboardInterrupt")
    except Exception as e:
        export()
        final_msg("Liste tamamlanamadı!\nBeklenmedik bir durum oluştu: " + str(e))

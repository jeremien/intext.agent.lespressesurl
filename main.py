#!/usr/bin/env python

from google_dork_scraper import *
from extract import *
import os, time, random
from vpn import *
import urllib

def get_timestamp():
    """Retrieve a pre-formated datetimestamp."""
    now = time.localtime()
    timestamp = time.strftime("%m%d%Y_%H%M%S", now)
    return timestamp

def get_new_word():
    """get a new word from wordlist"""
    with open("words.txt", "r") as f:
        content = f.readlines()
    # content = [x.strip() for x in content]
    content = list(dict.fromkeys(content))
    words = random.choice(content)
    # words = words.lower()
    # words = words.capitalize()
    return words 

def main(num):
    print("[*] Start")
    time = get_timestamp()
    
    print("[#] get a new word")
    word = get_new_word()

    print(f"[*] Initiation timestamp: {time}")
    search_word = '"' + word + '"'
    scraper = Scraper(search_word)
    
    print(f"[$] Querying Results for {search_word}")
    resultats = scraper.go()

    print('resultats', resultats)
    
    if resultats:
        print(f"[*] Get {resultats}")
        dirName = str(num) + '_' + word
        try:
            os.mkdir('./data/' + dirName)
            print(f"[#] create directory {dirName}")
        except FileExistsError:
            print(f"[!] directory {dirName}")
        for i in range(len(resultats)):
            print(f"[*] Get {resultats[i]}")
            extract = Extract(resultats[i], time + '-' + str(i + 1))
            extract.get_content()
            extract.parse_content()
            extract.save_in_file(dirName)
        print(f"[$] All files processed")    
    else:
        print(f"[!] No results")
        vpn()


if __name__ == "__main__":

    try:
        f = open("compteur.txt", "r")
        num = f.read()
        num = int(num)

        while True:
            main(num)
            print(f"[*] iteration n°{num}")
            time.sleep(1)
            num += 1

    except KeyboardInterrupt:
        print(f"[!] ending process at {num}")
        f = open("compteur.txt", "w")
        f.write(str(num))
        f.close()


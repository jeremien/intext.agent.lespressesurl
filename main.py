#!/usr/bin/env python

from google_dork_scraper import *
from extract import *
import os, time, random
from vpn import *

def get_timestamp():
    """Retrieve a pre-formated datetimestamp."""
    now = time.localtime()
    timestamp = time.strftime("%m%d%Y_%H%M%S", now)
    return timestamp

def get_new_words():
    """get a new word from wordlist"""
    with open("words.txt", "r") as f:
        content = f.readlines()
    content = [x.replace('\n', '') for x in content]
    content = list(dict.fromkeys(content))
    words = []
    print(f'[#] wordlist length : {len(content)}')
    if len(content) > 50 and len(content) < 199:
        for i in range(2):
            word = '"' + random.choice(content).strip() + '"'
            words.append(word)
        return '|'.join(words)

    elif len(content) > 200 and len(content) < 399:
        for i in range(3):
            word = '"' + random.choice(content).strip() + '"'
            words.append(word)
        return '|'.join(words)

    elif len(content) > 300 and len(content) < 499:
        for i in range(4):
            word = '"' + random.choice(content).strip() + '"'
            words.append(word)
        return '|'.join(words)

    elif len(content) > 500:
        open("words.txt", "w").close()
        print('[!] reset wordlist')
        return '"' + random.choice(content).strip() + '"'

    else:
        return '"' + random.choice(content).strip() + '"'


def main(num):
    print("[*] Start")
    new_time = get_timestamp()
    
    print("[#] get a new word")
    words = get_new_words()

    print(f"[*] Initiation timestamp: {new_time}")
    scraper = Scraper(words)
    
    print(f"[$] Querying Results for {words}")
    resultats = scraper.go()
    
    if resultats:
        print(f"[*] Get {resultats}")
        dirName = str(num) + '_' + words
        try:
            os.mkdir('./data/' + dirName)
            print(f"[#] create directory {dirName}")
        except (FileExistsError, FileNotFoundError) as err:
            print(f"[!] directory {dirName}, {err}")
        
        for i in range(len(resultats)):
            time.sleep(10)
            print(f"[*] Get {resultats[i]}")
            extract = Extract(resultats[i], new_time + '-' + str(i + 1))
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
            print(f"[*] iteration n°{num}")
            main(num)
            time.sleep(20)
            num += 1

    except KeyboardInterrupt:
        print(f"[!] ending process at {num}")
        f = open("compteur.txt", "w")
        f.write(str(num + 1))
        f.close()


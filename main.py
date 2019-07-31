from google_dork_scraper import *
from extract import *
import os, time

def main():
    print("[*] Start")
    time = get_timestamp()
    
    word = ''
    with open("words.txt", "r") as f:
        for line in f: pass
        word = line

    print(f"[*] Initiation timestamp: {time}")
    search_word = '"' + word + '"'
    scraper = Scraper(search_word)
    
    print(f"[*] Querying Results for {search_word}")
    resultats = scraper.go()

    if len(resultats):
        print(f"[*] Get {resultats}")
        dirName = word
        try:
            os.mkdir(dirName)
            print(f"[*] create directory {dirName}")
        except FileExistsError:
            print(f"[!] directory {dirName}")
        for i in range(len(resultats)):
            print(f"[*] Get {resultats[i]}")
            extract = Extract(resultats[i], time + '-' + str(i + 1))
            extract.get_content()
            extract.parse_content()
            extract.save_in_file(dirName)
        print(f"[*] All files processed")    
    else:
        print(f"[!] No results")

if __name__ == "__main__":
    try:
        i = 1
        while True:
            main()
            time.sleep(10)
            print(f"[*] iteration n°{i}")
            i += 1
    except KeyboardInterrupt:
        print(f"[!] ending process at {i}")

from requests import get
from bs4 import BeautifulSoup
import re
import tomd
import os
from generate_wordlist import * 

class Extract:
    """ extract class object"""

    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name

    def get_content(self):
        self.data = []
        response = get(self.url)
        if response.status_code != 200:
            print(f'[!] {response.status_code}')

        soup = BeautifulSoup(response.content, 'html5lib')
        for tag in soup.find_all(True):
            if tag.name == 'body':
                titres = soup.find_all('h1')
                print(titres)
                try:
                    if len(titres) != 0:
                        wordlist = Wordlist(titres[0].get_text())
                        wordlist.get_first_word()
                    self.data.append(titres)
                    img = soup.find_all('img')
                    images = []
                    try:
                        for i in img:
                            src = i['src']
                            link = f'![{src}]({src})'
                            images.append(link)
                    except KeyError:
                        continue
                    self.data.append(images)
                    paragraphes = soup.find_all('p')
                    self.data.append(paragraphes)
                except IndexError:
                    continue

    def parse_content(self):
        self.markdown = []
        for item in self.data:
            if len(item) != 0:
                for i in item:
                    t = str(i)
                    test = re.search("^!", t)                    
                    if test:
                        self.markdown.append(t)
                    md = tomd.convert(t)
                    self.markdown.append(md)
        filtered = list(filter(lambda x: not re.match(r'^\s*$', x), self.markdown))
        filtered = [x.replace('\n', '') for x in filtered]
        filtered = [x.replace('\t', '') for x in filtered]
        self.markdown = filtered

    def save_in_file(self, dirName):
        try:
            with open('./' + dirName + '/' + self.file_name + '.md', 'w') as file:
                file.writelines('%s\n' % m for m in self.markdown)
            file.close()
        except FileExistsError:
            print("file exist, skip", self.file_name)

if __name__ == "__main__":
    extract = Extract("https://www.mcafee.com/enterprise/fr-fr/security-awareness/ransomware/what-is-stuxnet.html", "new")
    extract.get_content()
    extract.parse_content()
    extract.save_in_file("test")
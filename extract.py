from requests import get, ConnectionError
from bs4 import BeautifulSoup
import re, sys
import tomd
from generate_wordlist import * 
from colorama import Fore
class Extract:
    """ extract class object"""

    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name
        sys.setrecursionlimit(1500)

    def extract_content(self, content):
        """ extract content from url"""

        soup = BeautifulSoup(content, 'html.parser')

        for tag in soup.find_all(True):
            if tag.name == 'body':
                try:
                    titresH1 = soup.find_all('h1')
                    if titresH1:
                        print(Fore.GREEN, f'[#] send {titresH1[0].get_text()} to spacy')
                        wordlist = Wordlist(titresH1[0].get_text())
                        wordlist.get_combination()

                    self.data.append(titresH1)

                    images = []
                    
                    try:
                        imgs = [img['src'] for img in soup.find_all('img')]                        
                        for i in imgs:
                            link = f'![{i}]({i})'
                            images.append(link)
                    
                    except KeyError as err:
                        print(Fore.RED, "[!] key error {0}".format(err))
                        continue
                    
                    self.data.append(images)
                    
                    paragraphes = soup.find_all('p')
                    self.data.append(paragraphes)

                except IndexError as err:
                    print(Fore.RED,"[!] index error {0}".format(err))
                    continue

    def get_content(self):
        """ get url from crawler """

        self.data = []
        
        try:
            response = get(self.url, allow_redirects=False)
            
            if response.status_code != 200:
                print(Fore.RED, f'[!] {response.status_code}')

            else:
                content_type = response.headers.get('content-type')
                
                try:
                    if 'text/html' in content_type:
                        # print('html')

                        self.extract_content(response.content)
                    
                    elif 'application/pdf' in content_type:
                        # print('pdf')
                        pass

                    else:
                        print(Fore.RED, f'[!] unknown type {content_type}')
                
                except TypeError as err:
                    print(Fore.RED, f"[!] Type error : {err}") 

        except ConnectionError as err:
            print(Fore.RED, "[!] network error {0}".format(err))
            pass

    def parse_content(self):
        """ parse data from html to markdown """
        
        self.markdown = []

        try:
            for item in self.data:
                if item:
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
        
        except RuntimeError as err:
            print(Fore.RED, "[!] Recursion {0}".format(err))
            pass

        self.markdown.append('\n' + self.url)

        
    def save_in_file(self, dirName):
        """ savec markdown to file """
        try:
            with open('./data/' + dirName + '/' + self.file_name + '.md', 'w') as file:
                file.writelines('%s\n' % m for m in self.markdown)
            file.close()
        except FileExistsError:
            print(Fore.RED, "[!] file exist, skip", self.file_name)

if __name__ == "__main__":
    extract = Extract("http://www.lefigaro.fr/flash-eco/l-iran-enleve-des-zeros-au-rial-et-renomme-sa-monnaie-20190731", "new")
    extract.get_content()
    extract.parse_content()
    extract.save_in_file("test")
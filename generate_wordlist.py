#!/usr/bin/env python

import spacy
from spacy_langdetect import LanguageDetector
from colorama import Fore
class Wordlist:
    """generate worldlist from search"""

    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp = spacy.load("en_core_web_sm")
        # self.nlp = spacy.load("fr_core_news_sm")

    def langage_detection(self):
        """detect language"""
        self.nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
        doc = self.nlp(self.phrase)
        return doc._.language

    def get_entity(self):
        pass

    def get_sentence(self):
        pass

    def get_combination(self):
        """isolate words combination for search"""
        language = self.langage_detection()
        print(Fore.GREEN,'[*] response from spacy', language)
        if language["language"] == 'en':
            doc = self.nlp(self.phrase)
            res = [chunk.text for chunk in doc.noun_chunks]
            f = open("words.txt", "a")
            for r in res:
                f.write('\n' + r)
                print(Fore.BLUE, f'[$] save {r} in list')
            f.close()

    def get_first_word(self):
        """get pos from sentence and isolate words"""
        language = self.langage_detection()
        print(Fore.WHITE, '[*] response from spacy', language)
        if language["language"] == 'fr':
            doc = self.nlp(self.phrase)
            f = open("words.txt", "a")
            for token in doc:
                print(token.text, token.pos_)
                if token.pos_ == 'NOUN':
                    f.write('\n' + token.text)
                    print(Fore.WHITE, f'[$] save {token.text} in list')
                elif token.pos_ == 'PROPN':
                    f.write('\n' + token.text)
                    print(Fore.WHITE, f'[$] save {token.text} in list')
                elif token.pos_ == 'ADJ':
                    f.write('\n' + token.text)
                    print(Fore.WHITE, f'[$] save {token.text} in list')                                    
            f.close()
        else:
            print(Fore.RED, f'[!] no new word in list')
   

if __name__ == "__main__":
    wordlist = Wordlist("How can I find a synonym for a word")
    wordlist.get_combination()
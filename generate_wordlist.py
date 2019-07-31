import spacy
from spacy_langdetect import LanguageDetector

class Wordlist:
    """generate worldlist from search"""

    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_fr = spacy.load("fr_core_news_sm")

    def langage_detection(self):
        self.nlp_en.add_pipe(LanguageDetector(), name='language_detector', last=True)
        doc = self.nlp_en(self.phrase)
        return doc._.language

    def get_first_word(self):
        language = self.langage_detection()
        print(language)
        if language["language"] == 'en':
            doc = self.nlp_en(self.phrase)
            f = open("words.txt", "a")
            last_word = 'no word'
            for token in doc:
                # print(token.text, token.pos_)
                if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
                    last_word = token.text
            f.write('\n' + last_word)
            f.close()
        elif language["language"] == 'fr':
            doc = self.nlp_fr(self.phrase)
            f = open("words.txt", "a")
            last_word = 'no word'
            for token in doc:
                # print(token.text, token.pos_)
                if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
                    last_word = token.text
            f.write('\n' + last_word)
            f.close()
        else:
            pass    

if __name__ == "__main__":
    wordlist = Wordlist("What is Stuxnet?")
    wordlist.get_first_word()
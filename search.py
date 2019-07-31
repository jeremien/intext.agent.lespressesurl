from googlesearch import search

for url in search('"Breaking"', stop=5):
    print(url)
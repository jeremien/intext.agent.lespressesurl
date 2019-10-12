#!/usr/bin/env python

import random
import numpy
import googlesearch 
from colorama import Fore
class Scraper:
    """scraper class object"""

    def __init__(self, word):
        self.word = word
        self.delay = 30.0
        self.jitter = numpy.random.uniform(low=self.delay, high=1.6 * self.delay, size=(50,))
        with open("user_agents.txt") as fp:
            self.random_user_agents = fp.readlines()
        with open("dorks.txt") as fd:
            self.random_dorks = fd.readlines()

    def go(self):
        """start scraping with google dork intitle"""

        self.links = []
        dork = random.choice(self.random_dorks).strip()
        query = dork + self.word
        print(Fore.GREEN, f"[#] dork query: {query}")
        user_agent = random.choice(self.random_user_agents).strip()
        print(user_agent)
        pause_time = self.delay + random.choice(self.jitter)
        print(Fore.WHITE, f"[*] Pause Time {pause_time} for a new google search")

        try:
            for url in googlesearch.search(
                query,
                start=0,
                stop=100,
                pause=pause_time,
                extra_params={"filter":"0"},
                user_agent=user_agent,
                tbs="qdr:m",
                lang="en"
            ):  
                self.links.append(url)
        
        except Exception as err:
            print(Fore.RED, "[!] Error with {query}", err)
            pass

        return self.links

if __name__ == "__main__":
    scraper = Scraper('"Stuxnet"')
    resultats = scraper.go()
    print(resultats)
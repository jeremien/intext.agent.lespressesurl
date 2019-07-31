#!/usr/bin/env python

import random, time
import numpy

# google == 2.0.1, module author changed import name to googlesearch
# https://github.com/MarioVilas/googlesearch/commit/92309f4f23a6334a83c045f7c51f87b904e7d61d
import googlesearch  # noqa

class Scraper:
    """scraper class object"""

    def __init__(self, word):
        self.word = word
        self.delay = 120.0
        self.jitter = numpy.random.uniform(low=self.delay, high=1.6 * self.delay, size=(50,))
        with open("user_agents.txt") as fp:
            self.random_user_agents = fp.readlines()

    def go(self):
        """start scraping"""

        self.links = []
        query = f"intitle:{self.word}"
        user_agent = random.choice(self.random_user_agents).strip()
        pause_time = self.delay + random.choice(self.jitter)
        print(f"[*] Pause Time {pause_time} for new google search")

        for url in googlesearch.search(
            query,
            start=0,
            stop=20,
            pause=pause_time,
            extra_params={"filter":"0"},
            user_agent=user_agent,
            tbs="li:1" #verbatim mode no suggested results
        ):  
            self.links.append(url)

        return self.links

def get_timestamp():
    """Retrieve a pre-formated datetimestamp."""
    now = time.localtime()
    timestamp = time.strftime("%Y%m%d_%H%M%S", now)
    return timestamp

if __name__ == "__main__":
    print(f"[*] Initiation timestamp: {get_timestamp()}")
    scraper = Scraper("Stuxnet")
    resultats = scraper.go()
    print(resultats)
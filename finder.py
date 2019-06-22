import urllib.request as url
import re
import base64

import requests

from bs4 import BeautifulSoup, Comment
import sys

class Finder:
    def __init__(self):
        self.home = "http://mythicspoiler.com"
        self.cards_hash = None
        self.cards_seen = []
        self.made_card_db = False
        self.cards_to_send = []
        self.first_time = True
        self.limit = 50
    #
    # # make a hash from concatenated links
    # def make_hash(self,links):
    #     hash_to_check = ""
    #     for link in links:
    #         hash_to_check += link
    #     return hash(hash_to_check)

    def make_card_db(self,links):
        for link in links:
            if link not in self.cards_seen:
                self.cards_seen.append(link)
        self.made_card_db = True


    def get_list_of_cards_to_fetch(self):
        html = url.urlopen(self.home + "/newspoilers.html").read()
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            ref = link.get('href')
            # if not a card, skip
            if not re.search('\S/cards/\S', ref):
                continue
            # add to list of card links
            links.append(ref)
        # make card DB if doesn't exist
        if not self.made_card_db:
            self.make_card_db(links)
        if self.first_time:
            for i in range(self.limit):
                self.get_card_image(self.cards_seen[i])
            self.first_time=False
        else:
            for link in links:
                if link not in self.cards_seen:
                    self.get_card_image(link)

    def get_card_image(self,link):
        expansion = re.findall('(\S+)/cards/', link)[0]
        # new card
        spoil = re.findall('\S/cards/(\S+)', link)[0]
        spoil_name = spoil[:-5]
        # url to jump to
        base_url = self.home + "/" + expansion + "/cards/"
        try:
            # Get card URL
            card_dest = base_url + spoil_name + ".jpg"
            resp = requests.get(card_dest)
            # make base64 image
            img = base64.b64encode(resp.content)
            self.cards_to_send.append(img)
        except IOError:
            print("eish")


def main():
    card_finder = Finder()
    card_finder.get_list_of_cards_to_fetch()
    for item in card_finder.cards_to_send:
        break


if __name__=='__main__':
    main()

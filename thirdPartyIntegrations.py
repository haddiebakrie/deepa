# -*- coding: utf-8 -*-
import os
import csv
import glob
from bs4 import BeautifulSoup as bs
import requests

def parse_td(td):
    """

    :param td: 

    """
    if td.text != "": return td.text
    return [x.text for x in td.find_all("li")]

def fetchJumiaProduct(page):
    """

    :param page: 

    """
    req = requests.get(page)
    title = bs(req.text, 'html.parser').find(class_="-fs20 -pts -pbxs").text
    price = bs(req.text, 'html.parser').find(class_="-b -ubpt -tal -fs24 -prxs").text.replace("₦", "").replace(",", "")
    imageLink = bs(req.text, 'html.parser').find(class_="-fw -fh")['data-src']
    metadata = bs(req.text, 'html.parser').find_all("tr")
    all = []
    def parse_td(td):
        """

        :param td: 

        """
        if td.text != "": return td.text
        return [x.text for x in td.find_all("li")]
    for i in metadata:
        data = {}
        tab = i.find_all("td")
        if len(tab) > 1:
            data[tab[0].text] = parse_td(tab[1])
            all.append(data)
    met = {}
    for i in all:
        for x, y in i.items():
            met[x] = y

    if all == []:
        detail = bs(req.text, 'html.parser').find(class_="markup -mhm -pvl -oxa -sc")
        ps = detail.children
        ps = [x.text for x in ps]
        all.append({"Product info": " \n ".join(ps)})

    for i in all:
        print(i)

    met["imageUrl"] = imageLink

    return {
        "productTitle": title,
        "productAmount": price,
        "productDescription": all[0]["Product info"],
        "metadata": met
    }

import requests
from bs4 import BeautifulSoup

def get_dict_titles(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("table", {"class": "wikitable"})
    titles = {}
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 2:
            # Warning : we should use findall for the movies as there are sometimes
            # more than 1 adaptation
            titles[cells[0].find(text=True)] = cells[1].find(text=True)
    return titles

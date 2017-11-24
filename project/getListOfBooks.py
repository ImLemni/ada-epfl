import requests
from bs4 import BeautifulSoup


def get_dict_titles(urlList):
    titles = {}
    for url in urlList:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        tables = soup.findAll("table", {"class": "wikitable"})
        for table in tables:
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) == 2:
                    # Warning : we should use findall for the movies as there are sometimes
                    # more than 1 adaptation
                    movie_data = cells[1].findAll(text=True)
                    movie_titles = [movie_data[0]]
                    movie_titles_mult = [value for index, value in enumerate(
                        movie_data) if movie_data[(index - 1) % len(movie_data)] == '\n']
                    titles[cells[0].find(text=True)] = list(
                        set(movie_titles + movie_titles_mult))
    return titles


urlList = ["https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939_and_A%E2%80%93C)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)"]
movies = get_dict_titles(urlList)
len(movies.keys())

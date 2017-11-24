from ada import data
from ada import getListOfBooks


urlList = ["https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939_and_A%E2%80%93C)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
           "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)"]
dict_books_movies = getListOfBooks.get_dict_titles(urlList)

movies_titles = [item for sublist in dict_books_movies.values()
                 for item in sublist]
len(movies_titles)

movies_association = {el.lower():[] for el in movies_titles}

movies_metada_lines = data.read_data_file("meta_Movies_and_TV", 208321)
for movie_line in movies_metada_lines:
    if 'title' in movie_line:
        title = movie_line['title'].lower()
        if title in movies_association:
            movies_association[title].append(movie_line)


sum([len(v) for _,v in movies_association.items()])/len(movies_titles)

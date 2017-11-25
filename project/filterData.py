from ada import data
from ada import getListOfBooks
from re import sub


def clean_title(title):
    removable = ['[', ']', 'dvd', 'vhs',
                 '(', ')', ',', '.', '!', '?', ':', ';']
    title = title.lower()
    # title = sub("\((.*film.*|.*movie.*)\)", "", title)
    title = sub("\(.*\)", "", title)
    title = sub("\s+", " ", title)
    title = sub("\s$", "", title)
    title = sub("^\s", "", title)
    for r in removable:
        title = title.replace(r, "")
    return title


def get_matching_product():
    urlList = ["https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939_and_A%E2%80%93C)",
               "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
               "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
               "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)"]
    dict_books_movies = getListOfBooks.get_dict_titles(urlList)

    movies_titles = [item for sublist in dict_books_movies.values()
                     for item in sublist]
    print(f"Number of movies from wikipedia : {len(movies_titles)}")

    for i, mov in enumerate(movies_titles):
        movies_titles[i] = clean_title(mov)

    movies_association = {el: [] for el in movies_titles}

    movies_metada_lines = data.read_data("meta_Movies_and_TV", 208321)
    for movie_line in movies_metada_lines:
        if 'title' in movie_line:
            title = clean_title(movie_line['title'])
            if title in movies_association:
                movies_association[title].append(movie_line)

    print(f"Number of movies selected: {sum([1 if len(v) > 0 else 0 for _, v in movies_association.items()])}")

    books_titles = [book for book in dict_books_movies]
    print(f"Number of books from wikipedia : {len(books_titles)}")

    for i, book in enumerate(books_titles):
        books_titles[i] = clean_title(book)

    books_association = {el: [] for el in books_titles}

    books_metada_lines = data.read_data("meta_Books", 2370585)
    for book_line in books_metada_lines:
        if 'title' in book_line:
            title = clean_title(book_line['title'])
            if title in books_association:
                books_association[title].append(book_line)
    print(f"Number of books selected: {sum([1 if len(v) > 0 else 0 for _, v in books_association.items()])}")

    total_selected = 0
    for k, v in dict_books_movies.items():
        associate = False
        if len(books_association[clean_title(k)]) > 0:
            for mov in v:
                if len(movies_association[clean_title(mov)]) > 0:
                    associate = True
                    break
        total_selected += 1 if associate else 0
    print(f"Number of association book/movies : {total_selected}")
    return books_association,movies_association

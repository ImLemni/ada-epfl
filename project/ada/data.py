import gzip
import os
import json
from ada.progressbar import ProgressBar
from ada.locations import get_abs_path


def read_json_file(file_path, limit, show_progress_bar=True):
    with open(file_path, 'r') as file:
        if show_progress_bar:
            with ProgressBar(limit) as progress_bar:
                for i, line in enumerate(file):
                    yield eval(line)
                    progress_bar.update(1)
                    if i == limit - 1:
                        break
        else:
            for i, line in enumerate(file):
                yield eval(line)
                if i == limit - 1:
                    break


def read_gzip_file(file_path, limit, show_progress_bar=True):
    with gzip.open(file_path, 'rb') as file:
        if show_progress_bar:
            with ProgressBar(limit) as progress_bar:
                for i, line in enumerate(file):
                    yield eval(line)
                    progress_bar.update(1)
                    if i == limit - 1:
                        break
        else:
            for i, line in enumerate(file):
                yield eval(line)
                if i == limit - 1:
                    break


def read_data_file(file_name, limit, show_progress_bar=True):
    json_path = get_abs_path("data", f"{file_name}.json")
    gzip_path = get_abs_path("data", f"{file_name}.json.gz")
    if os.path.isfile(json_path):
        return read_json_file(json_path, limit, show_progress_bar)
    else:
        return read_gzip_file(gzip_path, limit, show_progress_bar)


if __name__ == "__main__":
    reviews = read_data_file("reviews_Amazon_Instant_Video", 10)
    for review in reviews:
        print(review)

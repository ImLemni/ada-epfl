import gzip
import os
import json
from typing import Optional

import pandas
from ada.progressbar import ProgressBar, NoOpProgressBar
from ada.locations import get_abs_path


def get_path(data_name: str, use_gzip=True) -> str:
    if use_gzip:
        return get_abs_path("data", f"{data_name}.json.gz")
    else:
        return get_abs_path("data", f"{data_name}.json")


def read_json_file(file_path: str, limit: Optional[int], is_gzip: bool, show_progress_bar: bool = True):
    if limit is None:
        show_progress_bar = False
    with (gzip.open(file_path, 'rb') if is_gzip else open(file_path, 'r')) as file:
        with (ProgressBar(limit) if show_progress_bar else NoOpProgressBar(limit)) as progress_bar:
            if limit is not None and limit <= 0:
                return
            for i, line in enumerate(file):
                yield eval(line)
                progress_bar.update(1)
                if limit is not None and i == limit - 1:
                    break


def read_data(data_name, limit, show_progress_bar=True):
    json_path = get_path(data_name, False)
    gzip_path = get_path(data_name, True)
    if os.path.isfile(json_path):
        return read_json_file(json_path, limit, False, show_progress_bar)
    elif os.path.isfile(gzip_path):
        return read_json_file(gzip_path, limit, True, show_progress_bar)
    else:
        raise RuntimeError(f"File not found: {json_path}")


def write_data(data_name, data, use_gzip=True):
    file_path = get_path(data_name, use_gzip)

    with (gzip.open(file_path, 'wb') if use_gzip else open(file_path, 'wb')) as file:
        for item in data:
            file.write(json.dumps(item).encode())
            file.write(b'\n')


def read_df(data_name, limit, show_progress_bar=True):
    return pandas.DataFrame(read_data(data_name, limit, show_progress_bar))


if __name__ == "__main__":
    reviews = read_data("reviews_Amazon_Instant_Video", 10)
    for review in reviews:
        print(review)

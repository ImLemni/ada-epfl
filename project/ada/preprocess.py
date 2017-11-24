import ada
import os


def normalize_json(in_name: str, out_name: str) -> None:
    entries = ada.data.read_data(in_name, None)
    ada.data.write_data(out_name, entries)


def run():
    if not os.path.isfile(ada.data.get_path("meta_videos")):
        print("Normalizing videos")
        normalize_json("meta_Amazon_Instant_Video", "meta_videos")
    if not os.path.isfile(ada.data.get_path("meta_movies")):
        print("Normalizing movies")
        normalize_json("meta_Movies_and_TV", "meta_movies")
    if not os.path.isfile(ada.data.get_path("meta_books")):
        print("Normalizing books")
        normalize_json("meta_Books", "meta_books")


if __name__ == "__main__":
    run()

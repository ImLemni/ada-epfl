import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_abs_path(*segments):
    return os.path.normpath(os.path.join(PROJECT_ROOT, *segments))


REL_DATA_PATH = "./data"
ABS_DATA_PATH = get_abs_path("data")

if __name__ == "__main__":
    print("""
    PROJECT_ROOT = {!r}
    REL_DATA_PATH = {!r}
    ABS_DATA_PATH = {!r}
    """.format(PROJECT_ROOT, REL_DATA_PATH, ABS_DATA_PATH))

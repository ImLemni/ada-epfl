import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
REL_DATA_PATH = "./data"


def get_abs_path(*segments: str) -> str:
    """
    Converts a path relative to the the project root into an absolute path.

    :param segments: Segments of the relative path (from the project root)
    :return: Absolute path
    """
    return os.path.normpath(os.path.join(PROJECT_ROOT, *segments))


# Absolute path to the data directory, by default it uses the `data` directory in the project.
# You can configure it by setting the `ADA_DATA_PATH` environment variable.
ABS_DATA_PATH = os.environ["ADA_DATA_PATH"] if "ADA_DATA_PATH" in os.environ else get_abs_path(REL_DATA_PATH)


def get_abs_data_path(*segments):
    """
    Converts a path relative to the the data directory into an absolute path.

    :param segments: Segments of the relative path (from the data directory)
    :return: Absolute path
    """
    return get_abs_path(ABS_DATA_PATH, *segments)


if __name__ == "__main__":
    print("""
    PROJECT_ROOT = {!r}
    REL_DATA_PATH = {!r}
    ABS_DATA_PATH = {!r}
    """.format(PROJECT_ROOT, REL_DATA_PATH, ABS_DATA_PATH))

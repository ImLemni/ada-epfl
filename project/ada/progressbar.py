try:
    from tqdm import tqdm
except:
    tqdm = None

try:
    from ipywidgets import FloatProgress
    from IPython.display import display
except:
    FloatProgress, display = None, None


class NoOpProgressBar():
    """
    Represents a progressbar that does not do anything
    """

    def __init__(self, total: int):
        self.total = total
        self.progress = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def update(self, change: int):
        self.progress += change


if tqdm is not None:
    class TqdmProgressBar():
        def __init__(self, total: int):
            self.total = total
            self.progress = 0
            self._bar = None

        def __enter__(self):
            self._bar = tqdm(total=self.total)
            self._bar.__enter__()
            return self

        def __exit__(self, *args):
            if self._bar is not None:
                self._bar.close()
                self._bar = None

        def update(self, change: int):
            self.progress += change
            if self._bar is not None:
                self._bar.update(change)

if FloatProgress is not None and display is not None:
    class IPythonProgressBar():
        def __init__(self, total: int):
            self.total = total
            self.progress = 0
            self._bar = None

        def __enter__(self):
            self._bar = FloatProgress(min=0, max=self.total)
            display(self._bar)
            return self

        def __exit__(self, *args):
            pass

        def update(self, change: int):
            self.progress += change
            self._bar.value = self.progress

if tqdm is not None:
    ProgressBar = TqdmProgressBar
else:
    ProgressBar = IPythonProgressBar

if __name__ == "__main__":
    import time

    with ProgressBar(10) as pb:
        pb.update(0)
        for x in range(1, 11):
            time.sleep(1)
            pb.update(1)

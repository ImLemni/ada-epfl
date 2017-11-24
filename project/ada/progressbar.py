def get_tqdm():
    try:
        import tqdm
        return tqdm.tqdm
    except:
        return None


def get_ipython():
    try:
        from ipywidgets import FloatProgress
        from IPython.display import display
        return FloatProgress, display
    except:
        return None


tqdm = get_tqdm()
ipython = None  # get_ipython()

if tqdm is not None:
    class ProgressBar():
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
elif ipython is not None:
    FloatProgress, display = ipython


    class ProgressBar():
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
else:
    class ProgressBar():
        def __init__(self, total: int):
            self.total = total
            self.progress = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def update(self, change: int):
            self.progress += change

if __name__ == "__main__":
    import time

    with ProgressBar(10) as pb:
        pb.update(0)
        for x in range(1, 11):
            time.sleep(1)
            pb.update(1)

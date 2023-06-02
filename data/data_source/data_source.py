# From https://github.com/frankieeder/data_flow/blob/main/abstract.py


class DataSource:
    def source(self):
        raise NotImplementedError

    def clean(self, data):
        return data

    def finalize(self, data):
        return data

    def read(self):
        uncleaned = self.source()
        cleaned = self.clean(uncleaned)
        return cleaned

    def process(self):
        cleaned = self.read()
        finalized = self.finalize(cleaned)
        return finalized

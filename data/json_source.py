from urllib.request import urlopen
import json

from .data_source import DataSource


class JSONDataSource(DataSource):
    URL = ""

    def source(self):
        with urlopen(self.URL) as response:
            as_dict = json.load(response)
        return as_dict

from urllib.request import urlopen
import json

from .data_source import DataSource


class CountyGeoJSON(DataSource):
    def source(self):
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            county_boundaries = json.load(response)
        return county_boundaries
from urllib.request import urlopen
import json

from data.data_source.data_source import DataSource


class ZipGeoJSON(DataSource):
    def source(self, state_identifier_string="ca_california"):
        url = (
            f"https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/"
            f"{state_identifier_string}_zip_codes_geo.min.json"
        )
        with urlopen(url) as response:
            zipcodes = json.load(response)
        return zipcodes

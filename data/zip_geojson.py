from urllib.request import urlopen
import json

from .data_source import DataSource


class ZipGeoJSON(DataSource):
    def source(self, state_identifier_string='ca_california'):
        with urlopen(
                f'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/{state_identifier_string}_zip_codes_geo.min.json') as response:
            zipcodes = json.load(response)
        return zipcodes

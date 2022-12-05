import pandas as pd
from .data_source import DataSource


class ZipToFips(DataSource):
    def source(self):
        return pd.read_excel('./ZIP_COUNTY_122021.xlsx', sheet_name='SQLT0004', dtype={'zip': str, 'county': str})

    def clean(self, zip_to_fips_raw):
        zip_to_fips = zip_to_fips_raw.set_index('zip')['county']
        return zip_to_fips

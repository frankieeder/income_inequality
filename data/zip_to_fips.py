import pandas as pd
from pathlib import Path

from .data_source import DataSource


class ZipToFips(DataSource):
    LOCAL_FILE_DIR = Path(__file__).parent.resolve() / 'local_files' / 'ZIP_COUNTY_122021.xlsx'

    def source(self):
        return pd.read_excel(self.LOCAL_FILE_DIR, sheet_name='SQLT0004', dtype={'zip': str, 'county': str})

    def clean(self, zip_to_fips_raw):
        zip_to_fips_raw_deduped = zip_to_fips_raw\
            .sort_values('tot_ratio', ascending=False)\
            .drop_duplicates(subset='zip')
        zip_to_fips = zip_to_fips_raw_deduped.set_index('zip')['county']
        return zip_to_fips


if __name__ == '__main__':
    zip_to_fips = ZipToFips().process()

import urllib.request as urllib2
import lxml.html
from lxml import etree
import pandas as pd

from pathlib import Path

from data.data_source.data_source import DataSource


class FipsCountyInfo(DataSource):
    LOCAL_FILE_DIR = (
        Path(__file__).parent.parent.resolve() / "local_files" / "fips_county_info.csv"
    )

    def __init__(self, get_remote=False):
        self.get_remote = get_remote

    def source(self):
        if self.get_remote:
            c = urllib2.urlopen(
                "https://en.wikipedia.org/wiki/List_of_United_States_FIPS_codes_by_county"
            )
            tree = lxml.html.fromstring(c.read())
            table = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]')[0]
            county_fips_to_names = pd.read_html(etree.tostring(table))[0]
            return county_fips_to_names
        else:
            return pd.read_csv(self.LOCAL_FILE_DIR)

    def clean(self, df):
        df["FIPS"] = df["FIPS"].apply(lambda i: format(i, "05d"))
        df = df.set_index("FIPS")
        df = df.rename(
            columns={
                "County or equivalent": "county_name",
                "State or equivalent": "state_name",
            }
        )
        return df


if __name__ == "__main__":
    FipsCountyInfo(get_remote=True).process().to_csv(
        FipsCountyInfo.LOCAL_FILE_DIR, index=False
    )

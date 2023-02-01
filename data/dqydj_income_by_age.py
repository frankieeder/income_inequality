import urllib.request as urllib2
import lxml.html
from lxml import etree
import pandas as pd

from pathlib import Path

from .data_source import DataSource


class DQYDJIncomeByAge(DataSource):
    LOCAL_FILE_DIR = Path(__file__).parent.resolve() / 'local_files' / 'income_by_age.csv'
    URL = 'https://dqydj.com/income-percentile-by-age-calculator/'

    def __init__(self, get_remote=False):
        self.get_remote = get_remote

    def source(self):
        if self.get_remote:
            c = urllib2.urlopen(self.URL)
            tree = lxml.html.fromstring(c.read())
            table = tree.xpath('//*[@id="span-14-299"]/figure/table')[0]
            ceo_compensation = pd.read_html(etree.tostring(table), header=0)[0]
            return ceo_compensation
        else:
            return pd.read_csv(self.LOCAL_FILE_DIR)

    def clean(self, df):
        df = df.set_index('Age')
        df = df.transform(lambda c: c.str.replace('[$,]', '').astype('float'))
        return df


if __name__ == '__main__':
    ds = DQYDJIncomeByAge(get_remote=True)
    ds.source().to_csv(ds.LOCAL_FILE_DIR)

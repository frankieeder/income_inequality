import urllib.request as urllib2
import lxml.html
from lxml import etree
import pandas as pd

from pathlib import Path

from .data_source import DataSource


class PayscaleCeoCompensation(DataSource):
    LOCAL_FILE_DIR = Path(__file__).parent.resolve() / 'local_files' / 'payscale_ceo_compensation.csv'
    URL = 'https://www.payscale.com/data-packages/ceo-pay/full-list'

    def __init__(self, get_remote=False):
        self.get_remote = get_remote

    def source(self):
        if self.get_remote:
            c = urllib2.urlopen(self.URL)
            tree = lxml.html.fromstring(c.read())
            table = tree.xpath('//*[@id="Table1"]//table')[0]
            ceo_compensation = pd.read_html(etree.tostring(table), header=0)[0]
            return ceo_compensation
        else:
            return pd.read_csv(self.LOCAL_FILE_DIR)

    def clean(self, df):
        null_cols = [c for c in df.columns if c.startswith('Unnamed')]
        df = df.drop(columns=null_cols)
        currency_cols = {
            'ceo_compensation': 'Total CEO  Compensation',
            'median_compensation': 'Median Worker  Annual Pay  (Cash)'
        }
        for new_c, c in currency_cols.items():
            df[new_c] = df[c].replace('[\$,]', '', regex=True).astype(float)
        df['ratio'] = df['ceo_compensation'] / df['median_compensation']
        return df


if __name__ == '__main__':
    ds = PayscaleCeoCompensation(get_remote=True)
    ds.source().to_csv(ds.LOCAL_FILE_DIR)

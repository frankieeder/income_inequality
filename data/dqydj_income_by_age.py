from pathlib import Path
import pandas as pd

from .data_source import DataSource


class DQYDJIncomeByAge(DataSource):
    LOCAL_FILE_DIR = Path(__file__).parent.resolve() / 'local_files' / 'income_by_age.html'

    def source(self):
        return pd.read_html(self.LOCAL_FILE_DIR, header=0)[0]

    def clean(self, df):
        df = df.set_index('Age')
        df = df.transform(lambda c: c.str.replace('[$,]', '').astype('float'))
        return df

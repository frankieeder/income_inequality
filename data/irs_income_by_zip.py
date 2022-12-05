import pandas as pd

from .data_source import DataSource
from .zip_to_fips import ZipToFips


class IRSIncomeByZip(DataSource):
    AGI_STUB_LOWER_BOUNDS = {
        1: 1,
        2: 25,
        3: 50,
        4: 75,
        5: 100,
        6: 200,
    }
    AGI_STUB_DESCRIPTION = {
        1: '$1-25k',
        2: '$25k-50k',
        3: '$50k-75k',
        4: '$75k-100k',
        5: '$100k-200k',
        6: '$200k+',
    }
    CALCULATED_METRICS = {
        'mean_income_per_return': 'Mean Income per Return',
        'mean_income_per_individual': 'Mean Income per Individual',
    }
    METRIC_NAMES = {
        'N1': 'Number of Tax Returns',
        'N2': 'Number of Individuals',
        'A00100': 'Total AGI',
        **CALCULATED_METRICS,
    }

    def source(self):
        return pd.read_csv('https://www.irs.gov/pub/irs-soi/19zpallagi.csv', dtype={'zipcode': str})

    @staticmethod
    def calculate_additional_income_stats(df):
        df['mean_income_per_return'] = df['A00100'] / df['N1']
        df['mean_income_per_individual'] = df['A00100'] / df['N2']
        return df

    @classmethod
    def clean(cls, income_df):
        income_df = cls.calculate_additional_income_stats(income_df)
        income_df['agi_stub_lower_bound'] = income_df['agi_stub'].replace(cls.AGI_STUB_LOWER_BOUNDS)
        income_df['agi_stub_desc'] = income_df['agi_stub'].replace(cls.AGI_STUB_DESCRIPTION)
        zip_to_fips = ZipToFips().process()
        income_df = income_df.merge(zip_to_fips, left_on='zipcode', right_index=True, how='left')
        return income_df
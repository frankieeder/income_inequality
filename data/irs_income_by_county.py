import pandas as pd

from .data_source import DataSource
from .irs_income_by_zip import IRSIncomeByZip


class IRSIncomeByCounty(DataSource):
    AGI_STUB_RANGE = range(1, 7)
    CALCULATED_METRICS = {
        **{f'agi_stub_{i}_N1': f'Number of Reports in AGI Stub {i}' for i in AGI_STUB_RANGE},
        **{f'agi_stub_{i}_prop_N1': f'Proportion of Reports in AGI Stub {i}' for i in AGI_STUB_RANGE},
    }
    METRIC_NAMES = {
        **IRSIncomeByZip.METRIC_NAMES,
        **CALCULATED_METRICS,
    }

    def source(self):
        return IRSIncomeByZip().process()

    @staticmethod
    def county_aggregator(df):
        d = {}
        d['N1'] = df['N1'].sum()
        d['N2'] = df['N2'].sum()
        d['A00100'] = df['A00100'].sum()
        agi_stub_sums = df.groupby('agi_stub')['N1'].sum()
        agi_stub_proportions = agi_stub_sums / agi_stub_sums.sum()
        # agi_stub_lte_proportions = agi_stub_proportions.cumsum()
        for i in range(1, 7):
            d[f'agi_stub_{i}_N1'] = agi_stub_sums[i]
            d[f'agi_stub_{i}_prop_N1'] = agi_stub_proportions[i]
            # d[f'agi_stub_lte{i}_prop_N2']
        return pd.Series(d)

    @classmethod
    def clean(cls, income_df):
        county_sums = income_df.groupby('county').apply(cls.county_aggregator)
        county_sums = IRSIncomeByZip.calculate_additional_income_stats(county_sums)
        return county_sums
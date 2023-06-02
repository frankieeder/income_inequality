import pandas as pd

from data.data_source.data_source import DataSource
from data.irs.irs_income import IRSIncome


class IRSIncomeByGroup(DataSource):
    AGI_STUB_RANGE = range(1, 7)
    CALCULATED_METRICS = {
        **{
            f"agi_stub_{i}_N1": f"Number of Tax Returns w/ AGI in Range {IRSIncome.AGI_STUB_DESCRIPTION[i]}"
            for i in AGI_STUB_RANGE
        },
        **{
            f"agi_stub_{i}_prop_N1": (
                f"Proportion of Tax Returns w/ AGI in Range {IRSIncome.AGI_STUB_DESCRIPTION[i]}"
            )
            for i in AGI_STUB_RANGE
        },
    }
    METRIC_NAMES = {
        **IRSIncome.METRIC_NAMES,
        **CALCULATED_METRICS,
    }

    def source(self):
        return IRSIncome().process()

    @classmethod
    def group_aggregator(cls, df):
        d = {}
        d["N1"] = df["N1"].sum()
        d["N2"] = df["N2"].sum()
        d["A00100"] = df["A00100"].sum()
        agi_stub_sums = df.groupby("agi_stub")["N1"].sum()
        agi_stub_proportions = agi_stub_sums / agi_stub_sums.sum()
        # agi_stub_lte_proportions = agi_stub_proportions.cumsum()
        for i in cls.AGI_STUB_RANGE:
            d[f"agi_stub_{i}_N1"] = agi_stub_sums[i] if i in agi_stub_sums.index else 0
            d[f"agi_stub_{i}_prop_N1"] = (
                agi_stub_proportions[i] if i in agi_stub_proportions.index else 0
            )
            # d[f'agi_stub_lte{i}_prop_N2']
        return pd.Series(d)

    @classmethod
    def process_by_group(cls, income_df, grouping):
        group_sums = income_df.groupby(grouping).apply(cls.group_aggregator)
        group_sums = IRSIncome.calculate_additional_income_stats(group_sums)
        return group_sums

    @classmethod
    def clean(cls, income_df):
        raise NotImplementedError

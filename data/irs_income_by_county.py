from .irs_incom_by_group import IRSIncomeByGroup


class IRSIncomeByCounty(IRSIncomeByGroup):
    @classmethod
    def clean(cls, income_df):
        return IRSIncomeByGroup.process_by_group(income_df, 'county')

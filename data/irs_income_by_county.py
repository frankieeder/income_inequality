from .irs_income_by_group import IRSIncomeByGroup


class IRSIncomeByCounty(IRSIncomeByGroup):
    @classmethod
    def clean(cls, income_df):
        grouped = IRSIncomeByGroup.process_by_group(income_df, ['county', 'county_name', 'state_name'])
        grouped = grouped.reset_index()
        grouped = grouped.set_index('county')
        return grouped

from pathlib import Path
import pandas as pd

from .data_source import DataSource


class DQYDJIncomeByAge(DataSource):
    # https://dqydj.com/income-percentile-by-age-calculator/
    # Inspecting scripts led here
    # https://dqydj.com/scripts/cps/2022_income_calculators/2022_income_by_age.html
    # Then reading the js gave me the below link:
    REMOTE_URL = "https://dqydj.com/scripts/cps/2022_income_calculators/cps_2022_income_by_age.csv"
    LOCAL_FILE_DIR = (
        Path(__file__).parent.resolve() / "local_files" / "cps_2022_income_by_age.csv"
    )

    def source(self):
        return pd.read_csv(self.LOCAL_FILE_DIR)

    def clean(self, df):
        df = df.set_index("Pct")
        return df

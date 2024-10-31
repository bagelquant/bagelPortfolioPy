"""
Data Handler
"""

import pandas as pd
from dataclasses import dataclass, field


@dataclass(slots=True)
class DataHandler:
    """
    This class is built specific for the McGill porfolio event.
    It does not offer any flexibility for other types of data.
    """
    
    path: str = "data/data.xlsx"
    raw_data: list[pd.DataFrame] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.assets = self.set_assets()
        self.raw_data.extend(self.load_data())

    @staticmethod
    def set_assets() -> list[str]:
        return [
            # Equity
            "FTSE All Cap",
            # "FTSE Factor Weighted",
            # "Private Equity",
               
            # Fixed Income
            "US Treasury",
            "US MBS",
            "Corporate",
            "High Yield",
            "EM Bond",
               
            # Real Assets
            ]
    
    def load_data(self) -> list[pd.DataFrame]:
        all_data = []
        for sheet in self.assets:
            asset_data = pd.read_excel(self.path, sheet_name=sheet, index_col=0)
            asset_data.columns = [sheet]
            asset_data = self.remove_date_keep_month(asset_data)
            all_data.append(asset_data)
        return all_data
    
    @staticmethod
    def remove_date_keep_month(asset_data: pd.DataFrame) -> pd.DataFrame:
        """
        The raw data has mismatched dates, some are at beginning of month, some are at end of month.

        This function will remove the date and keep only the year and month.
        If the data is at beginning of month, it will have month - 1.
        """
        if asset_data.index[0].day == 1:  # type: ignore
            asset_data.index = asset_data.index.shift(-1, freq="D")
        asset_data.index = asset_data.index.to_period("M")  # type: ignore
        # remove duplicates
        asset_data = asset_data[~asset_data.index.duplicated(keep="first")]  # type: ignore
        return asset_data

    def get_all_data(self) -> pd.DataFrame:
        data = pd.concat(self.raw_data, axis=1).sort_index()
        data = self.handle_missing_data(data)
        return data
    
    @staticmethod
    def handle_missing_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        Just for this example, since it only missing the oldest data, and one newest data for All Cap index.
        We'll forward fill the missing data then drop the first n rows with missing data.
        """
        data = data.ffill()
        return data.dropna()
            

if __name__ == "__main__":
    data_handler = DataHandler()
    data = data_handler.get_all_data()
    data.plot()
    import matplotlib.pyplot as plt
    plt.show()
    # data.to_excel('data/data_cleaned.xlsx')
    

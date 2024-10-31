"""
Portfolio class
"""

import pandas as pd
from dataclasses import dataclass, field


@dataclass(slots=True)
class Porfolio:
    
    cash_weights: float
    data: pd.DataFrame
    
    assets: list[str] = field(default_factory=list, init=False)
    weights: dict[str, float] = field(default_factory=dict, init=False)
    drifts: pd.DataFrame = field(init=False)
    
    def __post_init__(self):
        self.assets = self.data.columns.tolist()
        self.weights = {asset: 0 for asset in self.assets}
        self.drifts = self.data.pct_change()

    def __repr__(self):
        return f"""
        Portfolio weights:
            Cash: {self.cash_weights}
            Weights: {self.weights}
        Porfolio statistics:
            Expected Return: {self.expected_return()}
            Volatility: {self.volatility()}
        """
    
    def covariance(self):
        return self.drifts.cov()

    """
    ---------------------
    Portfolio statistics
    ---------------------
    """

    def expected_return(self):
        assets_expected_return = self.drifts.mean(axis=0)
        weights = pd.Series(self.weights.values(), index=self.assets)
        return (assets_expected_return * weights).sum()

    def volatility(self):
        cov = self.covariance()
        weights = pd.Series(self.weights.values(), index=self.assets)
        return (weights @ cov @ weights) ** 0.5

    """
    ---------------------
    Assets statistics
    ---------------------
    """

    def assets_expected_return(self):
        return self.drifts.mean(axis=0)

    def assets_volatility(self):
        return self.drifts.std(axis=0)

    def assets_sharpe_ratio(self, rf: float = 0.0):
        return (self.assets_expected_return() - rf) / self.assets_volatility()


if __name__ == "__main__":
    # test for simple data
    data = pd.DataFrame({
        "AAPL": [1, 2, 3],
        "GOOGL": [4, 5, 6],
        "MSFT": [7, 8, 9]
    })

    p = Porfolio(cash_weights=0.1, data=data)
    print(p)

    # test for mcgill data
    from datahandler import DataHandler
    datahandler = DataHandler()
    data = datahandler.get_all_data()
    p = Porfolio(cash_weights=0.1, data=data)
    p.weights = {
        "FTSE All Cap": 0.2,
        "US Treasury": 0.3,
        "US MBS": 0.2,
        "Corporate": 0.1,
        "High Yield": 0.1,
        "EM Bond": 0.1
    }
    print(p)
    print(p.assets_expected_return())
    

"""
Portfolio class
"""

import pandas as pd
from dataclasses import dataclass, field


@dataclass(slots=True)
class Portfolio:
    
    cash_weights: float
    data: pd.DataFrame
    
    assets: list[str] = field(default_factory=list, init=False)
    weights: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))
    drifts: pd.DataFrame = field(init=False)
    
    def __post_init__(self):
        self.assets = self.data.columns.tolist()
        if self.weights.empty:
            self.weights = pd.Series({asset: (1 - self.cash_weights) / len(self.assets) for asset in self.assets})
        self.drifts = self.data.pct_change()

    def __repr__(self):
        return f"""
        =====================
        Portfolio weights:

        - Cash: {self.cash_weights}
        - Weights (Round to 4 decimal places):
        {self.weights.round(4)}

        Porfolio statistics:

        - Expected Return: {self.expected_return()}
            - Annualized: {(1 + self.expected_return()) ** 12 - 1}
        - Volatility: {self.volatility()}
        - sharpe ratio: {self.sharpe_ratio()}
        =====================
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
        return (assets_expected_return * self.weights).sum()

    def volatility(self):
        cov = self.covariance()
        return (self.weights @ cov @ self.weights) ** 0.5

    def sharpe_ratio(self, rf: float = 0.0):
        return (self.expected_return() - rf) / self.volatility()

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

    """
    ---------------------
    backtesting
    ---------------------
    """

    def get_portfolio_data(self):
        portfolio_drifts = self.drifts @ self.weights
        portfolio_data = (1 + portfolio_drifts).cumprod()
        portfolio_data.iloc[0] = 1
        portfolio_data.name = "Portfolio"
        return portfolio_data


if __name__ == "__main__":
    # test for simple data
    data = pd.DataFrame({
        "AAPL": [1, 2, 3],
        "GOOGL": [4, 5, 6],
        "MSFT": [7, 8, 9]
    })

    p = Portfolio(cash_weights=0.1, data=data)
    print(p)

    # test for mcgill data
    from datahandler import DataHandler
    datahandler = DataHandler()
    data = datahandler.get_all_data()
    p = Portfolio(cash_weights=0.1, data=data)
    p.weights = pd.Series({
        "FTSE All Cap": 0.2,
        "US Treasury": 0.3,
        "US MBS": 0.2,
        "Corporate": 0.1,
        "High Yield": 0.1,
        "EM Bond": 0.1
    })
    print(p)
    

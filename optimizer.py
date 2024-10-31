"""
Optimizer class
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from portfolio import Portfolio

@dataclass(slots=True)
class Optimizer(ABC):
    """
    input: portfolio class
    output: new portfolio class
    """
    portfolio: Portfolio

    constraints: list[dict] = field(default_factory=list, init=False)
    init_weights: pd.Series = field(default_factory=lambda: pd.Series(dtype=float), init=False)

    @abstractmethod
    def optimize(self) -> Portfolio:
        pass
    
    @abstractmethod
    def _objective(self, x: np.array) -> float:  # type:ignore
        pass

    def add_constraint(self, constraint: dict):
        self.constraints.append(constraint)

    def add_constraint_nneg(self):
        self.add_constraint({'type': 'ineq', 'fun': lambda x: x})
    
    def add_constraint_sum_one(self):
        self.add_constraint({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    def add_constraint_sum_less_one(self):
        self.add_constraint({'type': 'ineq', 'fun': lambda x: 1 - np.sum(x)})
    
    def add_constraint_sum_one_inc_cash(self):
        self.add_constraint({'type': 'eq', 'fun': lambda x: np.sum(x) + self.portfolio.cash_weights - 1})

    def add_constraint_lower_bound(self, lower_bound: pd.Series):
        self.add_constraint({'type': 'ineq', 'fun': lambda x: x - lower_bound})


@dataclass(slots=True)
class MeanVarianceOptimizer(Optimizer):
    """
    Mean-variance optimizer
    
    Only optimize the risky assets and return a highest Sharpe ratio portfolio
    """

    covariance: pd.DataFrame = field(init=False)
    expected_return: pd.Series = field(init=False)
    
    def __post_init__(self):
        self.covariance = self.portfolio.covariance()
        self.init_weights = self.portfolio.weights
        self.expected_return = self.portfolio.assets_expected_return()  # type:ignore

    def _objective(self, x: np.array) -> float:  # type:ignore
        """
        Objective function to minimize
        """
        return -((self.expected_return @ x) / np.sqrt(x @ self.covariance @ x))

    def optimize(self) -> Portfolio:
        """
        Optimize the portfolio weights
        """
        if self.constraints:
            result = minimize(self._objective, self.init_weights, constraints=self.constraints)
        else:
            result = minimize(self._objective, self.init_weights)
        weights = pd.Series(result.x, index=self.portfolio.assets)
        return Portfolio(cash_weights=self.portfolio.cash_weights, data=self.portfolio.data, weights=weights)


# McGill Portfolio 2024

## Functionality

- [ ] Mean variance optimization
- [ ] Portfolio backtest
- [ ] Portfolio visualization

## Structure

```mermaid
---
title: Project Structure
---
graph LR
Portfolio --> Optimizer
Optimizer --> Portfolio
Portfolio --> Backtest
Backtest --> p[plot functions]
```

### Main classes responsibilities

```mermaid
classDiagram
class Portfolio{
    +cash_weight: float
    +data: pd.DataFrame
    +assets: list[str]
    +weights: dict[str, float]

    -__post_init__()
    -__repr__()
    +covariance()
    +expected_return()
    +volatility()
    +sharpe_ratio()

    +assets_expected_return()
    +assets_volatility()
    +assets_sharpe_ratio()
}
```

```mermaid
classDiagram
class Optimizer{
    +portfolio: Portfolio
    +risk_free_rate: float

    -__post_init__()
    -__repr__()
    +optimize()
}
```

This is a simple project structure. Just a few classes that interact with each other. 



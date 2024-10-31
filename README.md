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
---
title: Portfolio class
---
classDiagram
class Portfolio{
    -cash_weight: float
    -data: pd.DataFrame
    +assets: list[str]
    +weights: dict[str, float]

    -__post_init__()
    -__repr__()

}
```

This is a simple project structure. Just a few classes that interact with each other. 

Extand this structure to include:
- DataHandler: 


## `Portfolio` class

- input:

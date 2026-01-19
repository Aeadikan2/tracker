from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass
class IncomeEntry:
    amount: float
    date: str  # ISO format YYYY-MM-DD
    savings: float = 0.0
    expenses: float = 0.0
    investments: float = 0.0
    discretionary: float = 0.0

@dataclass
class BudgetConfig:
    savings_pct: float = 0.30
    expenses_pct: float = 0.50
    investments_pct: float = 0.10
    discretionary_pct: float = 0.10

    def validate(self) -> bool:
        total = self.savings_pct + self.expenses_pct + self.investments_pct + self.discretionary_pct
        return abs(total - 1.0) < 0.001

    def to_dict(self) -> Dict[str, float]:
        return {
            "savings_pct": self.savings_pct,
            "expenses_pct": self.expenses_pct,
            "investments_pct": self.investments_pct,
            "discretionary_pct": self.discretionary_pct
        }

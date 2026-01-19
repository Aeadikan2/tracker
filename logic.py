from models import IncomeEntry, BudgetConfig
from database import Database
from datetime import datetime
from typing import List, Dict

class BudgetManager:
    def __init__(self):
        self.db = Database()
        self.config = self.db.get_settings()

    def calculate_split(self, amount: float, date_str: str = None) -> IncomeEntry:
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        # Refresh config in case it changed
        self.config = self.db.get_settings()

        entry = IncomeEntry(
            amount=amount,
            date=date_str,
            savings=amount * self.config.savings_pct,
            expenses=amount * self.config.expenses_pct,
            investments=amount * self.config.investments_pct,
            discretionary=amount * self.config.discretionary_pct
        )
        return entry

    def add_income(self, amount: float, date_str: str = None) -> IncomeEntry:
        entry = self.calculate_split(amount, date_str)
        self.db.save_income(entry)
        return entry

    def update_settings(self, savings: float, expenses: float, investments: float, discretionary: float) -> bool:
        new_config = BudgetConfig(savings, expenses, investments, discretionary)
        if new_config.validate():
            self.db.save_settings(new_config)
            self.config = new_config
            return True
        return False

    def get_history(self) -> List[IncomeEntry]:
        return self.db.get_all_entries()

    def get_cumulative_savings(self) -> float:
        entries = self.get_history()
        return sum(e.savings for e in entries)
        
    def get_monthly_stats(self) -> Dict[str, float]:
        entries = self.get_history()
        # Simple stats for now, can be expanded
        total_income = sum(e.amount for e in entries)
        total_savings = sum(e.savings for e in entries)
        return {
            "total_income": total_income,
            "total_savings": total_savings,
            "entry_count": len(entries)
        }

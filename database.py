import csv
import json
import os
from typing import List, Optional
from models import IncomeEntry, BudgetConfig
import pandas as pd

DATA_FILE = "income_data.csv"
SETTINGS_FILE = "settings.json"

class Database:
    def __init__(self):
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Total Income", "Savings", "Expenses", "Investments", "Discretionary"])
        
        if not os.path.exists(SETTINGS_FILE):
            default_config = BudgetConfig()
            self.save_settings(default_config)

    def save_income(self, entry: IncomeEntry):
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                entry.date,
                entry.amount,
                entry.savings,
                entry.expenses,
                entry.investments,
                entry.discretionary
            ])

    def get_all_entries(self) -> List[IncomeEntry]:
        if not os.path.exists(DATA_FILE):
            return []
        
        df = pd.read_csv(DATA_FILE)
        entries = []
        for _, row in df.iterrows():
            entries.append(IncomeEntry(
                date=row["Date"],
                amount=float(row["Total Income"]),
                savings=float(row["Savings"]),
                expenses=float(row["Expenses"]),
                investments=float(row["Investments"]),
                discretionary=float(row["Discretionary"])
            ))
        return entries

    def get_settings(self) -> BudgetConfig:
        if not os.path.exists(SETTINGS_FILE):
            return BudgetConfig()
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                return BudgetConfig(
                    savings_pct=data.get("savings_pct", 0.30),
                    expenses_pct=data.get("expenses_pct", 0.50),
                    investments_pct=data.get("investments_pct", 0.10),
                    discretionary_pct=data.get("discretionary_pct", 0.10)
                )
        except json.JSONDecodeError:
            return BudgetConfig()

    def save_settings(self, config: BudgetConfig):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(config.to_dict(), f, indent=4)

import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, Confirm
from rich.layout import Layout
from rich import print as rprint
from logic import BudgetManager
from models import BudgetConfig
from datetime import datetime

console = Console()
manager = BudgetManager()

def print_header():
    console.clear()
    console.print(Panel.fit("[bold blue]Personal Income Tracker[/bold blue]", border_style="blue"))

def display_menu():
    print_header()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Description")
    table.add_row("1", "Add New Income")
    table.add_row("2", "View History and Reports")
    table.add_row("3", "View/Edit Budget Settings")
    table.add_row("4", "Exit")
    console.print(table)

def add_income_ui():
    print_header()
    console.print("[bold green]Add New Income[/bold green]\n")
    
    amount = FloatPrompt.ask("Enter total income amount")
    if amount <= 0:
        console.print("[red]Income must be positive![/red]")
        Prompt.ask("Press Enter to continue...")
        return

    date_str = Prompt.ask("Enter date (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
    
    try:
        entry = manager.add_income(amount, date_str)
        
        console.print("\n[bold]Budget Breakdown:[/bold]")
        table = Table(show_header=True)
        table.add_column("Category")
        table.add_column("Amount", justify="right")
        table.add_column("Percent", justify="right")
        
        config = manager.config
        table.add_row("Savings", f"₦{entry.savings:.2f}", f"{config.savings_pct*100:.0f}%")
        table.add_row("Expenses", f"₦{entry.expenses:.2f}", f"{config.expenses_pct*100:.0f}%")
        table.add_row("Investments", f"₦{entry.investments:.2f}", f"{config.investments_pct*100:.0f}%")
        table.add_row("Discretionary", f"₦{entry.discretionary:.2f}", f"{config.discretionary_pct*100:.0f}%")
        
        console.print(table)
        console.print(f"\n[green]Saved successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error saving income: {e}[/red]")
    
    Prompt.ask("\nPress Enter to return to menu...")

def view_history_ui():
    print_header()
    entries = manager.get_history()
    
    if not entries:
        console.print("[yellow]No history found.[/yellow]")
    else:
        table = Table(title="Income History")
        table.add_column("Date", style="cyan")
        table.add_column("Total", style="green", justify="right")
        table.add_column("Savings", justify="right")
        table.add_column("Expenses", justify="right")
        table.add_column("Investments", justify="right")
        table.add_column("Discretionary", justify="right")
        
        for entry in entries:
            table.add_row(
                entry.date,
                f"₦{entry.amount:.2f}",
                f"₦{entry.savings:.2f}",
                f"₦{entry.expenses:.2f}",
                f"₦{entry.investments:.2f}",
                f"₦{entry.discretionary:.2f}"
            )
            
        console.print(table)
        
        # Summary stats
        stats = manager.get_monthly_stats()
        console.print(Panel(
            f"Total Income: ₦{stats['total_income']:.2f}\n"
            f"Total Savings: ₦{stats['total_savings']:.2f}\n"
            f"Number of Entries: {stats['entry_count']}",
            title="Summary Statistics"
        ))
        
    Prompt.ask("\nPress Enter to return to menu...")

def settings_ui():
    print_header()
    current = manager.config
    console.print(f"[bold]Current Settings:[/bold]")
    console.print(f"Savings: {current.savings_pct*100:.0f}%")
    console.print(f"Expenses: {current.expenses_pct*100:.0f}%")
    console.print(f"Investments: {current.investments_pct*100:.0f}%")
    console.print(f"Discretionary: {current.discretionary_pct*100:.0f}%")
    
    if Confirm.ask("\nDo you want to modify these percentages?"):
        console.print("\n[dim]Enter percentages as decimals (e.g. 0.30 for 30%)[/dim]")
        try:
            s = FloatPrompt.ask("Savings %")
            e = FloatPrompt.ask("Expenses %")
            i = FloatPrompt.ask("Investments %")
            d = FloatPrompt.ask("Discretionary %")
            
            if manager.update_settings(s, e, i, d):
                console.print("[green]Settings updated successfully![/green]")
            else:
                console.print("[red]Error: Percentages must sum to 1.0 (100%)[/red]")
        except ValueError:
             console.print("[red]Invalid input[/red]")
             
    Prompt.ask("\nPress Enter to return to menu...")

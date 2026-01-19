import sys
from rich.console import Console
from ui import display_menu, add_income_ui, view_history_ui, settings_ui
from rich.prompt import Prompt

def main():
    while True:
        display_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            add_income_ui()
        elif choice == "2":
            view_history_ui()
        elif choice == "3":
            settings_ui()
        elif choice == "4":
            print("Goodbye!")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit()

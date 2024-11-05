import time
from rich.console import Console
from rich.prompt import Prompt
from sessions.session import save_and_exit, start_break, start_work
from sessions.stats import view_daily_totals, view_logs
from ui.ui import display_menu

# Initialize Rich console
console = Console()

def main():
    """Main loop of the Work-Break Tracker."""
    while True:
        display_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="4")

        if choice == "1":
            start_work()
        elif choice == "2":
            start_break()
        elif choice == "3":
            view_logs()
        elif choice == "4":
            view_daily_totals()
        elif choice == "5":
            save_and_exit()
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user. Saving daily totals and exiting...[/bold red]")
        save_and_exit()
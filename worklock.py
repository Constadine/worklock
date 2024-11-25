import time
import sys
from rich.console import Console
from rich.prompt import Prompt
from sessions.session import  start_break, start_work
from ui.ui import display_menu, view_daily_totals, view_logs, settings_menu
from sessions.log_manager import calculate_daily_totals
# Initialize Rich console
console = Console()

def save_and_exit():
    """Saves daily totals and exits the program."""
    console.print("[bold blue]Saving daily totals...[/bold blue]")
    calculate_daily_totals()
    console.print("[bold green]Daily totals saved successfully.[/bold green]")
    console.print("[bold red]Exiting the Work-Break Tracker. Stay productive![/bold red]")
    sys.exit()

def main():
    """Main loop of the Work-Break Tracker."""
    while True:
        display_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5" ,"6"], default="1")

        if choice == "1":
            start_work()
        elif choice == "2":
            start_break()
        elif choice == "3":
            view_logs()
        elif choice == "4":
            view_daily_totals()
        elif choice == "5":
            settings_menu()
        elif choice == "6":
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

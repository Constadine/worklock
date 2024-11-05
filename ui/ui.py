# ui/ui.py

import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from settings.config import Settings

SESSION_LOG_FILE = Settings().session_log_file
DAILY_TOTALS_FILE = Settings().daily_totals_file

console = Console()
settings = Settings()
def display_menu():
    """Displays the main menu."""
    console.clear()
    table = Table(title=" -- Worklock 1.0 -- ", box=box.ROUNDED, style="cyan")
    table.add_column("Option", style="magenta", justify="center")
    table.add_column("Description", style="white")
    table.add_row("1", "Start Work Session")
    table.add_row("2", "Start Break Session")
    table.add_row("3", "View Session Logs")
    table.add_row("4", "View Daily Totals")
    table.add_row("5", "Settings")
    table.add_row("6", "Save and Exit")
    console.print(table)

def view_logs():
    """Displays all session logs."""
    if not os.path.exists(SESSION_LOG_FILE):
        console.print("[yellow]No session logs found.[/yellow]")
        Prompt.ask("Press Enter to return to the menu")
        return

    table = Table(title="Session Logs", box=box.MINIMAL_DOUBLE_HEAD, show_lines=True, style="green")
    table.add_column("Session Type", style="magenta")
    table.add_column("Start Time", style="cyan")
    table.add_column("End Time", style="cyan")
    table.add_column("Duration", style="yellow")

    with open(SESSION_LOG_FILE, "r") as f:
        for line in f:
            session_type, start, end, duration = line.strip().split(",")
            table.add_row(session_type, start, end, duration)

    console.print(table)
    Prompt.ask("Press Enter to return to the menu")

def view_daily_totals():
    """Displays daily totals from DAILY_TOTALS_FILE."""
    if not os.path.exists(DAILY_TOTALS_FILE):
        console.print("[yellow]No daily totals found.[/yellow]")
        Prompt.ask("Press Enter to return to the menu")
        return

    table = Table(title="Daily Totals", box=box.MINIMAL_DOUBLE_HEAD, show_lines=True, style="green")
    table.add_column("Date", style="cyan")
    table.add_column("Total Work", style="magenta")
    table.add_column("Total Break", style="magenta")
    table.add_column("Work Day Started", style="yellow")
    table.add_column("Work Day Ended", style="yellow")

    with open(DAILY_TOTALS_FILE, "r") as f:
        for line in f:
            date_str, total_work_str, total_break_str, start_time_str, end_time_str = line.strip().split(",")
            table.add_row(date_str, total_work_str, total_break_str, start_time_str, end_time_str)

    console.print(table)
    Prompt.ask("Press Enter to return to the menu")


def view_flavors():
    """Displays all available flavors and allows the user to select one."""
    
    # Display current flavor selection
    console.print(Panel(f"Current Flavor: [bold green]{settings.current_flavor.capitalize()}[/bold green]", 
                        title="Settings", border_style="green"))

    # Create a table to display all available flavors
    table = Table(title="Available Timer Flavors", box=box.ROUNDED, show_lines=True, style="white")
    table.add_column("Flavor", style="cyan", justify="center")
    table.add_column("Work Duration (min)", style="magenta", justify="center")
    table.add_column("Break Duration (min)", style="magenta", justify="center")
    table.add_column("Emoji", style="yellow", justify="center")
    table.add_column("Break Sound", style="green", justify="center")

    # Populate the table with each flavor's details
    for flavor_name, flavor_instance in settings.flavors.items():
        table.add_row(
            flavor_name.capitalize(),
            str(flavor_instance.work_duration),
            str(flavor_instance.break_duration),
            flavor_instance.emoji,
            flavor_instance.break_sound
        )

    console.print(table)

    # Let user pick a flavor
    flavor_choice = Prompt.ask("Enter the name of the flavor to select", choices=list(settings.flavors.keys()))
    settings.current_flavor = flavor_choice.lower()
    console.print(f"[bold green]Flavor set to {flavor_choice.capitalize()}[/bold green]\n")

    Prompt.ask("Press Enter to return to the menu")


def settings_menu():
    """Displays the settings menu with various options."""
    while True:
        console.clear()
        table = Table(title="Settings Menu", box=box.ROUNDED, show_lines=False, style="blue")
        table.add_column("Option", style="magenta", justify="center")
        table.add_column("Description", style="white")
        table.add_row("1", "Pick Flavor")
        table.add_row("2", "Set Theme [Placeholder]")
        table.add_row("3", "Adjust Timer Defaults [Placeholder]")
        table.add_row("4", "Back to Main Menu")
        console.print(table)

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            view_flavors()
        elif choice == "2":
            console.print("[yellow]Theme setting is a placeholder.[/yellow]")
            Prompt.ask("Press Enter to return to the settings menu")
        elif choice == "3":
            console.print("[yellow]Timer defaults adjustment is a placeholder.[/yellow]")
            Prompt.ask("Press Enter to return to the settings menu")
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            Prompt.ask("Press Enter to return to the settings menu")

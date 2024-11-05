import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box


SESSION_LOG_FILE = "session_logs.txt"
DAILY_TOTALS_FILE = "daily_totals.txt"

console = Console()

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
    




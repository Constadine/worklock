from rich.table import Table
from rich import box
from rich.console import Console

console = Console()

def display_menu() -> None:
    """Displays the main menu."""
    console.clear()
    table = Table(title=" -- Worklock 1.0 -- ", box=box.ROUNDED, style="cyan")
    table.add_column("Option", style="magenta", justify="center")
    table.add_column("Description", style="white")
    table.add_row("1", "Start Work Session")
    table.add_row("2", "Start Break Session")
    table.add_row("3", "View Session Logs")
    table.add_row("4", "View Daily Totals")
    table.add_row("5", "Save and Exit")
    console.print(table)
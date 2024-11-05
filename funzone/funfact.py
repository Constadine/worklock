from rich.panel import Panel
import subprocess
from rich.console import Console

console = Console()

def display_funfact():
    """Executes the funfact command and displays the output with rich formatting."""
    try:
        # The command from your alias
        command = "wget http://www.randomfunfacts.com -O - 2>/dev/null | grep '<strong>' | sed 's;^.*<i>\\(.*\\)</i>.*$;\\1;'"
        # Execute the command in the shell
        result = subprocess.run(command, capture_output=True, text=True, shell=True, executable='/bin/bash')
        if result.returncode == 0:
            fact = result.stdout.strip()
            # Use rich to display the fact nicely
            panel = Panel(fact, title="Fun Fact", title_align="left", style="green")
            console.print(panel)
        else:
            console.print("[red]Error getting fun fact.[/red]")
    except Exception as e:
        console.print(f"[red]Error running funfact command: {e}[/red]")
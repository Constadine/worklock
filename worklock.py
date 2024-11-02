import time
import sys
import os
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich import box
import subprocess

# Initialize Rich console
console = Console()

# Log file paths
SESSION_LOG_FILE = "session_logs.txt"
DAILY_TOTALS_FILE = "daily_totals.txt"

def log_session(session_type, start_time, end_time, duration):
    """Logs each session to SESSION_LOG_FILE."""
    with open(SESSION_LOG_FILE, "a") as f:
        f.write(f"{session_type},{start_time},{end_time},{duration}\n")

def send_notification(title, message, sound_source='system', sound_id=None):
    """Sends a desktop notification and plays a sound."""
    try:
        subprocess.run(["notify-send", title, message])
        # Play the specified system sound
        if sound_id and sound_source == 'system':
            subprocess.run(["canberra-gtk-play", "--id", sound_id])
        elif sound_id and sound_source == 'file':
            subprocess.run(["canberra-gtk-play", "--file", sound_id])
    except Exception as e:
        console.print(f"[red]Error sending notification: {e}[/red]")

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
    table.add_row("5", "Save and Exit")
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

    
def calculate_daily_totals():
    """Calculates and logs daily totals to DAILY_TOTALS_FILE."""
    if not os.path.exists(SESSION_LOG_FILE):
        return

    # Dictionary to store per-date totals and times
    daily_data = {}

    # Read existing sessions and accumulate work and break times per day
    with open(SESSION_LOG_FILE, "r") as f:
        for line in f:
            session_type, start_str, end_str, duration = line.strip().split(",")
            start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
            date_str = start_time.date().isoformat()
            h, m, s = map(int, duration.split(":"))
            duration_seconds = h * 3600 + m * 60 + s

            if date_str not in daily_data:
                daily_data[date_str] = {
                    'total_work': 0,
                    'total_break': 0,
                    'earliest_start_time': start_time,
                    'latest_end_time': end_time
                }
            # Update total work or break time
            if session_type.lower() == "work":
                daily_data[date_str]['total_work'] += duration_seconds
            elif session_type.lower() == "break":
                daily_data[date_str]['total_break'] += duration_seconds

            # Update earliest start time
            if start_time < daily_data[date_str]['earliest_start_time']:
                daily_data[date_str]['earliest_start_time'] = start_time

            # Update latest end time
            if end_time > daily_data[date_str]['latest_end_time']:
                daily_data[date_str]['latest_end_time'] = end_time

    # Write daily totals to DAILY_TOTALS_FILE
    with open(DAILY_TOTALS_FILE, "w") as f:
        for date_str, data in daily_data.items():
            total_work_str = str(timedelta(seconds=data['total_work']))
            total_break_str = str(timedelta(seconds=data['total_break']))
            start_time_str = data['earliest_start_time'].strftime("%H:%M:%S")
            end_time_str = data['latest_end_time'].strftime("%H:%M:%S")
            f.write(f"{date_str},{total_work_str},{total_break_str},{start_time_str},{end_time_str}\n")

def save_and_exit():
    """Saves daily totals and exits the program."""
    console.print("[bold blue]Saving daily totals...[/bold blue]")
    calculate_daily_totals()
    console.print("[bold green]Daily totals saved successfully.[/bold green]")
    console.print("[bold red]Exiting the Work-Break Tracker. Stay productive![/bold red]")
    sys.exit()

def timer(session_type, duration_minutes, auto_break=True):
    """Manages the countdown timer for sessions."""
    # Before starting the timer, if it's a break session, display funfact
    if session_type.lower() == "break":
        display_funfact()
    
    duration_seconds = duration_minutes * 60  # Corrected multiplication
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = ""

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        TextColumn("{task.completed:3.0f} / {task.total} seconds", justify="right"),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(f"{session_type} Time", total=duration_seconds)
        while not progress.finished:
            remaining = (end_time - datetime.now()).total_seconds()
            if remaining < 0:
                remaining = 0
            progress.update(task, completed=duration_seconds - remaining)
            time.sleep(1)

    end_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration_str = str(timedelta(seconds=duration_seconds))

    log_session(session_type, start_time_str, end_time_str, duration_str)

    # Send notification with a different sound based on session type
    if session_type.lower() == "work":
        sound_id = "sounds/bell.wav"
        send_notification(
            f"{session_type} Session Completed",
            f"Alright! Nice one. Time to rest bro.",
            sound_source='file',
            sound_id=sound_id
        )

    
    else:
        sound_id = "message-new-instant"
        send_notification(
            f"{session_type} Session Completed",
            f"Hope you used your break man. You really need those.",
            sound_id=sound_id
        )
    console.print(f"\n[bold green]{session_type} session completed![/bold green]")
    
    if session_type.lower() == "work" and auto_break:
        break_duration = IntPrompt.ask("Enter break duration in minutes", default=5)
        console.print(f"\n[bold blue]Starting break session for {break_duration} minutes...[/bold blue]")
        send_notification("Break Session Started", f"Your break session has started for {break_duration} minutes.")
        timer("Break", break_duration, auto_break=False)

        # Ask if user wants another break or continue with work
        poo_pile = 0
        while True:
            choice = Prompt.ask("Do you think you need another break? [y/n]", choices=["y", "n"], default="n")
            if choice.lower() == "y":
                if poo_pile == 0:
                    poo_pile += 1
                    message = "Sure!" + ":pile_of_poo:"*poo_pile + " How many minutes? "
                elif poo_pile == 1:
                    poo_pile += 1
                    message = "Ok!" + ":pile_of_poo:"*poo_pile + " How many minutes? "
                elif poo_pile < 4:
                    poo_pile *= 2
                    message = "You sure? " + ":pile_of_poo:"*poo_pile + " How many minutes now? "
                elif poo_pile  < 8:
                    poo_pile *= 3
                    console.print("[red]Wtf. WORKLOCK IS FULL OF POO, WORK MAN[/red]")
                    console.print(":pile_of_poo:"*poo_pile)
                    message = "Maybe you should be working? Please make it be the last one... How many minutes? "
                else:
                    poo_pile *= 2
                    console.print("[red]You are HOPELESS.[/red]")
                    console.print(":pile_of_poo:"*poo_pile)

                    message = "I don't care anymore."

                break_duration = IntPrompt.ask(message, default=3)

                timer("Break", break_duration, auto_break=False)
            elif choice.lower() == "n":
                break
            else:
                console.print("[red]Invalid choice. Please enter 'y' or 'n'.[/red]")

def start_work():
    """Starts a work session."""
    duration = IntPrompt.ask("Enter work duration in minutes", default=25)
    console.print(f"\n[bold blue]Starting Work Session for {duration} minutes...[/bold blue]")
    send_notification("Work Session Started", f"You have started a {duration}-minute work session.")
    timer("Work", duration)

def start_break():
    """Starts a break session."""
    duration = IntPrompt.ask("Enter break duration in minutes", default=5)
    console.print(f"\n[bold blue]Starting Break Session for {duration} minutes...[/bold blue]")
    send_notification("Break Session Started", f"You have started a {duration}-minute break session.")
    timer("Break", duration)

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

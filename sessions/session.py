from funzone.funfact import display_funfact
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from sessions.log_manager import log_session
import time
import sys
from sessions.log_manager import calculate_daily_totals
from notifications.notification import send_notification
from settings.config import Settings


console = Console()
settings = Settings()
flavor = settings.get_current_flavor()

def timer(session_type, duration_minutes, auto_break=True):
    """Manages the countdown timer for sessions."""
    # Before starting the timer, if it's a break session, display funfact
    if session_type.lower() == "break":
        display_funfact()
    
    duration_seconds = duration_minutes * 1  # Corrected multiplication
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
        sound_id = flavor.break_sound
        send_notification(
            f"{session_type} Session Completed",
            f"Alright! Nice one. Time to rest! {flavor.emoji}",
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
        break_duration = IntPrompt.ask("Enter break duration in minutes", default=flavor.break_duration)
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
    duration = IntPrompt.ask("Enter work duration in minutes", default=flavor.work_duration)
    console.print(f"\n[bold blue]Starting Work Session for {duration} minutes...[/bold blue]")
    send_notification("Work Session Started", f"You have started a {duration}-minute work session.")
    timer("Work", duration)

def start_break():
    """Starts a break session."""
    duration = IntPrompt.ask("Enter break duration in minutes", default=flavor.break_duration)
    console.print(f"\n[bold blue]Starting Break Session for {duration} minutes...[/bold blue]")
    send_notification("Break Session Started", f"You have started a {duration}-minute break session.")
    timer("Break", duration)


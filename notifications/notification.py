import os
import subprocess
from rich.console import Console

console = Console()

def send_notification(title, message, sound_source='system', sound_id=None):
    """Sends a desktop notification and plays a sound."""
    try:
        subprocess.run(["notify-send", title, message])
        if sound_id and sound_source == 'system':
            subprocess.run(["canberra-gtk-play", "--id", sound_id])
        elif sound_id and sound_source == 'file':
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(base_dir, sound_id)
            subprocess.run(["canberra-gtk-play", "--file", sound_path])
    except Exception as e:
        console.print(f"[red]Error sending notification: {e}[/red]")
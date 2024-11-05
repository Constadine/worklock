import os
from datetime import datetime, timedelta

# from dotenv import load_dotenv
# SESSION_LOG_FILE = load_dotenv()

SESSION_LOG_FILE = "session_logs.txt"
DAILY_TOTALS_FILE = "daily_totals.txt"

def log_session(session_type, start_time, end_time, duration):
    """Logs each session to SESSION_LOG_FILE."""
    with open(SESSION_LOG_FILE, "a") as f:
        f.write(f"{session_type},{start_time},{end_time},{duration}\n")


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
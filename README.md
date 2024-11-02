# Worklock

Worklock is a productivity application that helps you manage work and break sessions with desktop notifications, logs, and a fun fact during breaks. The application uses a terminal-based interface powered by Rich for a visually appealing and user-friendly experience.
# Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running Worklock](#running-worklock)
5. [Shortcut and Dock Access](#shortcut-and-dock-access)
6. [Uninstallation](#uninstallation)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

## Features

Track work and break sessions with logs saved to files for easy tracking. Receive desktop notifications for each session with customizable sounds. A fun fact during breaks to keep you entertained. Easily start, stop, and view logs in an organized menu. Optional shortcut creation for accessing the app from your applications menu or dock.

## Prerequisites

Make sure the following are installed on your system:

- Python 3 and pip – Python package installer.
- Virtualenv – For creating isolated Python environments. Install with:
```bash
pip install virtualenv
```

- libcanberra-gtk-module – For playing notification sounds (Linux only):
```bash
sudo apt-get install libcanberra-gtk-module libcanberra-gtk3-module
```
## Installation
##### Download and Navigate to Project Directory
Clone or download the project files from the repository. Then, navigate to the project directory:

```bash
cd /path/to/your_project_directory
```

##### Run Setup Script

Run the `setup.sh` script to automatically set up the virtual environment, install dependencies, and create a desktop shortcut.

```bash
chmod +x setup.sh
./setup.sh
```

##### Manual Installation (Optional)

If you prefer manual setup, follow these steps:
1. Create a Virtual Environment:

```bash
python3 -m venv venv
```
2. Activate the Virtual Environment:

```bash
source venv/bin/activate
```

3. Install Requirements:
```bash
pip install -r requirements.txt
```

4. Create a Desktop Shortcut (optional for dock access):

Create a .desktop file (instructions in the Shortcut and Dock Access section below).

## Running Worklock

Once installed, you can run Worklock in a few ways:
- From Applications Menu: Search for "Worklock" in your applications menu. Click to launch.
- From Dock: If you've pinned it to your dock, click to open.
- From Terminal:
```bash
    cd /path/to/your_project_directory
    source venv/bin/activate
    python work_tracker.py
```
## Shortcut and Dock Access
##### Creating a Desktop Shortcut Manually

If the setup script didn’t create a shortcut or you need to set it up manually:

1. Open a new file in a text editor:

```bash
nano ~/.local/share/applications/Worklock.desktop
```
2. Add the following content:

```ini
[Desktop Entry]
Version=1.0
Name=Worklock
Comment=Track work and break sessions with notifications
Exec=/path/to/your_project_directory/venv/bin/python /path/to/your_project_directory/worklock.py
Icon=/path/to/your_project_directory/icon.png  # Optional
Terminal=true
Type=Application
Categories=Utility;
```
3. Make Executable:
```bash
    chmod +x ~/.local/share/applications/Worklock.desktop
```

4. Pin to Dock: Open Worklock from the applications menu and pin it to your dock by right-clicking and selecting "Add to Favorites."

## Uninstallation

To uninstall Worklock:
- Remove the Project Directory:

```bash
rm -rf /path/to/your_project_directory
```
- Remove the Desktop Shortcut:
```bash
rm ~/.local/share/applications/Worklock
```
- Delete any Logs or Configurations (optional): Remove any log files or configurations generated by Worklock.

## Troubleshooting
##### Notifications or Sound Not Working

Ensure `libcanberra-gtk-module` is installed for sound notifications:

```bash
sudo apt-get install libcanberra-gtk-module libcanberra-gtk3-module
```
##### Shortcut Not Showing in Applications Menu
If you don’t see Worklock in the applications menu, try refreshing the desktop database:

```bash
xdg-desktop-menu forceupdate
```
##### Fun Fact Not Displaying
The fun fact feature requires internet access. Ensure your internet connection is active when starting a break session.
## License

This project is open-source and available under the MIT License.

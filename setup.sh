#!/bin/bash

# Define paths and variables
PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"
DESKTOP_FILE="$HOME/.local/share/applications/WorkTracker.desktop"
ICON_PATH="$PROJECT_DIR/icon.png"  # Optional: Change if you have an icon
SCRIPT_PATH="$PROJECT_DIR/work_tracker.py"

# Check for Python3 and virtualenv
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 before running this script."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip before running this script."
    exit 1
fi

# Step 1: Set up virtual environment
echo "Setting up virtual environment..."
python3 -m venv "$VENV_DIR"

# Step 2: Activate virtual environment and install requirements
source "$VENV_DIR/bin/activate"
echo "Installing required packages..."
pip install -r requirements.txt

# Step 3: Create .desktop file
echo "Creating application shortcut..."

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Worklock
Comment=Track work and break sessions with notifications
Exec=$VENV_DIR/bin/python $SCRIPT_PATH
Icon=$ICON_PATH
Terminal=true
Type=Application
Categories=Utility;
EOF

# Make the .desktop file executable
chmod +x "$DESKTOP_FILE"

echo "Shortcut created at $DESKTOP_FILE"

# Step 4: Check if icon file exists and update path in desktop file if needed
if [[ -f "$ICON_PATH" ]]; then
    echo "Icon found at $ICON_PATH"
else
    echo "No icon found. The shortcut will not have an icon."
    sed -i '/^Icon=/d' "$DESKTOP_FILE"  # Remove Icon line if no icon
fi

# Step 5: Finishing up
echo "Setup complete!"
echo "You can now launch Worklock from your applications menu or by searching 'Worklock'."
echo "To start the program manually, use:"
echo "  source $VENV_DIR/bin/activate"
echo "  python $SCRIPT_PATH"
echo "Or simply search 'Worklock' in your applications menu."

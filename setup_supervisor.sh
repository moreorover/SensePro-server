#!/bin/bash

# Install Supervisor if not already installed
if ! command -v supervisord &> /dev/null
then
    echo "Supervisor is not installed. Installing now..."
    sudo apt-get update
    sudo apt-get install -y supervisor build-essential python3-dev
    sudo pip install --no-cache-dir -r requirements.txt
else
    echo "Supervisor is already installed."
fi

# Create logs directory if it doesn't exist
LOG_DIR="/app/logs"
if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory: $LOG_DIR"
    sudo mkdir -p $LOG_DIR
    sudo chown root:root $LOG_DIR
    sudo chmod 755 $LOG_DIR
fi

# Path to the local supervisord.conf file (assuming it's in the same directory as this script)
LOCAL_CONFIG_FILE="./supervisord.config"
SUPERVISOR_CONFIG_PATH="/etc/supervisor/conf.d/supervisord.conf"

# Check if the supervisord.config file exists locally
if [ ! -f "$LOCAL_CONFIG_FILE" ]; then
    echo "Error: supervisord.config not found in the current directory."
    exit 1
fi

# Copy the supervisord.config file to the Supervisor configuration directory
echo "Copying supervisord.config to $SUPERVISOR_CONFIG_PATH"
sudo cp "$LOCAL_CONFIG_FILE" "$SUPERVISOR_CONFIG_PATH"

# Reload Supervisor to apply the new configuration
echo "Reloading Supervisor to apply the new configuration..."
sudo supervisorctl reread
sudo supervisorctl update

# Enable Supervisor to start at boot
echo "Enabling Supervisor to start at boot..."
sudo systemctl enable supervisor
sudo systemctl start supervisor

echo "Supervisor setup complete. Services should now be managed by Supervisor."

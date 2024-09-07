#!/bin/bash

# Install Docker using the convenience script
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Installing now..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installation complete. Rebooting now..."
    sudo reboot
else
    echo "Docker is already installed."
fi
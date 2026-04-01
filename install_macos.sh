#!/bin/bash

echo "=== Hashcash Installation Script for macOS ==="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing Python 3..."
    echo "Please install Homebrew first if you don't have it: https://brew.sh/"
    echo "Then run this script again."
    exit 1
fi

# Check if Homebrew is installed
if command -v brew &> /dev/null; then
    echo "Homebrew is installed. Proceeding with installation..."
else
    echo "Homebrew is not installed. It's recommended for installing dependencies."
    echo "Would you like to install Homebrew now? (y/n)"
    read answer
    if [ "$answer" == "y" ]; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Proceeding without Homebrew. Some dependencies might need to be installed manually."
    fi
fi

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

echo ""
echo "=== Installation complete! ==="
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python3 hashcash.py"
echo ""

# Make the script executable
chmod +x hashcash.py

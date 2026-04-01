# Hashcash - Cryptocurrency Mining CLI

## Overview

Hashcash is a command-line interface (CLI) application for cryptocurrency mining on the Base Sepolia network. It allows users to create wallets, mine $HASH tokens, claim rewards, and send tokens to other addresses.

## Features

- 💰 **Wallet Management**: Create and manage your cryptocurrency wallet
- ⛏️ **Mining**: Mine $HASH tokens using your computer's CPU
- 🪙 **Claim Rewards**: Claim your earned $HASH tokens
- 💸 **Send Tokens**: Transfer $HASH tokens to other addresses
- ⚙️ **Settings**: Configure mining parameters like CPU cores and RPC URL

## Requirements

- Python 3.8 or higher
- apt install python3.12-venv
- apt install python3-pip
- Internet connection
- **Important**: You need at least >0.01 ETH in your wallet to start mining

## Installation

### Windows

1. Clone or download this repository
2. Run the installation script:
   ```
   install_windows.bat
   ```
3. The script will install all required dependencies

### Ubuntu/Debian

1. Clone or download this repository
2. Make the installation script executable:
   ```
   chmod +x install_linux.sh
   ```
3. Run the installation script:
   ```
   ./install_linux.sh
   ```
4. The script will create a virtual environment and install all required dependencies

### macOS

1. Clone or download this repository
2. Make the installation script executable:
   ```
   chmod +x install_macos.sh
   ```
3. Run the installation script:
   ```
   ./install_macos.sh
   ```
4. The script will create a virtual environment and install all required dependencies

## Usage

### Starting the Application

Run the application with:

```
python hashcash.py
```

### First-time Setup

1. Select **Create Wallet** from the main menu
2. Follow the prompts to create a new wallet
3. Choose whether to save your wallet information to a file
4. Choose yes to update the `.env.local` file with your wallet information
5. **Important**: Fund your wallet with at least 0.001 ETH on the Base

### Mining

1. Select **Start Mining** from the main menu
2. The application will check your wallet balance (requires at least 0.001 ETH)
3. Mining rewards will be automatically submitted to the contract

### Claiming Rewards

1. Select **Claim $HASH** from the main menu
2. The application will show your pending rewards
3. Confirm to claim your rewards

### Sending Tokens

1. Select **Send $HASH** from the main menu
2. Enter the recipient's wallet address
3. Enter the amount of $HASH to send
4. Confirm the transaction

### Settings

1. Select **Settings** from the main menu
2. Configure the RPC URL and number of CPU cores for mining

## Configuration

The application uses a `.env.local` file for configuration. The following variables can be set:

- `PRIVATE_KEY`: Your wallet's private key (automatically set when creating a wallet)
- `MY_ADDRESS`: Your wallet address (automatically set when creating a wallet)
- `CPU_CORES`: Number of CPU cores to use for mining (default: 1)
- `RPC_URL`: URL of the RPC endpoint (default: https://sepolia.base.org)
- `CONTRACT_ADDRESS`: Address of the mining contract (do not change)
- `TOKEN`: Address of the $HASH token contract (do not change)

## Security Notes

- Never share your private key with anyone
- Back up your wallet information in a secure location
- The application stores your private key in the `.env.local` file, so keep this file secure

## Troubleshooting

- If you encounter RPC connection issues, try changing the RPC URL in the settings menu
- Make sure you have enough ETH in your wallet for transaction fees (minimum 0.001 ETH for mining)
- For mining issues, try reducing the number of CPU cores

## License

This project is open source and available under the MIT License.

## Disclaimer

Cryptocurrency mining and trading involve risk. This application is provided as-is with no guarantees. Use at your own risk.
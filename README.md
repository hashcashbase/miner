# 💙 Hashcash - Advanced cryptocurrency Mining CLI (v3.0.x)

## 🌟 Overview

Hashcash is a high-performance command-line interface (CLI) application for decentralized cryptocurrency mining on the **Base Sepolia** network. Version 3.0 introduces a gamified **Achievement NFT** system that rewards loyal miners with reduced fees and exclusive on-chain ranks.

## 🚀 Key Features

- 💰 **Wallet Management**: Seamlessly create or import Ethereum-compatible wallets.
- ⛏️ **Smart Mining**: Mine $HASH tokens using optimized CPU multi-threading.
- 🛡️ **Achievement NFT System**: 
    - 5 unique ranks (Stone Pickaxe to Giga Voyager).
    - **Dynamic Discounts**: Lower your `SUBMIT_FEE` by up to **99%** by holding higher-tier NFTs.
    - **On-chain Progress**: Track your rounds and rank up directly in the CLI.
- 🪙 **One-Click Rewards**: Easily claim your earned $HASH tokens from the mining pool.
- 💸 **Instant Transfers**: Send $HASH tokens to any address with built-in validation.
- ⚙️ **Advanced Settings**: Fine-tune CPU core usage and RPC endpoints for maximum efficiency.
- 🔄 **Auto-Updater**: Stay up to date with the latest features and security fixes.

## 📋 Requirements

- **Python**: 3.8 or higher.
- **System**: Windows, Linux (Ubuntu/Debian recommended), or macOS.
- **Dependencies**: `python3-venv`, `python3-pip`.
- **Wallet Balance**: At least **0.001 ETH** on Base Sepolia is required to cover transaction fees.

## 🛠️ Installation

### Windows
1. Download or clone this repository.
2. Run `install_windows.bat`.
3. The script handles all environment and dependency setups.

### Ubuntu / Debian / Linux
1. `chmod +x install_linux.sh`
2. `./install_linux.sh`
3. Activate environment: `source venv/bin/activate`

### macOS
1. `chmod +x install_macos.sh`
2. `./install_macos.sh`
3. Activate environment: `source venv/bin/activate`

## 🕹️ Usage

Run the main application:
```bash
python3 hashcash.py
```

### Main Menu Options

1. **💰 Create Wallet**: Generates a new private key and address. Saves details to `.env.local`.
2. **📥 Import Wallet**: Use your existing private key to mine from your main account.
3. **⛏️ Start Mining**: Begins the proof-of-work process.
    - *Note*: Bot automatically detects your NFT tier and applies discounted fees.
4. **🪙 Claim $HASH**: View and withdraw your pending rewards to your wallet.
5. **🛡️ Achievement NFT**: The hub for your mining career.
    - View total rounds participated.
    - Check current fee discount.
    - **Mint/Upgrade**: Reach required rounds and burn $HASH to ascend to the next Tier.
6. **💸 Send $HASH**: Transfer tokens to friends or other wallets.
7. **⚙️ Settings**: Change your RPC provider or adjust CPU core allocation.
8. **🔄 Check for Updates**: Pulls latest changes from the official repository.

## 🏆 Achievement Ranks (Tiers)

| Tier | Name | Target Rounds | $HASH Burn | Fee Discount |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Stone Pickaxe | 2,000 | 100 | 10% |
| 2 | Iron Miner | 10,000 | 1,000 | 25% |
| 3 | Golden Excavator | 25,000 | 10,000 | 50% |
| 4 | Diamond Driller | 50,000 | 15,000 | 75% |
| 5 | Giga Voyager | 100,000 | 25,000 | 99% |

## ⚙️ Configuration (.env.local)

While the CLI handles most settings, you can manually edit `.env.local`:
- `PRIVATE_KEY`: Your mining key.
- `CPU_CORES`: How many threads to use (default: 1).
- `RPC_URL`: Your preferred Base Sepolia RPC (default: https://sepolia.base.org).

## 🔒 Security & Safety

- **Private Keys**: Stored locally in your `.env.local`. Never share this file!
- **Gas Fees**: Mining involves on-chain transactions. Always ensure you have a small amount of ETH for gas.
- **Risk**: Use at your own risk. Digital assets can be volatile.

## 📄 License & Links

- **License**: MIT
- **Dashboard**: [Access the Web Dashboard](https://hashcash-dashboard.vercel.app)
- **Explorer**: [View Pool on BaseScan](https://sepolia.basescan.org/address/0x8C6bfe28b4B534a2fe0F3813c4c6571A476bd274)

---
*Mine smart, rank up, and dominate the Hashcash ecosystem!* ⛏️💎
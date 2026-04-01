import sys
import inquirer
import platform
from wallet import create_wallet, import_wallet
from claim import claim_rewards
from achievements import manage_achievements
from settings import update_settings
from mining import start_mining
from send_hash import send_hash
from config import VERSION, NETWORK
from updater import check_for_updates

# 📋 Hashcash CLI - Cryptocurrency Mining Application

def get_menu_choices():
    """🧩 Get menu choices based on platform"""
    # Check if running on Windows
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        # 🖥️ Windows version with emoji
        return [
            ("💰 Create Wallet", "wallet"),
            ("📥 Import Wallet", "import_wallet"),
            ("⛏️  Start Mining", "mine"),
            ("🪙  Claim $HASH", "claim"),
            ("🛡️  Achievement NFT", "achievements"),
            ("💸 Send $HASH", "send"),
            ("⚙️  Settings", "settings"),
            ("🔄 Check for Updates", "update"),
            ("🚪 Exit", "exit")
        ]
    else:
        # 🐧 Linux/macOS version with single spaces
        return [
            ("💰 Create Wallet", "wallet"),
            ("📥 Import Wallet", "import_wallet"),
            ("⛏️ Start Mining", "mine"),
            ("🪙 Claim $HASH", "claim"),
            ("🛡️ Achievement NFT", "achievements"),
            ("💸 Send $HASH", "send"),
            ("⚙️ Settings", "settings"),
            ("🔄 Check for Updates", "update"),
            ("🚪 Exit", "exit")
        ]

def main():
    """🚀 Main application entry point"""
    # Check for updates on startup
    check_for_updates(auto_update=False)
    
    while True:
        # Get menu choices based on platform
        menu_choices = get_menu_choices()
        is_windows = platform.system() == 'Windows'
        
        # 📝 Menu title
        menu_title = f"=== 💙 Hashcash Miner Menu - {NETWORK} v{VERSION} ===" 
        
        questions = [
            inquirer.List(
                "action",
                message=menu_title,
                choices=menu_choices
            )
        ]
        answer = inquirer.prompt(questions)
        if not answer:
            continue
        action = answer["action"]
        
        # 🔄 Route to the appropriate function based on user selection
        if action == "wallet":
            create_wallet()  # 💰 Create a new wallet
        elif action == "import_wallet":
            import_wallet()  # 📥 Import an existing wallet
        elif action == "mine":
            start_mining()   # ⛏️ Start mining process
        elif action == "claim":
            claim_rewards()  # 🪙 Claim mining rewards
        elif action == "achievements":
            manage_achievements() # 🛡️ Manage Achievement NFTs
        elif action == "send":
            send_hash()      # 💸 Send HASH tokens
        elif action == "settings":
            update_settings() # ⚙️ Update settings
        elif action == "update":
            check_for_updates() # 🔄 Check for updates
        elif action == "exit":
            print("👋 Exiting...")
            sys.exit(0)      # 🚪 Exit application

if __name__ == '__main__':
    main()
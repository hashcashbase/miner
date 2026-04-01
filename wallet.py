import secrets
from eth_account import Account
from utils import set_env_variable


def create_wallet():
    private_key = secrets.token_hex(32)
    account = Account.from_key(private_key)
    print(f"🔐 Private key: 0x{private_key}")
    print(f"🏦 Address: {account.address}")
    
    # Check if PRIVATE_KEY starts with 0x
    full_private_key = f"0x{private_key}"

    save = input("[?] Do you want to save the wallet to a file? (Y/n): ").strip().lower() or 'y'
    if save == 'y':
        filename = input("[?] Enter filename: ").strip() or "wallet.txt"
        if not filename.endswith(".txt"):
            filename += ".txt"
        with open(filename, "w") as f:
            f.write(f"Address: {account.address}\n")
            f.write(f"Private Key: {full_private_key}\n")
        print(f"✅ Wallet saved to {filename}")

    update = input("[?] Do you want to update .env.local with this wallet? (Y/n): ").strip().lower() or 'y'
    if update == 'y':
        set_env_variable("PRIVATE_KEY", full_private_key)
        set_env_variable("MY_ADDRESS", account.address)
        print("✅ .env.local updated!")


def import_wallet():
    """📥 Import an existing wallet by providing address and private key"""
    print("\n--- 📥 Import Wallet ---")
    address = input("[?] Enter your public Ethereum address (MY_ADDRESS): ").strip()
    if not address:
        print("❌ Address cannot be empty!")
        return

    private_key = input("[?] Enter your private key (starts with 0x): ").strip()
    if not private_key:
        print("❌ Private key cannot be empty!")
        return

    if not private_key.startswith('0x'):
        private_key = '0x' + private_key

    # Verification (optional but recommended)
    try:
        account = Account.from_key(private_key)
        if account.address.lower() != address.lower():
            print(f"⚠️ Warning: The private key provided corresponds to address {account.address}, not {address}.")
            confirm = input("[?] Do you want to continue anyway? (y/N): ").strip().lower()
            if confirm != 'y':
                return
    except Exception as e:
        print(f"❌ Error verifying private key: {e}")
        return

    set_env_variable("MY_ADDRESS", address)
    set_env_variable("PRIVATE_KEY", private_key)
    print("✅ .env.local updated with imported wallet!")
import os
import time
import platform
from dotenv import load_dotenv
from web3 import Web3
from config import TOKEN_ADDRESS, DEFAULT_RPC_URL

def send_hash():
    # Load environment variables
    load_dotenv(".env.local", override=True)
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    MY_ADDRESS = os.getenv("MY_ADDRESS")
    RPC_URL = os.getenv("RPC_URL", DEFAULT_RPC_URL)
    TOKEN = TOKEN_ADDRESS
    
    # Check if running on Windows for emoji display
    is_windows = platform.system() == 'Windows'
    
    # Check if wallet exists
    if not PRIVATE_KEY or not MY_ADDRESS:
        print("\n❌ No wallet found. Please create a wallet first.")
        return
    
    # Connect to Web3
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise Exception("❌ Could not connect to RPC")
    
    if is_windows:
        print("🚀 Connected to RPC!")
    else:
        print("🚀 Connected to RPC!")
    
    # Define basic ERC-20 ABI
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
            "name": "transfer",
            "outputs": [{"name": "success", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    
    # Create token contract
    token_contract = w3.eth.contract(address=w3.to_checksum_address(TOKEN), abi=ERC20_ABI)
    
    # Get balance and decimals
    decimals = token_contract.functions.decimals().call()
    raw_balance = token_contract.functions.balanceOf(MY_ADDRESS).call()
    formatted_balance = raw_balance / (10 ** decimals)
    
    if is_windows:
        print(f"💰 Your $HASH balance: {formatted_balance:.6f}")
    else:
        print(f"💰 Your $HASH balance: {formatted_balance:.6f}")
    
    if raw_balance == 0:
        if is_windows:
            print("⚠️  You don't have any $HASH tokens to send.")
        else:
            print("⚠️ You don't have any $HASH tokens to send.")
        return
    
    # Get destination and amount
    if is_windows:
        to = input("📬 Enter destination wallet address: ").strip()
        amount_str = input(f"💸 Enter amount to send (max {formatted_balance:.6f}): ").strip()
    else:
        to = input("📬 Enter destination wallet address: ").strip()
        amount_str = input(f"💸 Enter amount to send (max {formatted_balance:.6f}): ").strip()
    
    try:
        amount_float = float(amount_str)
    except ValueError:
        if is_windows:
            print("❌  Invalid amount.")
        else:
            print("❌ Invalid amount.")
        return
    
    if amount_float <= 0 or amount_float > formatted_balance:
        if is_windows:
            print("❌  Invalid amount.")
        else:
            print("❌ Invalid amount.")
        return
    
    amount_wei = int(amount_float * (10 ** decimals))
    
    # Get recipient's balance before transaction
    recipient_balance_before = token_contract.functions.balanceOf(w3.to_checksum_address(to)).call() / (10 ** decimals)
    
    # Confirm transaction
    if is_windows:
        print("\n📦 Summary:")
    else:
        print("\n📦 Summary:")
    print(f"→ To: {to}")
    print(f"→ Amount: {amount_float:.6f} $HASH")
    
    if is_windows:
        confirm = input("✅ Confirm sending? (y/n): ").strip().lower()
    else:
        confirm = input("✅ Confirm sending? (y/n): ").strip().lower()
    
    if confirm != 'y':
        if is_windows:
            print("❌  Aborted.")
        else:
            print("❌ Aborted.")
        return
    
    # Send transaction
    nonce = w3.eth.get_transaction_count(MY_ADDRESS)
    gas_price = int(w3.eth.gas_price * 1.1)
    
    tx = token_contract.functions.transfer(to, amount_wei).build_transaction({
        "from": MY_ADDRESS,
        "gas": 100_000,
        "gasPrice": gas_price,
        "nonce": nonce
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    if is_windows:
        print(f"🚀 Sending... TX hash: {w3.to_hex(tx_hash)}")
    else:
        print(f"🚀 Sending... TX hash: {w3.to_hex(tx_hash)}")
    
    # Wait for receipt
    if is_windows:
        print("⏳ Waiting for confirmation...")
    else:
        print("⏳ Waiting for confirmation...")
    
    while True:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                if is_windows:
                    print(f"✅ Transaction confirmed in block {receipt.blockNumber}!")
                else:
                    print(f"✅ Transaction confirmed in block {receipt.blockNumber}!")
                break
        except:
            pass
        time.sleep(3)
    
    # Wait 5 seconds and refresh balances
    if is_windows:
        print("🔄 Refreshing balances in 3 seconds...")
    else:
        print("🔄 Refreshing balances in 3 seconds...")
    time.sleep(3)
    
    # Get your updated balance
    raw_balance = token_contract.functions.balanceOf(MY_ADDRESS).call()
    formatted_balance = raw_balance / (10 ** decimals)
    if is_windows:
        print(f"💰 Your updated $HASH balance: {formatted_balance:.6f}")
    else:
        print(f"💰 Your updated $HASH balance: {formatted_balance:.6f}")
    
    # Get recipient's updated balance
    recipient_balance_after = token_contract.functions.balanceOf(w3.to_checksum_address(to)).call() / (10 ** decimals)
    if is_windows:
        print(f"📥 Recipient's $HASH balance: {recipient_balance_after:.6f} (+{recipient_balance_after - recipient_balance_before:.6f})")
    else:
        print(f"📥 Recipient's $HASH balance: {recipient_balance_after:.6f} (+{recipient_balance_after - recipient_balance_before:.6f})")

if __name__ == "__main__":
    send_hash()

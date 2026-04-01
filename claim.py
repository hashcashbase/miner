import os
import time
import platform
from dotenv import load_dotenv
from web3 import Web3
import json
from utils import set_env_variable
from config import CONTRACT_ADDRESS, TOKEN_ADDRESS, DEFAULT_RPC_URL

# Global variables that will be initialized in claim_rewards
PRIVATE_KEY = None
MY_ADDRESS = None
RPC_URL = None
TOKEN = TOKEN_ADDRESS
TOKEN_DECIMALS = 10**18
w3 = None
contract = None

# Define basic ERC-20 ABI for token balance check
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
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

def get_hash_balance(w3_instance):
    # Create token contract
    token_contract = w3_instance.eth.contract(address=w3_instance.to_checksum_address(TOKEN), abi=ERC20_ABI)
    
    # Get balance and decimals
    decimals = token_contract.functions.decimals().call()
    raw_balance = token_contract.functions.balanceOf(MY_ADDRESS).call()
    formatted_balance = raw_balance / (10 ** decimals)
    
    return formatted_balance

def claim_rewards():
    # Reload environment variables
    load_dotenv('.env.local', override=True)
    global PRIVATE_KEY, MY_ADDRESS, RPC_URL, TOKEN, w3, contract
    
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    MY_ADDRESS = os.getenv('MY_ADDRESS')
    RPC_URL = os.getenv('RPC_URL', DEFAULT_RPC_URL)
    
    # Reconnect to web3 with potentially updated RPC_URL
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print(f"\n❌ Cannot connect to RPC_URL: {RPC_URL}")
        return
    
    # Recreate contract with potentially updated CONTRACT_ADDRESS
    with open("HashcashMiningPoolABI.json", "r") as f:
        abi = json.load(f)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
    
    # Check if running on Windows for emoji display
    is_windows = platform.system() == 'Windows'
    
    # Check if wallet exists
    if not PRIVATE_KEY or not MY_ADDRESS:
        print("\n❌ No wallet found. Please create a wallet first.")
        return
        
    pending = contract.functions.pendingRewards(MY_ADDRESS).call()
    human = pending / TOKEN_DECIMALS
    
    if is_windows:
        print(f"💰 Pending rewards: {human:.6f} $HASH ({pending} raw units)")
    else:
        print(f"💰 Pending rewards: {human:.6f} $HASH ({pending} raw units)")

    if pending == 0:
        if is_windows:
            print("✅  Nothing to claim. Exiting.")
        else:
            print("✅ Nothing to claim. Exiting.")
        return

    if is_windows:
        answer = input(f"🔥 You have {human:.6f} $HASH pending. Claim now? (y/n): ").strip().lower()
    else:
        answer = input(f"🔥 You have {human:.6f} $HASH pending. Claim now? (y/n): ").strip().lower()
        
    if answer != 'y':
        if is_windows:
            print("❌  Claim cancelled by user.")
        else:
            print("❌ Claim cancelled by user.")
        return

    if is_windows:
        print("💸 Sending claimRewards()…")
    else:
        print("💸 Sending claimRewards()…")
    
    tx = contract.functions.claimRewards().build_transaction({
        "from": MY_ADDRESS,
        "gas": 200_000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(MY_ADDRESS),
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    if is_windows:
        print("🚀 claim tx:", w3.to_hex(tx_hash))
    else:
        print("🚀 claim tx:", w3.to_hex(tx_hash))

    timeout = time.time() + 120
    while time.time() < timeout:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                if is_windows:
                    print(f"✅ Claimed in block {receipt.blockNumber}")
                    print("🔄 Refreshing balance in 3 seconds...")
                else:
                    print(f"✅ Claimed in block {receipt.blockNumber}")
                    print("🔄 Refreshing balance in 3 seconds...")
                
                # Wait a moment for the blockchain to update the balance
                time.sleep(3)
                
                # Show current $HASH balance
                balance = get_hash_balance(w3)
                if is_windows:
                    print(f"💰 Current $HASH balance: {balance:.6f}")
                else:
                    print(f"💰 Current $HASH balance: {balance:.6f}")
                return
        except Exception:
            time.sleep(3)

    if is_windows:
        print("❌  Timeout waiting for claim receipt")
    else:
        print("❌ Timeout waiting for claim receipt")
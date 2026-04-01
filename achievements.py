import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv
from config import MINING_POOL_ADDRESS, ACHIEVEMENT_ADDRESS, TOKEN_ADDRESS, DEFAULT_RPC_URL

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Rank data mapping
TIERS = {
    1: {"name": "Stone Pickaxe", "rounds": 2000, "burn": 100, "discount": "10%"},
    2: {"name": "Iron Miner", "rounds": 10000, "burn": 1000, "discount": "25%"},
    3: {"name": "Golden Excavator", "rounds": 25000, "burn": 10000, "discount": "50%"},
    4: {"name": "Diamond Driller", "rounds": 50000, "burn": 15000, "discount": "75%"},
    5: {"name": "Giga Voyager", "rounds": 100000, "burn": 25000, "discount": "99%"}
}

def get_web3():
    rpc_url = os.getenv("RPC_URL", DEFAULT_RPC_URL)
    return Web3(Web3.HTTPProvider(rpc_url))

def manage_achievements():
    """🛡️ Achievement NFT Management Menu"""
    w3 = get_web3()
    my_address = os.getenv("MY_ADDRESS")
    private_key = os.getenv("PRIVATE_KEY")

    if not my_address or not private_key:
        print("❌ Wallet not configured. Please create or import a wallet first.")
        return

    # Load ABI (Simplified for our needs)
    # Using Pool ABI for sharesSubmitted and mintAchievement
    with open("HashcashMiningPoolABI.json", "r") as f:
        pool_abi = json.load(f)
    
    pool_contract = w3.eth.contract(address=MINING_POOL_ADDRESS, abi=pool_abi)

    print("\n--- 🛡️  Achievement NFT Status ---")
    
    # 1. Get current stats
    try:
        shares = pool_contract.functions.getSharesSubmitted(my_address).call()
        current_fee = pool_contract.functions.getEffectiveSubmitFee(my_address).call()
        
        # Check current tier via Pool (which checks NFT)
        # We need the NFT contract ABI for getHighestTier
        # For simplicity, we can also check balance in NFT contract
        # But let's use the Pool's view function logic
        
        # We'll just check balance and highest tier if possible
        # For now, let's show rounds and current discount based on fee
        base_fee = Web3.to_wei(0.000003, 'ether')
        discount_pct = (1 - (current_fee / base_fee)) * 100
        
        print(f"📊 Total Rounds Participated: {shares}")
        print(f"💰 Current Submit Fee: {Web3.from_wei(current_fee, 'ether'):.8f} ETH ({discount_pct:.0f}% Discount)")
        
        # Find next tier
        next_tier = 1
        for t in range(1, 6):
            if shares < TIERS[t]["rounds"]:
                next_tier = t
                break
            next_tier = t + 1
        
        if next_tier <= 5:
            t_data = TIERS[next_tier]
            progress = (shares / t_data["rounds"]) * 100
            print(f"\n🔜 Next Rank: {t_data['name']} (Tier {next_tier})")
            print(f"📈 Progress: [{('█' * int(progress//5)).ljust(20, ' ')}] {progress:.1f}%")
            print(f"📉 Requirements: {t_data['rounds']} rounds & {t_data['burn']} $HASH burn")
            
            # Action prompt
            print(f"\n[1] Mint/Upgrade to {t_data['name']}")
            print("[Q] Back to main menu")
            
            choice = input("\nSelect action: ").strip().lower()
            if choice == '1':
                if shares < t_data["rounds"]:
                    print(f"❌ Not enough rounds! You need {t_data['rounds'] - shares} more.")
                    return
                
                print(f"🔄 Preparing to mint {t_data['name']}...")
                confirm = input(f"⚠️  This will BURN {t_data['burn']} $HASH. Proceed? (y/n): ").lower()
                if confirm == 'y':
                    mint_achievement(w3, pool_contract, my_address, private_key, next_tier)
        else:
            print("\n🏆 Congratulations! You have reached the Maximum Rank (Giga Voyager)!")
            input("\nPress Enter to return...")

    except Exception as e:
        print(f"❌ Error fetching status: {str(e)}")

def mint_achievement(w3, pool_contract, my_address, private_key, tier):
    """🛠️  Execute Minting/Upgrading NFT"""
    try:
        print("⏳ Sending transaction...")
        nonce = w3.eth.get_transaction_count(my_address)
        
        # Build transaction
        tx = pool_contract.functions.mintAchievement(tier).build_transaction({
            'from': my_address,
            'nonce': nonce,
            'gasPrice': int(w3.eth.gas_price * 1.2) # 20% bump
        })
        
        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"🚀 Transaction sent! Hash: {tx_hash.hex()}")
        print("⏳ Waiting for confirmation...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print(f"\n🎉 SUCCESS! You have reached a new rank!")
            print("🛡️  Your NFT has been minted and discount is now active.")
        else:
            print("\n❌ Transaction failed. Check your $HASH balance.")
            
        input("\nPress Enter to return...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("\nPress Enter to return...")

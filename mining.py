import os
import json
import time
import concurrent.futures
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from decimal import Decimal
from tqdm import tqdm
from utils import set_env_variable
import platform
from config import CONTRACT_ADDRESS

from config import CONTRACT_ADDRESS, DEFAULT_RPC_URL, DEFAULT_CPU_CORES

# Global variables that will be initialized in start_mining
PRIVATE_KEY = None
MY_ADDRESS = None
RPC_URL = None
CPU_CORES = None
w3 = None
account = None
contract = None
SUBMIT_FEE = 0
ROUND_BLOCKS = 20


def mine_share(challenge: bytes, diff: int, start: int, step: int, my_address: str):
    from web3 import Web3 as LocalWeb3
    w3_local = LocalWeb3()
    nonce = start
    while True:
        digest = w3_local.solidity_keccak(['bytes32', 'address', 'uint256'], [challenge, my_address, nonce])
        if int(digest.hex(), 16) < diff:
            return nonce
        nonce += step


def start_mining():
    # Reload environment variables
    load_dotenv('.env.local', override=True)
    global PRIVATE_KEY, MY_ADDRESS, RPC_URL, CPU_CORES, w3, account, contract, SUBMIT_FEE
    
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    MY_ADDRESS = os.getenv('MY_ADDRESS')
    RPC_URL = os.getenv('RPC_URL', DEFAULT_RPC_URL)
    CPU_CORES = int(os.getenv('CPU_CORES', str(DEFAULT_CPU_CORES)))
    
    # Reconnect to web3 with potentially updated RPC_URL
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print(f"\n❌ Cannot connect to RPC_URL: {RPC_URL}")
        return
    
    # Recreate account with potentially updated PRIVATE_KEY
    account = None
    if PRIVATE_KEY:
        try:
            account = Account.from_key(PRIVATE_KEY)
        except Exception:
            print("❌ Invalid PRIVATE_KEY format in .env.local")
            return
    
    # Recreate contract with potentially updated CONTRACT_ADDRESS
    with open("HashcashMiningPoolABI.json") as f:
        abi = json.load(f)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
    
    # Check if wallet exists
    if not PRIVATE_KEY or not MY_ADDRESS:
        print("\n❌ No wallet found. Please create a wallet first.")
        return
        
    # Get dynamic submit fee (considering NFT discounts)
    try:
        SUBMIT_FEE = contract.functions.getEffectiveSubmitFee(MY_ADDRESS).call()
    except Exception:
        # Fallback to base fee if the function fails (e.g. older contract)
        SUBMIT_FEE = contract.functions.SUBMIT_FEE().call()
    
    # Check if running on Windows for emoji display
    is_windows = platform.system() == 'Windows'
        
    last_round = None
    round_start_block = None
    
    if is_windows:
        print("\n⛏️  Starting mining... (press Ctrl+C to stop and return to menu)")
        print(f"🌐 RPC URL: {RPC_URL}")
        print(f"💻 CPU Cores: {CPU_CORES}")
    else:
        print("\n⛏️ Starting mining... (press Ctrl+C to stop and return to menu)")
        print(f"🌐 RPC URL: {RPC_URL}")
        print(f"💻 CPU Cores: {CPU_CORES}")
    
    # Check ETH balance
    eth_balance = w3.eth.get_balance(MY_ADDRESS)
    eth_balance_ether = w3.from_wei(eth_balance, 'ether')
    submit_fee_ether = w3.from_wei(SUBMIT_FEE, 'ether')
    
    # Calculate how many mining rounds the current balance can pay for
    if SUBMIT_FEE > 0:
        rounds_possible = eth_balance // SUBMIT_FEE
    else:
        # If fee is 0 (very high discount), rounds are "unlimited" relative to fee
        rounds_possible = "Unlimited (Very low fee)"
    
    # Check pending rewards
    pending_rewards = contract.functions.pendingRewards(MY_ADDRESS).call()
    pending_rewards_formatted = pending_rewards / 10**18  # Assuming 18 decimals for the token
    
    # Display wallet info
    if is_windows:
        print("\n===  💰  Wallet Status ===")
        print(f"💰 ETH Balance: {eth_balance_ether:.6f} ETH")
        print(f"🧾 Effective Submit Fee: {submit_fee_ether:.8f} ETH per share")
        print(f"🔢 Rounds Possible: {rounds_possible}")
        print(f"🪙  Pending Rewards: {pending_rewards_formatted:.6f} $HASH")
    else:
        print("\n=== 💰 Wallet Status ===")
        print(f"💰 ETH Balance: {eth_balance_ether:.6f} ETH")
        print(f"🧾 Effective Submit Fee: {submit_fee_ether:.8f} ETH per share")
        print(f"🔢 Rounds Possible: {rounds_possible}")
        print(f"🪙 Pending Rewards: {pending_rewards_formatted:.6f} $HASH")
    
    # Check if balance is sufficient for mining
    MIN_ETH_REQUIRED = w3.to_wei(0.001, 'ether')
    if eth_balance < MIN_ETH_REQUIRED:
        print("\n❌ Insufficient ETH balance. You need at least 0.001 ETH to start mining.")
        return
    
    print("\n✅ Balance sufficient, starting mining process...")

    while True:
        try:
            current_round = contract.functions.getCurrentRound().call()
            challenge = contract.functions.challengeNumber().call()
            difficulty = contract.functions.difficulty().call()

            if last_round == current_round:
                if is_windows:
                    print("  Already submitted this round. Waiting...")
                else:
                    print("⏳ Already submitted this round. Waiting...")
                if round_start_block:
                    current_block = w3.eth.block_number
                    if current_block >= round_start_block + ROUND_BLOCKS:
                        if is_windows:
                            print(f"  {ROUND_BLOCKS} blocks passed, retrying tx...")
                        else:
                            print(f"⏱️ {ROUND_BLOCKS} blocks passed, retrying tx...")
                        last_round = None
                time.sleep(3)
                continue

            round_start_block = contract.functions.roundStartBlock().call()

            if current_round > 1:
                prev_round = current_round - 1
                miners = contract.functions.getMinersCount(prev_round).call()
                batch_miners_list = contract.functions.getBatchMiners(prev_round).call()
                batch_miners = len(batch_miners_list)
                is_batch_miner = MY_ADDRESS.lower() in [addr.lower() for addr in batch_miners_list]
                batch_miner_status = " (you are BatchMiner)" if is_batch_miner else ""
                round_reward = contract.functions.getRoundReward().call()
                miner_reward = round_reward * 95 // 100 // (miners if miners else 1)
                batch_reward = round_reward * 5 // 100 // (batch_miners if batch_miners else 1)

                if is_windows:
                    print(f"\n📊 Previous Round #{prev_round} stats:")
                    print(f"👷 Miners: {miners} | 🧺 BatchMiners: {batch_miners}{batch_miner_status}")
                    print(f"⛓️  Started at block: {round_start_block}")
                    print(f"💰 Miner reward: {miner_reward / 10**18:.4f} HASH")
                    print(f"🎁 Batch reward: {batch_reward / 10**18:.4f} HASH\n")
                else:
                    print(f"\n📊 Previous Round #{prev_round} stats:")
                    print(f"👷 Miners: {miners} | 🧺 BatchMiners: {batch_miners}{batch_miner_status}")
                    print(f"⛓️ Started at block: {round_start_block}")
                    print(f"💰 Miner reward: {miner_reward / 10**18:.4f} HASH")
                    print(f"🎁 Batch reward: {batch_reward / 10**18:.4f} HASH\n")

            if is_windows:
                print(f"\n=== ⛏️   Round {current_round} ===")
                print(f"🧩 Challenge: 0x{challenge.hex()}")
                print(f"🔒 Difficulty: {difficulty}\n")
            else:
                print(f"\n=== ⛏️  Round {current_round} ===")
                print(f"🧩 Challenge: 0x{challenge.hex()}")
                print(f"🔒 Difficulty: {difficulty}\n")

            start_time = time.time()
            with concurrent.futures.ProcessPoolExecutor(max_workers=CPU_CORES) as executor:
                futures = [executor.submit(mine_share, challenge, difficulty, i, CPU_CORES, MY_ADDRESS) for i in range(CPU_CORES)]
                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                nonce = done.pop().result()
                duration = time.time() - start_time
                if is_windows:
                    print(f"✅ Valid nonce found: {nonce} in {duration:.2f}s")
                else:
                    print(f"✅ Valid nonce found: {nonce} in {duration:.2f}s")

            gas_price = int(w3.eth.gas_price * 1.1)
            tx = contract.functions.submitShare(nonce).build_transaction({
                "from": MY_ADDRESS,
                "value": SUBMIT_FEE,
                "gas": 15_000_000,
                "gasPrice": gas_price,
                "nonce": w3.eth.get_transaction_count(MY_ADDRESS)
            })

            try:
                w3.eth.call(tx)
            except Exception as e:
                msg = str(e)
                if 'Already submitted' in msg:
                    if is_windows:
                        print("⚠️  Probably already submitted in this round. Wait for the next one.")
                    else:
                        print("⚠️ Probably already submitted in this round. Wait for the next one.")
                    last_round = current_round
                    continue
                if 'Invalid share' in msg:
                    if is_windows:
                        print("⚠️  Invalid share. Try again.")
                    else:
                        print("⚠️ Invalid share. Try again.")
                    continue
                if is_windows:
                    print(f"❌  Simulation error: {msg}")
                else:
                    print(f"❌ Simulation error: {msg}")
                continue

            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            if is_windows:
                print(f"🚀 submitShare tx: {w3.to_hex(tx_hash)}")
            else:
                print(f"🚀 submitShare tx: {w3.to_hex(tx_hash)}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            if is_windows:
                print(f"✅ Confirmed in block {receipt.blockNumber}")
            else:
                print(f"✅ Confirmed in block {receipt.blockNumber}")
            last_round = current_round
            
            # Update ETH balance after submitting
            eth_balance = w3.eth.get_balance(MY_ADDRESS)
            eth_balance_ether = w3.from_wei(eth_balance, 'ether')
            rounds_possible = eth_balance // SUBMIT_FEE if SUBMIT_FEE > 0 else 0
            if is_windows:
                print(f"💰 Remaining ETH: {eth_balance_ether:.6f} (for ~{rounds_possible} more rounds)")
            else:
                print(f"💰 Remaining ETH: {eth_balance_ether:.6f} (for ~{rounds_possible} more rounds)")
            
            # Check if balance is still sufficient
            if eth_balance < MIN_ETH_REQUIRED:
                if is_windows:
                    print("\n❌  ETH balance too low. Mining stopped.")
                else:
                    print("\n❌ ETH balance too low. Mining stopped.")
                return

        except KeyboardInterrupt:
            if is_windows:
                print("\n👋 Mining stopped. Returning to main menu...")
            else:
                print("\n👋 Mining stopped. Returning to main menu...")
            return
        except Exception as e:
            if is_windows:
                print(f"❌  Error: {e}")
            else:
                print(f"❌ Error: {e}")
            time.sleep(3)

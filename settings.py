import os
import inquirer
from dotenv import load_dotenv
from utils import set_env_variable
from config import DEFAULT_CPU_CORES, DEFAULT_RPC_URL

load_dotenv('.env.local')

RPC_URL       = os.getenv("RPC_URL", DEFAULT_RPC_URL)
CPU_CORES     = os.getenv("CPU_CORES", str(DEFAULT_CPU_CORES))

def update_settings():
    print("🎛️  Settings Menu\n")
    
    # Ask about RPC URL
    rpc_question = [
        inquirer.Text('rpc_url', message="🌐 RPC URL", default=RPC_URL)
    ]
    rpc_answer = inquirer.prompt(rpc_question)
    if not rpc_answer:
        return
    rpc_url = rpc_answer['rpc_url']
    
    # Ask about CPU cores
    cores_question = [
        inquirer.Text('cpu_cores', message="💻 CPU Cores for mining (1-16)", default=CPU_CORES)
    ]
    cores_answer = inquirer.prompt(cores_question)
    if not cores_answer:
        return
    
    # Validate CPU cores input
    try:
        cpu_cores = int(cores_answer['cpu_cores'])
        if cpu_cores < 1:
            cpu_cores = 1
        elif cpu_cores > 16:
            cpu_cores = 16
    except ValueError:
        cpu_cores = DEFAULT_CPU_CORES  # Default to configured default if invalid input
    
    # Save settings
    set_env_variable("RPC_URL", rpc_url)
    set_env_variable("CPU_CORES", str(cpu_cores))

    print("✅ Settings saved to .env.local")
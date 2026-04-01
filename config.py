"""
HashCash Configuration File

This file contains constants and configuration values used across the HashCash mining application.
These values should not be modified by users.
"""

# Contract Addresses (Base Sepolia)
MINING_POOL_ADDRESS = "0x8C6bfe28b4B534a2fe0F3813c4c6571A476bd274"
TOKEN_ADDRESS = "0xc9de6590b4a5505bEEbe7a64f2dA083F945Ce908"
ACHIEVEMENT_ADDRESS = "0x1d2C341BE79578A90209E750777498A4089BCeAc"

# Version information
VERSION = "3.0.0"
NETWORK = "testnet"

# Default values that can be overridden in .env.local
DEFAULT_CPU_CORES = 1
DEFAULT_RPC_URL = "https://sepolia.base.org"

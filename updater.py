import os
import time
import sys
import json
import shutil
import platform
import tempfile
import zipfile
from pathlib import Path
import subprocess
import requests
from dotenv import load_dotenv
from config import VERSION

GITHUB_REPO = "hashcashbase/miner"
GITHUB_BRANCH = "testnet"
UPDATE_EXCLUDE = ['.env.local', '__pycache__', 'test1', 'test2', 'contracts']
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"

def get_latest_version():
    """Check GitHub for the latest release version"""
    try:
        # You can either use releases API
        # response = requests.get(f"{GITHUB_API_URL}/releases/latest")
        # Or check the config.py file in the repository for VERSION
        # Bypass cache by adding a timestamp
        timestamp = int(time.time())
        response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/config.py?t={timestamp}")
        if response.status_code == 200:
            content = response.text
            for line in content.splitlines():
                if line.strip().startswith("VERSION"):
                    version = line.split("=")[1].strip().replace('"', '').replace("'", '')
                    return version
        return None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None

def download_update(version):
    """Download the latest version from GitHub"""
    try:
        url = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/{GITHUB_BRANCH}.zip"
        print(f"⬇️ Downloading update {version}...")
        
        # Download the zipfile
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"❌ Failed to download update: HTTP {response.status_code}")
            return None
            
        # Save to a temporary file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "update.zip")
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return zip_path
    except Exception as e:
        print(f"❌ Error downloading update: {e}")
        return None

def apply_update(zip_path):
    """Extract and apply the update"""
    try:
        temp_dir = os.path.dirname(zip_path)
        extract_dir = os.path.join(temp_dir, "extracted")
        
        # Extract the zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Find the first directory in the extracted content (should be the repo)
        repo_dir = None
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path):
                repo_dir = item_path
                break
                
        if not repo_dir:
            print("❌ Could not find repository directory in downloaded zip")
            return False
            
        # Now copy files from the extracted repo to our installation
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Back up .env.local
        env_path = os.path.join(current_dir, '.env.local')
        env_backup = None
        if os.path.exists(env_path):
            env_backup = os.path.join(temp_dir, '.env.local.backup')
            shutil.copy2(env_path, env_backup)
        
        # Copy new files, excluding those in UPDATE_EXCLUDE
        for root, dirs, files in os.walk(repo_dir):
            # Skip directories in exclude list
            dirs[:] = [d for d in dirs if d not in UPDATE_EXCLUDE]
            
            for file in files:
                # Skip files we shouldn't update
                if file in UPDATE_EXCLUDE:
                    continue
                    
                rel_path = os.path.relpath(os.path.join(root, file), repo_dir)
                src_path = os.path.join(root, file)
                dst_path = os.path.join(current_dir, rel_path)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
        
        # Restore .env.local
        if env_backup:
            shutil.copy2(env_backup, env_path)
            
        print(f"✅ Update to version {get_latest_version()} completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error applying update: {e}")
        return False
    finally:
        # Clean up temporary files
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

def check_for_updates(auto_update=False):
    """Check if there's a newer version available"""
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        print("\n🔄 Checking for updates...")
    else:
        print("\n🔄 Checking for updates...")
    
    latest_version = get_latest_version()
    
    if not latest_version:
        if is_windows:
            print("❓ Could not determine the latest version.")
        else:
            print("❓ Could not determine the latest version.")
        return False
    
    current_version = VERSION
    
    # Helper function to compare versions
    def is_newer(v_latest, v_current):
        try:
            l = [int(x) for x in v_latest.split('.')]
            c = [int(x) for x in v_current.split('.')]
            # Iterate up to the length of the version lists
            for i in range(max(len(l), len(c))):
                lv = l[i] if i < len(l) else 0
                cv = c[i] if i < len(c) else 0
                if lv > cv: return True
                if lv < cv: return False
            return False
        except:
            return v_latest != v_current # Fallback to simple comparison
            
    if not is_newer(latest_version, current_version):
        if is_windows:
            print(f"✅ You are running the latest version ({current_version}).")
        else:
            print(f"✅ You are running the latest version ({current_version}).")
        return False
    
    if is_windows:
        print(f"📢 Update available! Current: {current_version}, Latest: {latest_version}")
    else:
        print(f"📢 Update available! Current: {current_version}, Latest: {latest_version}")
    
    if auto_update:
        return update_now()
    
    # Ask if the user wants to update
    while True:
        if is_windows:
            choice = input("📥 Do you want to update now? (y/n): ").strip().lower()
        else:
            choice = input("📥 Do you want to update now? (y/n): ").strip().lower()
        
        if choice == 'y':
            return update_now()
        elif choice == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def update_now():
    """Perform the update"""
    is_windows = platform.system() == 'Windows'
    
    latest_version = get_latest_version()
    zip_path = download_update(latest_version)
    
    if not zip_path:
        if is_windows:
            print("❌ Update failed: Could not download update package.")
        else:
            print("❌ Update failed: Could not download update package.")
        return False
    
    success = apply_update(zip_path)
    
    if success:
        if is_windows:
            print("\n🚀 Update successful! The application will restart.")
        else:
            print("\n🚀 Update successful! The application will restart.")
        
        # Restart the application
        python = sys.executable
        subprocess.run([python, "hashcash.py"])
        sys.exit(0)
    else:
        if is_windows:
            print("❌ Update failed. Please try again later.")
        else:
            print("❌ Update failed. Please try again later.")
        return False

if __name__ == "__main__":
    check_for_updates()

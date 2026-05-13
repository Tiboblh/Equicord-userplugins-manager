import os
import zipfile
import sys
import shutil, glob
import subprocess

print("[LOG] Checking for equicord...")
if not os.path.exists("equicord"):
    print("[LOG] Cloning equicord repository...")
    os.system("git clone https://github.com/equicord/equicord")
    os.makedirs("equicord/src/userplugins", exist_ok=True)
else:
    print("[LOG] Equicord found. Checking for updates...")
    # Check current equicord version
    current_version = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd="equicord").decode().strip()
    # Get latest equicord version
    latest_version = subprocess.check_output(["git", "ls-remote", "origin", "HEAD"], cwd="equicord").decode().split()[0]
    if current_version != latest_version:
        if platform.system() == "Windows":
            print("[LOG] Updating equicord to the latest version...")
            os.system("move equicord\\src\\userplugins userplugins_backup")
            os.system("rmdir /s /q equicord")
            os.system("git clone https://github.com/equicord/equicord")
            os.system("move userplugins_backup equicord\\src\\userplugins")
        else:
            print("[LOG] Updating equicord to the latest version...")
            os.system("mv equicord/src/userplugins userplugins_backup")
            os.system("rm -rf equicord")
            os.system("git clone https://github.com/equicord/equicord")
            os.system("mv userplugins_backup equicord/src/userplugins")

print("[LOG] Killing Discord...")
if platform.system() == "Windows":
    os.system("taskkill /f /im Discord.exe")
    os.system("cd equicord && pnpm install && pnpm build && echo '0' | pnpm inject")
else:
    os.system("killall -9 Discord")
    os.system("cd equicord && pnpm install && pnpm build && echo '0' | pnpm inject")
print("[LOG] Equicord injected successfully.")
print("[LOG] Restarting Discord...")
subprocess.Popen(
    ['discord'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True
)
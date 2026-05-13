import os
import zipfile
import sys
import shutil, glob
import subprocess
import platform

path = input("Enter the path of a zip file, a directory or a github repository: ")
name = input("Enter the name of the plugin: ")
if os.path.isfile(path) and path.endswith('.zip'):
    print("[LOG] Extracting zip file...")
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("extracted")
    path = "extracted"
elif os.path.isdir(path):
    print("[LOG] Using directory...")
elif path.startswith("https://github.com/"):
    print("[LOG] Cloning github repository...")
    os.system(f"git clone {path} equicord_plugin")
    path = "equicord_plugin"

if not os.path.exists(path + "/index.ts") and not os.path.exists(path + "/index.tsx"):
    print("[LOG] No index.ts or index.tsx file found in the directory.")
    sys.exit(1)
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
os.makedirs("equicord/src/userplugins/" + name, exist_ok=False)
for f in glob.glob(path + "/*"):
    shutil.move(f, "equicord/src/userplugins/" + name + "/")
print("[LOG] Plugin moved to equicord/src/userplugins/" + name + "/")
if platform.system() == "Windows":
    os.system("taskkill /f /im Discord.exe")
else:
    os.system("killall -9 Discord")
os.system("cd equicord && pnpm install && pnpm build && echo '0' | pnpm inject")
os.system("rm -rf " + path)
print("[LOG] Plugin installed successfully.")
print("[LOG] Restarting Discord...")
subprocess.Popen(
    ['discord'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True
)

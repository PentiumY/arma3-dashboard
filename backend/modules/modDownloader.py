# steam_mod_downloader.py

import subprocess
import os
import shutil
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

STEAM_USER = os.getenv("STEAM_USER")
STEAM_PASS = os.getenv("STEAM_PASS")
CURRENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "modsManifest.json"
)

SERVER_PATH = os.path.join("/home/arma/arma3server")

def find_mod_dirs():
    """
    Scan `base_dir` for subdirectories that contain both 'mod.cpp' and 'meta.cpp'.
    
    Args:
        base_dir (str): The path to scan.
    
    Returns:
        List[str]: List of subdirectory names that meet the criteria.
    """
    valid_dirs = []

    # Iterate over all entries in base_dir
    for entry in os.listdir(SERVER_PATH):
        full_path = os.path.join(SERVER_PATH, entry)

        # Check if it is a directory
        if os.path.isdir(full_path):
            # Check if both mod.cpp and meta.cpp exist in the directory
            mod_file = os.path.join(full_path, "mod.cpp")
            meta_file = os.path.join(full_path, "meta.cpp")
            if os.path.isfile(mod_file) and os.path.isfile(meta_file):
                valid_dirs.append(entry)  # store just the directory name

    return valid_dirs

def get_workshop_mod_name(workshop_id: int) -> str:
    """
    Fetch the name/title of a Steam Workshop mod.

    Args:
        workshop_id (int): The Steam Workshop mod ID.

    Returns:
        str: The mod title.
    """
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    data = {"itemcount": 1, "publishedfileids[0]": workshop_id}
    response = requests.post(url, data=data)
    response.raise_for_status()
    r = response.json()
    return r["response"]["publishedfiledetails"][0]["title"]


def download_workshop_mod(
    workshop_id: int,
    server_path: str = "/home/arma/arma3server",
    steamcmd_path: str = "/home/arma/steamcmd/steamcmd.sh",
    steam_library: str = "/home/arma/Steam"
) -> str:
    """
    Download a Steam Workshop mod via SteamCMD and copy it to the Arma 3 server folder.

    Args:
        workshop_id (int): The Steam Workshop mod ID.
        server_path (str): Path to the Arma 3 server directory.
        steamcmd_path (str): Path to SteamCMD executable.
        steam_library (str): Path to Steam library where mods are downloaded.

    Returns:
        str: Path to the copied mod in the server folder.
    """
    if not STEAM_USER or not STEAM_PASS:
        raise ValueError("Steam credentials not found in environment variables.")

    env = os.environ.copy()
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'

    mod_name = get_workshop_mod_name(workshop_id)

    # Step 1: Download via SteamCMD
    cmd = [
        steamcmd_path,
        "+login", STEAM_USER, STEAM_PASS,
        "+workshop_download_item", "107410", str(workshop_id), "validate",
        "+quit"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError(f"SteamCMD failed to download workshop mod {workshop_id}")

    # Step 2: Copy to Arma 3 server folder
    src = os.path.join(steam_library, "steamapps", "workshop", "content", "107410", str(workshop_id))
    dest = os.path.join(server_path, f"@{mod_name}")

    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)



    print(f"Copied Workshop mod '{mod_name}' to server folder: {dest}")
    return dest


# Optional: allow running as a script
if __name__ == "__main__":
    mods = find_mod_dirs()
    print(mods)

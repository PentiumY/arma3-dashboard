import subprocess
import os

def download_workshop_mod(workshop_id, server_path="/home/arma3server", steamcmd_path="/home/arma/steamcmd/steamcmd.sh"):
    cmd = [
        steamcmd_path,                # full path to steamcmd.sh
        "+login", "anonymous",
        "+force_install_dir", server_path,
        "+workshop_download_item", "107410", str(workshop_id), "validate",
        "+quit"
    ]
    subprocess.run(cmd)

download_workshop_mod(463939057)
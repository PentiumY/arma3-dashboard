import subprocess
import os

def download_workshop_mod(workshop_id, server_path="/home/arma3server", steamcmd_path="/home/arma/steamcmd/steamcmd.sh"):
    env = os.environ.copy()
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'

    cmd = [
        steamcmd_path,
        "+force_install_dir", server_path,   # MUST come before login
        "+login", "anonymous",
        "+workshop_download_item", "107410", str(workshop_id), "validate",
        "+quit"
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    return proc.returncode

# Example usage
download_workshop_mod(463939057)

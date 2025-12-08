import subprocess, os, shutil, requests

def getWorkshopModName(workshop_id):
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    data = {"itemcount": 1, "publishedfileids[0]": workshop_id}
    response = requests.post(url, data=data)
    r = response.json()
    name = r["response"]["publishedfiledetails"][0]["title"]
    return name

def downloadWorkshopMod(workshop_id, server_path="/home/arma/arma3server", steamcmd_path="/home/arma/steamcmd/steamcmd.sh"):
    env = os.environ.copy()
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'

    steam_library = "/home/arma/Steam"
    mod_name = getWorkshopModName(workshop_id)

    # Step 1: Download via SteamCMD
    cmd = [
        steamcmd_path,
        "+login", "annalunda", "Laserbrain42",
        "+workshop_download_item", "107410", str(workshop_id), "validate",
        "+quit"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()

    # Step 2: Copy to Arma 3 server folder
    src = os.path.join(steam_library, "steamapps", "workshop", "content", "107410", str(workshop_id))
    dest = os.path.join(server_path, f"@{mod_name}")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"Copied Workshop mod {mod_name} to server folder: {dest}")

# Example usage
downloadWorkshopMod(3441837719)

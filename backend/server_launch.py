import subprocess, os

def launchArma3Server(
    server_path="/home/arma/arma3server",
    arma_exe="arma3server_x64",
    profile="profile1",
    config_file="server.cfg",
    port=2302,
    mods=None,
    steamcmd_path="/home/arma/steamcmd/steamcmd.sh"
):
    """
    Launch an Arma 3 server.

    - server_path: folder where arma3server_x64 is located
    - profile: profile folder name (for saved configs)
    - config_file: server.cfg filename
    - port: server port
    - mods: list of mod folder names (e.g., ['@ACE3', '@CBA_A3'])
    """

    env = os.environ.copy()
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'

    exe_path = os.path.join(server_path, arma_exe)
    if not os.path.exists(exe_path):
        print(f"ERROR: {exe_path} does not exist")
        return

    # Build -mod argument
    mod_string = ""
    if mods:
        mod_string = "-mod=" + ";".join(mods)

    cmd = [
        exe_path,
        f"-config={config_file}",
        f"-profiles={os.path.join(server_path, profile)}",
        f"-port={port}",
    ]
    if mod_string:
        cmd.append(mod_string)

    # Launch the server
    print(f"Launching Arma 3 server with command:\n{' '.join(cmd)}\n")
    
    # Popen will keep the server running
    proc = subprocess.Popen(cmd, cwd=server_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

    # Stream output
    try:
        for line in proc.stdout:
            print(line, end="")
    except KeyboardInterrupt:
        print("Server terminated by user")
        proc.terminate()

    proc.wait()
    print(f"Arma 3 server exited with code {proc.returncode}")
    return proc.returncode

launchArma3Server()
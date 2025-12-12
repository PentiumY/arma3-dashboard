from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from modules.modDownloader import download_workshop_mod as installMod

app = FastAPI()

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# CORS setup from environment
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
# Split comma-separated origins into a list and strip spaces
origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint to check status
@app.get("/status")
def get_status():
    return {"status": "running"}


# Background worker to install mods
def background_install_mods(mods):
    for mod in mods:
        workshop_id = mod.get("workshopId")
        if workshop_id:
            try:
                print(f"Installing mod {mod['name']} (ID: {workshop_id})...")
                installMod(int(workshop_id))  # Calls your module function
                print(f"Finished installing {mod['name']}")
            except Exception as e:
                print(f"Failed to install {mod['name']} ({workshop_id}): {e}")


@app.post("/upload")
async def upload_modlist(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # Read file contents
    contents = await file.read()
    html = contents.decode("utf-8", errors="ignore")

    # Parse HTML/XML
    soup = BeautifulSoup(html, "lxml")

    mods = []

    # Find all <tr data-type="ModContainer">
    rows = soup.find_all("tr", {"data-type": "ModContainer"})

    for row in rows:
        name_el = row.find("td", {"data-type": "DisplayName"})
        link_el = row.find("a", {"data-type": "Link"})
        source_el = row.find("span")

        if not name_el:
            continue

        name = name_el.text.strip()
        source = source_el.text.strip() if source_el else None
        url = link_el["href"] if link_el else None

        # extract workshop ID if present
        workshopId = None
        if url and "id=" in url:
            workshopId = url.split("id=")[-1]

        mods.append({
            "name": name,
            "source": source,
            "url": url,
            "workshopId": workshopId
        })

    # Start background task to install mods
    if background_tasks:
        background_tasks.add_task(background_install_mods, mods)

    return JSONResponse({
        "status": "ok",
        "modCount": len(mods),
        "mods": mods,
        "message": "Mod installation started in the background"
    })

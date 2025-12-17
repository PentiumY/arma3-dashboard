from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from modules.modDownloader import download_workshop_mod as installMod
from modules.modDownloader import find_mod_dirs as getAllMods
import json
from typing import Dict, Any
from pydantic import BaseModel
import random

app = FastAPI()

fakeMods = [
            {"name": "ace", "filesize": 100},
            {"name": "cats", "filesize": 100},
            {"name": "dogs", "filesize": 100}
        ]

PRESETS_FILE = os.path.join(os.path.dirname(__file__), "presets.json")
CURRENT_FILE = os.path.join(os.path.dirname(__file__), "current.json")

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env.development")
load_dotenv(dotenv_path=env_path)

# CORS setup from environment
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
# Split comma-separated origins into a list and strip spaces
origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

environment = os.getenv("ENVIRONMENT", "development")

class PresetSaveRequest(BaseModel):
    name: str
    data: dict

class PresetPayload(BaseModel):
    name: str

class ModlistUpdateRequest(BaseModel):
    modlist: list[str]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_presets() -> Dict[str, Any]:
    if not os.path.exists(PRESETS_FILE):
        return {}

    with open(PRESETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_presets(presets: Dict[str, Any]):
    with open(PRESETS_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=4)

def get_current_preset():
    if not os.path.exists(CURRENT_FILE):
        return None
    with open(CURRENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("current")

def set_current_preset(name: str):
    with open(CURRENT_FILE, "w", encoding="utf-8") as f:
        json.dump({"current": name}, f, indent=4)

# Endpoint to check status
@app.get("/status")
def get_status():
    return {"status": "running"}

@app.get("/presets")
def get_presets():
    PRESETS = load_presets()
    return list(PRESETS.keys())

@app.get("/presets/{selected_preset}")
async def get_preset(selected_preset: str):
    PRESETS = load_presets()
    preset = PRESETS.get(selected_preset)

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    return preset

@app.get("/presets/{selected_preset}/modlist")
async def get_preset_modlist(selected_preset: str):
    PRESETS = load_presets()
    preset = PRESETS.get(selected_preset)

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # Ensure modlist always exists
    modlist = preset.get("modlist", [])
    
    return modlist

@app.post("/presets/{selected_preset}/modlist")
async def set_preset_modlist(selected_preset: str, payload: ModlistUpdateRequest):
    presets = load_presets()
    preset = presets.get(selected_preset)

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # Update only the modlist
    preset["modlist"] = payload.modlist
    presets[selected_preset] = preset

    save_presets(presets)

    return {
        "status": "ok",
        "message": f"Modlist for preset '{selected_preset}' updated",
        "modlist": preset["modlist"]
    }

@app.post("/save")
def save_settings(payload: PresetSaveRequest):
    presets = load_presets()

    # Ensure payload has a modlist key
    if "modlist" not in payload.data:
        payload.data["modlist"] = []

    if payload.name in presets:
        # Merge existing preset with incoming data
        existing = presets[payload.name]
        merged = {**existing, **payload.data}

        # Ensure modlist is always present
        if "modlist" not in merged:
            merged["modlist"] = []

        presets[payload.name] = merged
    else:
        # New preset
        presets[payload.name] = payload.data

    save_presets(presets)
    set_current_preset(payload.name)

    return {
        "status": "ok",
        "message": f"Preset '{payload.name}' saved or merged"
    }

@app.get("/current")
def getcurrent():
    return get_current_preset()

@app.get("/allMods")
def getmods():
    if environment == "production":
        return getAllMods()
    else:
        return fakeMods
    
        
@app.post("/setCurrent")
def setcurrent(payload: PresetPayload):
    set_current_preset(payload.name)

# Background worker to install mods
def background_install_mods(mods):
    currentMods = []
    if environment == "production":
        currentMods = getAllMods()

    for mod in mods:
        mod_name = mod.get("name")
        workshop_id = mod.get("workshopId")

        if environment == "production":
            if mod_name in currentMods:
                print(f"Skipping mod '{mod_name}' (already installed)")
                continue

            if workshop_id:
                try:
                    print(f"Installing mod {mod_name} (ID: {workshop_id})...")
                    installMod(int(workshop_id))  # Your actual installation function
                    print(f"Finished installing {mod_name}")
                except Exception as e:
                    print(f"Failed to install {mod_name} ({workshop_id}): {e}")
        else:
            # Check if a fake mod with the same name already exists
            if any(fm["name"] == mod_name for fm in fakeMods):
                print(f"Skipping fake mod '{mod_name}' (already exists)")
                continue

            fake_mod = {
                "name": mod_name,
                "filesize": random.randint(1, 10000)  # size in MB, for example
            }
            fakeMods.append(fake_mod)
            print("Added fake mod:", fake_mod)


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

    fake_mods = []
    for mod in mods:
        fake_mods.append(mod["name"])

    return JSONResponse({
        "status": "ok",
        "modCount": len(mods),
        "mods": mods,
        "modlist": fake_mods,
        "message": "Mod installation started in the background"
    })

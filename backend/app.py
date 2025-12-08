from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI()

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

raw_origins = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

print(origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    return {"status": "running"}


@app.post("/upload")
async def upload_modlist(file: UploadFile = File(...)):
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

    return JSONResponse({
        "status": "ok",
        "modCount": len(mods),
        "mods": mods
    })

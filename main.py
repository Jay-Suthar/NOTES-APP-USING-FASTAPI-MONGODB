from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conn = MongoClient("mongodb+srv://jay_prekshit_2001:grsuthar_shachi_javi_avi_2001@cluster0.ewpmu.mongodb.net")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    notedocs = []
    for doc in docs:
        notedocs.append({
            "id": doc["_id"],
            "note": doc["note"]
        })
    return templates.TemplateResponse(
        request=request, name="index.html", context={"notedocs": notedocs}
    )

from fastapi import APIRouter, HTTPException
from config.db import conn
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    notedocs = []
    for doc in docs:
        notedocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
        })
    return templates.TemplateResponse(
        request=request, name="index.html", context={"notedocs": notedocs}
    )


@note.post("/")
async def add_item(request: Request):

    try:
        form = await request.form()
        dictf = dict(form)
        notex = conn.notes.notes.insert_one(dictf)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error adding item: {e}")
    return RedirectResponse(url="/", status_code=303)


@note.post("/delete/{item_id}")
async def delete_item(item_id: str):

    try:
        conn.notes.notes.delete_one({"_id": ObjectId(item_id)})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error deleting item: {e}")
    return RedirectResponse(url="/", status_code=303)
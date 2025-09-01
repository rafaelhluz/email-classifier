from typing import Optional
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from app.model import classify_and_generate
from app.utils import parse_pdf_text
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class EmailRequest(BaseModel):
    email_text: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/classify")
async def classify_email_endpoint(
    email_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not email_text and not file:
        return JSONResponse(status_code=400, content={"error": "Nenhum texto ou arquivo fornecido."})

    text = email_text
    if file:
        if file.content_type == 'application/pdf':
            text = await parse_pdf_text(file.file)
        else:
            text = (await file.read()).decode("utf-8")
    
    result = await classify_and_generate(text)
    
    return {
        "category": result["category"],
        "response": result["response"],
        "email_text": text,
        "characters_processed": len(text)
    }
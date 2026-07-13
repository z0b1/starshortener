from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from prisma import Prisma
import random
import string
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

db = Prisma()

@app.on_event("startup")
async def startup():
    await db.connect()
@app.on_event("shutdown")
async def shutdown():
    if db.is_connected():
        await db.disconnect()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# --- UI Page ---
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    # Fix: Wrap parameters explicitly inside the context keyword argument
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}
    )

# --- Action: Shorten Link ---
@app.post("/shorten", response_class=HTMLResponse)
async def create_short_url(request: Request, long_url: str = Form(...)):
    # ... your existing short code generation and db write logic stays here ...
    
    base_url = str(request.base_url)
    full_short_url = f"{base_url}{short_code}"
    
    # Fix: Wrap parameters explicitly inside the context keyword argument
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "short_url": full_short_url,
            "long_url": long_url
        }
    )


@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):

    record = await db.url.find_unique(where={"shortCode": short_code})

    if record:
        return RedirectResponse(record.longUrl, status_code = 307)
    
    raise HTTPException(status_code=404, detail="Short URL not found")
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from prisma import Prisma
import random
import string
import os

app = FastAPI()

# Absolute path tracking for Vercel
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
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}
    )

# --- Action: Shorten Link ---
@app.post("/shorten", response_class=HTMLResponse)
async def create_short_url(request: Request, long_url: str = Form(...)):
    # 1. Generate the unique code string
    short_code = generate_short_code()
    
    # 2. Check the database for rare code collisions
    existing = await db.url.find_unique(where={"shortCode": short_code})
    while existing:
        short_code = generate_short_code()
        existing = await db.url.find_unique(where={"shortCode": short_code})
        
    # 3. Save the entry to your Serverless Neon Postgres database
    await db.url.create(
        data={
            "shortCode": short_code,
            "longUrl": long_url
        }
    )
    
    # 4. Construct the complete short URL path
    base_url = str(request.base_url)
    full_short_url = f"{base_url}{short_code}"
    
    # 5. Send data cleanly to your Jinja2 template
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "short_url": full_short_url,
            "long_url": long_url
        }
    )

# --- Action: Redirect ---
@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    # Fetch from database
    record = await db.url.find_unique(where={"shortCode": short_code})

    if record:
        return RedirectResponse(record.longUrl, status_code=307)
    
    raise HTTPException(status_code=404, detail="Short URL not found")

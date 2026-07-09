from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

app = FastAPI()

# Пути к файлам
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "index.html"

# Тестовые данные
WORKS_DB = [
    {
        "id": 1,
        "title": "Утро в деревне",
        "technique": "Масло, холст · 40×50 см",
        "price": 18000,
        "description": "Тёплое летнее утро",
        "image_url": "https://picsum.photos/seed/1/400/400",
        "is_available": 1
    },
    {
        "id": 2,
        "title": "Старый маяк",
        "technique": "Акварель · 30×40 см",
        "price": 12000,
        "description": "Маяк на берегу",
        "image_url": "https://picsum.photos/seed/2/400/400",
        "is_available": 1
    },
    {
        "id": 3,
        "title": "Портрет незнакомки",
        "technique": "Уголь, бумага · 25×35 см",
        "price": 9500,
        "description": "Загадочный портрет",
        "image_url": "https://picsum.photos/seed/3/400/400",
        "is_available": 1
    }
]

@app.get("/")
async def root():
    """Отдаёт сайт"""
    try:
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except:
        return HTMLResponse(content="<h1>Site loading...</h1>")

@app.get("/api/works")
async def get_works():
    return JSONResponse(WORKS_DB)

@app.get("/api/about")
async def get_about():
    return JSONResponse({
        "name": "Мария",
        "tagline": "Винтажная живопись",
        "description": "Работаю с маслом и акварелью"
    })

@app.post("/api/contact")
async def post_contact():
    return JSONResponse({"status": "ok"})
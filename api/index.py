from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import os

@app.get("/")
async def root():
    # Читаем index.html и возвращаем его
    html_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# База данных (пока тестовые данные)
WORKS_DB = [
    {
        "id": 1,
        "title": "Утро в деревне",
        "technique": "Масло, холст · 40×50 см",
        "price": 18000,
        "description": "Тёплое летнее утро в русской деревне",
        "image_url": "https://picsum.photos/seed/1/400/400",
        "is_available": 1
    },
    {
        "id": 2,
        "title": "Старый маяк",
        "technique": "Акварель · 30×40 см",
        "price": 12000,
        "description": "Маяк на берегу северного моря",
        "image_url": "https://picsum.photos/seed/2/400/400",
        "is_available": 1
    },
    {
        "id": 3,
        "title": "Портрет незнакомки",
        "technique": "Уголь, бумага · 25×35 см",
        "price": 9500,
        "description": "Загадочный портрет в классическом стиле",
        "image_url": "https://picsum.photos/seed/3/400/400",
        "is_available": 1
    }
]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Maria Art API", "status": "ok"}


@app.get("/api/works")
async def get_works():
    return JSONResponse(WORKS_DB)


@app.get("/api/works/{work_id}")
async def get_work(work_id: int):
    work = next((w for w in WORKS_DB if w["id"] == work_id), None)
    if work:
        return JSONResponse(work)
    return JSONResponse({"error": "Work not found"}, status_code=404)


@app.get("/api/about")
async def get_about():
    about = {
        "name": "Мария",
        "tagline": "Винтажная живопись и графика",
        "description": "Работаю с маслом, акварелью и тушью. Вдохновляюсь северными пейзажами и старой архитектурой. Каждая картина — это маленькая история, которую я рассказываю цветом и линией.",
        "contacts": {
            "telegram": "https://t.me/your_bot",
            "avito": "https://avito.ru/user/your_id",
            "email": "maria@example.com"
        }
    }
    return JSONResponse(about)


@app.post("/api/contact")
async def post_contact(request: Request):
    data = await request.json()
    # Здесь можно добавить отправку уведомления админу
    print(f"New contact message: {data}")
    return JSONResponse({"status": "ok", "message": "Message received"})


@app.get("/api/stats")
async def get_stats():
    total = len(WORKS_DB)
    available = sum(1 for w in WORKS_DB if w.get("is_available", 0) == 1)
    return JSONResponse({
        "total_works": total,
        "available": available,
        "sold": total - available
    })
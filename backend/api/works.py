from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Здесь должна быть логика получения работ из БД
# Пока вернём тестовые данные
@app.get("/api/works")
async def get_works():
    works = [
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
        }
    ]
    return JSONResponse(works)

@app.get("/api/works/{work_id}")
async def get_work(work_id: int):
    work = {
        "id": work_id,
        "title": f"Работа {work_id}",
        "technique": "Масло, холст",
        "price": 15000,
        "description": "Описание",
        "image_url": f"https://picsum.photos/seed/{work_id}/400/400",
        "is_available": 1
    }
    return JSONResponse(work)

@app.get("/api/about")
async def get_about():
    about = {
        "name": "Мария",
        "tagline": "Винтажная живопись и графика",
        "description": "Работаю с маслом, акварелью и тушью. Вдохновляюсь северными пейзажами и старой архитектурой.",
        "contacts": {
            "telegram": "https://t.me/your_bot",
            "avito": "https://avito.ru/user/your_id",
            "email": "maria@example.com"
        }
    }
    return JSONResponse(about)

@app.post("/api/contact")
async def post_contact():
    return JSONResponse({"status": "ok"})
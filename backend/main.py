from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Artwork
from models import ArtworkCreate, ArtworkUpdate, ArtworkResponse, ContactForm

app = FastAPI(
    title="Мария. Арт API",
    description="API для портфолио художника Марии",
    version="1.0.0"
)

# Разрешаем запросы с сайта (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в продакшене указать домен сайта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── РАБОТЫ ───────────────────────────────────────────────

@app.get("/api/works", response_model=List[ArtworkResponse])
def get_works(available_only: bool = False, db: Session = Depends(get_db)):
    """Получить список работ (для сайта и бота)"""
    query = db.query(Artwork)
    if available_only:
        query = query.filter(Artwork.is_available == 1)
    return query.order_by(Artwork.id.desc()).all()


@app.get("/api/works/{work_id}", response_model=ArtworkResponse)
def get_work(work_id: int, db: Session = Depends(get_db)):
    """Получить одну работу по ID"""
    work = db.query(Artwork).filter(Artwork.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    return work


@app.post("/api/works", response_model=ArtworkResponse)
def create_work(work: ArtworkCreate, db: Session = Depends(get_db)):
    """Добавить новую работу (для админа / бота)"""
    db_work = Artwork(**work.model_dump())
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


@app.put("/api/works/{work_id}", response_model=ArtworkResponse)
def update_work(work_id: int, work: ArtworkUpdate, db: Session = Depends(get_db)):
    """Обновить работу"""
    db_work = db.query(Artwork).filter(Artwork.id == work_id).first()
    if not db_work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    for key, value in work.model_dump(exclude_unset=True).items():
        setattr(db_work, key, value)
    db.commit()
    db.refresh(db_work)
    return db_work


@app.delete("/api/works/{work_id}")
def delete_work(work_id: int, db: Session = Depends(get_db)):
    """Удалить работу"""
    db_work = db.query(Artwork).filter(Artwork.id == work_id).first()
    if not db_work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    db.delete(db_work)
    db.commit()
    return {"message": "Работа удалена"}


# ─── О ХУДОЖНИКЕ ──────────────────────────────────────────

@app.get("/api/about")
def get_about():
    """Информация о художнике"""
    return {
        "name": "Мария",
        "tagline": "Винтажная живопись и графика",
        "description": (
            "Работаю с маслом, акварелью и тушью. "
            "Вдохновляюсь северными пейзажами и старой архитектурой. "
            "Каждая картина — это маленькая история, "
            "которую я рассказываю цветом и линией."
        ),
        "contacts": {
            "telegram": "https://t.me/your_bot",
            "avito": "https://avito.ru/user/your_id",
            "email": "maria@example.com"
        }
    }


# ─── ФОРМА СВЯЗИ ─────────────────────────────────────────

@app.post("/api/contact")
def send_contact(form: ContactForm):
    """Получить заявку от посетителя сайта"""
    # Здесь можно:
    # - сохранить в БД
    # - отправить уведомление в Telegram через бота
    # - отправить на email
    print(f"📩 Новая заявка: {form.name} <{form.email}>")
    print(f"   Сообщение: {form.message}")
    if form.artwork_id:
        print(f"   Интересует работа ID: {form.artwork_id}")
    return {"message": "Сообщение отправлено. Мария скоро ответит!"}


# ─── СТАТТИСТИКА (для бота) ───────────────────────────────

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Статистика для бота"""
    total = db.query(Artwork).count()
    available = db.query(Artwork).filter(Artwork.is_available == 1).count()
    sold = total - available
    return {
        "total_works": total,
        "available": available,
        "sold": sold
    }


# ─── ЗАПУСК ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
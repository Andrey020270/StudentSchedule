from app import db, app
import models  # важно: импортируем, чтобы SQLAlchemy "увидел" модели

with app.app_context():
    db.create_all()
    print("База данных создана успешно.")

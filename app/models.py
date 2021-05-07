from datetime import datetime


from app import db


class Task(db.Model):
    """Модель ссылки на конкретную страницу"""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512))
    image = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    save_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.id}:{self.url}'

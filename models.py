from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Nota {self.id} {self.titulo}>"

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Nota

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'unison-secreto'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    integrante = "Maria Galaviz"
    return render_template('index.html', integrante=integrante)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()

        if not titulo or not contenido:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('create_note'))

        nueva = Nota(titulo=titulo, contenido=contenido)
        db.session.add(nueva)
        db.session.commit()
        flash("Nota creada con éxito", "success")
        return redirect(url_for('list_notes'))
    
    return render_template('crear-nota.html')

@app.route('/notes')
def list_notes():
    notas = Nota.query.all()
    return render_template('lista-notas.html', notas=notas)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    nota = Nota.query.get_or_404(id)

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()

        if not titulo or not contenido:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('edit_note', id=id))

        nota.titulo = titulo
        nota.contenido = contenido
        db.session.commit()
        flash("Nota actualizada", "success")
        return redirect(url_for('list_notes'))

    return render_template('editar-nota.html', nota=nota)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_note(id):
    nota = Nota.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(nota)
        db.session.commit()
        flash("Nota eliminada", "success")
        return redirect(url_for('list_notes'))

    return render_template('confirmar-eliminar.html', nota=nota)

if __name__ == '__main__':
    app.run(debug=True)

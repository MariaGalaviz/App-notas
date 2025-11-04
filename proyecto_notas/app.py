from flask import Flask, render_template, request, redirect, url_for, g
from model import ManejadorDeNotas, Nota

app = Flask(__name__)
DATABASE = 'notasBD.sqlite'

def get_db():
    if 'db' not in g:
        g.db = ManejadorDeNotas(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.cerrar()

@app.route('/')
@app.route('/index')
def index():
  
    return render_template('index.html')

@app.route('/listar')
def listar_notas():
   
    manejador = get_db()
    lista_de_notas = manejador.leer_todas_las_notas()
    return render_template('listar_notas.html', notas=lista_de_notas)

@app.route('/crear_nota', methods=['GET', 'POST'])
def crear_nota():
 
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        
        if not titulo:
            return redirect(url_for('crear_nota'))
            
        manejador = get_db()
        manejador.crear_nota(titulo, contenido)
        
        return redirect(url_for('listar_notas'))
        
    return render_template('crear_nota.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_nota_ruta(id):
   
    manejador = get_db()
    
    if request.method == 'POST':
        titulo_actualizado = request.form['titulo']
        contenido_actualizado = request.form['contenido']
        
        nota_actualizada = Nota(
            id=id,
            titulo=titulo_actualizado,
            contenido=contenido_actualizado
        )
        manejador.actualizar_nota(nota_actualizada)
        
        return redirect(url_for('listar_notas'))
    
    nota_existente = manejador.leer_nota(id)
    if nota_existente is None:
        return redirect(url_for('listar_notas'))
        
    return render_template('editar_nota.html', nota=nota_existente)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_nota_ruta(id):

    manejador = get_db()
    manejador.eliminar_nota(id)
    
    return redirect(url_for('listar_notas'))

if __name__ == '__main__':
    app.run(debug=True)
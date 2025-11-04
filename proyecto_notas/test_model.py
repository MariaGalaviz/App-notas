import pytest
import sqlite3
import os
from model import ManejadorDeNotas, Nota

DB_TEST = 'notasTestBD.sqlite'

@pytest.fixture
def manejador_de_prueba():

    conn = sqlite3.connect(DB_TEST)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT
        )
    """)
    cursor.execute("DELETE FROM notas") 
    conn.commit()
    conn.close()

    manejador = ManejadorDeNotas(db_name=DB_TEST)
    
    yield manejador 
    
    manejador.cerrar()



def test_crear_nota(manejador_de_prueba):
    nuevo_id = manejador_de_prueba.crear_nota("Test Titulo", "Test Contenido")
    
    assert nuevo_id is not None
    
    conn = sqlite3.connect(DB_TEST)
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, contenido FROM notas WHERE id = ?", (nuevo_id,))
    fila = cursor.fetchone()
    conn.close()
    
    assert fila[0] == "Test Titulo"
    assert fila[1] == "Test Contenido"

def test_leer_nota(manejador_de_prueba):
    conn = sqlite3.connect(DB_TEST)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (titulo, contenido) VALUES (?, ?)", 
                   ("Leer Titulo", "Leer Contenido"))
    id_insertado = cursor.lastrowid
    conn.commit()
    conn.close()

    nota_leida = manejador_de_prueba.leer_nota(id_insertado)

    assert nota_leida.id == id_insertado
    assert nota_leida.titulo == "Leer Titulo"
    assert nota_leida.contenido == "Leer Contenido"

def test_actualizar_nota(manejador_de_prueba):
    conn = sqlite3.connect(DB_TEST)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (titulo, contenido) VALUES (?, ?)", 
                   ("Original", "Original"))
    id_insertado = cursor.lastrowid
    conn.commit()
    conn.close()

    nota_para_actualizar = Nota(
        id=id_insertado,
        titulo="Actualizado",
        contenido="Actualizado"
    )
    manejador_de_prueba.actualizar_nota(nota_para_actualizar)

    conn_verif = sqlite3.connect(DB_TEST)
    cursor_verif = conn_verif.cursor()
    cursor_verif.execute("SELECT titulo, contenido FROM notas WHERE id = ?", (id_insertado,))
    fila = cursor_verif.fetchone()
    conn_verif.close()

    assert fila[0] == "Actualizado"
    assert fila[1] == "Actualizado"

def test_eliminar_nota(manejador_de_prueba):
    conn = sqlite3.connect(DB_TEST)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (titulo, contenido) VALUES (?, ?)", 
                   ("Borrar", "Borrar"))
    id_insertado = cursor.lastrowid
    conn.commit()
    conn.close()

    manejador_de_prueba.eliminar_nota(id_insertado)

    conn_verif = sqlite3.connect(DB_TEST)
    cursor_verif = conn_verif.cursor()
    cursor_verif.execute("SELECT * FROM notas WHERE id = ?", (id_insertado,))
    fila = cursor_verif.fetchone()
    conn_verif.close()

    assert fila is None
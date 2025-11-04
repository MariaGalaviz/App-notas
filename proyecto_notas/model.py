import sqlite3

class Nota:
   
    def __init__(self, id, titulo, contenido):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido

    def __repr__(self):
        return f"<Nota id={self.id} titulo='{self.titulo}'>"

class ManejadorDeNotas:

    def __init__(self, db_name='notasBD.sqlite'):
       
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self._crear_tabla()

    def _crear_tabla(self):
       
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT
            )
        """)
        self.conn.commit()

    def cerrar(self):
        self.conn.close()


    def crear_nota(self, titulo, contenido):
      
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO notas (titulo, contenido) VALUES (?, ?)", 
            (titulo, contenido)
        )
        self.conn.commit()
        return cursor.lastrowid
    def leer_nota(self, id):
     
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notas WHERE id = ?", (id,))
        fila = cursor.fetchone()
        
        if fila:
            return Nota(id=fila[0], titulo=fila[1], contenido=fila[2])
        else:
            return None

    def leer_todas_las_notas(self):
     
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notas ORDER BY id DESC")
        filas = cursor.fetchall()
        
        return [Nota(id=f[0], titulo=f[1], contenido=f[2]) for f in filas]

    def actualizar_nota(self, nota):
      
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE notas SET titulo = ?, contenido = ? WHERE id = ?",
            (nota.titulo, nota.contenido, nota.id)
        )
        self.conn.commit()

    def eliminar_nota(self, id):
      
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notas WHERE id = ?", (id,))
        self.conn.commit()
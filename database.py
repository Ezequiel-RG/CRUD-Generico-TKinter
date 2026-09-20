import sqlite3

class BaseDatos:
    def __init__(self, db_name="concesionaria.db"):
        self.db_name = db_name

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self, nombre_tabla, campos):
        columnas = ", ".join([f"{col} TEXT" for col in campos])
        query = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columnas})"
        with self.conectar() as conn:
            conn.execute(query)

    def obtener_todos(self, nombre_tabla):
        query = f"SELECT * FROM {nombre_tabla}"
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def insertar(self, nombre_tabla, campos, valores):
        cols = ", ".join(campos)
        placeholders = ", ".join(["?"] * len(valores))
        query = f"INSERT INTO {nombre_tabla} ({cols}) VALUES ({placeholders})"
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            return cursor.lastrowid

    def actualizar(self, nombre_tabla, campos, valores, id_registro):
        set_clause = ", ".join([f"{col} = ?" for col in campos])
        query = f"UPDATE {nombre_tabla} SET {set_clause} WHERE id = ?"
        with self.conectar() as conn:
            conn.execute(query, valores + [id_registro])

    def eliminar(self, nombre_tabla, id_registro):
        query = f"DELETE FROM {nombre_tabla} WHERE id = ?"
        with self.conectar() as conn:
            conn.execute(query, (id_registro,))
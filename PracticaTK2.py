import tkinter as tk
from tkinter import ttk, messagebox
from database import BaseDatos

class CRUDGenerico:
    def __init__(self, contenedor, campos, nombre_tabla):
        self.contenedor = contenedor
        self.campos = campos
        self.nombre_tabla = nombre_tabla
        self.entradas = {}
        
        self.db = BaseDatos()
        self.db.crear_tabla(self.nombre_tabla, list(self.campos.keys()))
        
        f_base = len(self.campos)  
              
        boton_crear = tk.Button(self.contenedor, text="Crear", command=self.crear_registro)
        boton_crear.grid(row=f_base, column=0, pady=10)
        
        boton_borrar = tk.Button(self.contenedor, text='Borrar', command=self.borrar_registro)
        boton_borrar.grid(row=f_base, column=1, pady=10)

        boton_actualizar = tk.Button(self.contenedor, text='Actualizar', command=self.actualizar_registro)
        boton_actualizar.grid(row=f_base, column=2, pady=10)
        
        tabla = ttk.Treeview(self.contenedor, columns=list(self.campos.keys()), show="headings", height=5)
        tabla.grid(row=f_base + 1, column=0, columnspan=3, padx=5, pady=5)
        self.tabla = tabla
        
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_registro)

        for indice, (clave, texto_label) in enumerate(self.campos.items()):
            etiqueta = tk.Label(self.contenedor, text=texto_label)
            campo = tk.Entry(self.contenedor)
            etiqueta.grid(row=indice, column=0, padx=5, pady=2, sticky="e")
            campo.grid(row=indice, column=1, padx=5, pady=2)
            self.entradas[clave] = campo
            self.tabla.heading(clave, text=texto_label)
            self.tabla.column(clave, width=110)

        self.cargar_datos()

    def cargar_datos(self):
        registros = self.db.obtener_todos(self.nombre_tabla)
        for fila in registros:
            id_registro = fila[0]
            valores = fila[1:]
            self.tabla.insert("", "end", iid=id_registro, values=valores)

    def seleccionar_registro(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            for indice, clave in enumerate(self.entradas.keys()):
                campo = self.entradas[clave]
                campo.delete(0, tk.END)
                campo.insert(0, valores[indice])
                
    def crear_registro(self):
        datos = self.obtener_datos_entradas()
        
        if self.validar_campos_vacios(datos):
            return
        
        nuevo_id = self.db.insertar(self.nombre_tabla, list(self.campos.keys()), datos)
        
        self.tabla.insert("", "end", iid=nuevo_id, values=datos)
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Registro creado correctamente.")

    def actualizar_registro(self):
        seleccion = self.tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Atención", "Debe seleccionar un registro de la tabla para actualizar.")
            return

        nuevos_datos = self.obtener_datos_entradas()

        if self.validar_campos_vacios(nuevos_datos):
            return
        
        id_registro = seleccion[0]
        self.db.actualizar(self.nombre_tabla, list(self.campos.keys()), nuevos_datos, id_registro)
        self.tabla.item(id_registro, values=nuevos_datos)
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
                
    def borrar_registro(self):
        seleccion = self.tabla.selection()
        if seleccion:
            id_registro = seleccion[0]
            self.db.eliminar(self.nombre_tabla, id_registro)
            self.tabla.delete(id_registro)
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
        else:
            messagebox.showwarning("Atención", "Debe seleccionar un registro de la tabla para eliminar.")
            
    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
                
    def validar_campos_vacios(self, datos):
        if any(valor.strip() == "" for valor in datos):
            messagebox.showwarning("Campo Vacío", "Este campo es obligatorio y no puede quedar vacío.")
            return True
        return False

    def obtener_datos_entradas(self):
        return [entry.get() for entry in self.entradas.values()]
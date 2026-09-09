import tkinter as tk
from tkinter import ttk

class CRUDGenerico:
    def __init__(self, contenedor, campos, fila_base=None):
    
        self.contenedor = contenedor
        self.campos = campos
        self.entradas = {}
        self.memoria = []
        
        f_base = fila_base if fila_base is not None else len(self.campos)
        
        boton_crear = tk.Button(self.contenedor, text="Crear", command=self.crear_registro)
        boton_crear.grid(row=f_base, column=0, pady=10)
        
        boton_borrar = tk.Button(self.contenedor, text='Borrar', command=self.borrar_registro)
        boton_borrar.grid(row=f_base, column=1, pady=10)

        boton_actualizar = tk.Button(self.contenedor, text='Actualizar', command=self.actualizar_registro)
        boton_actualizar.grid(row=f_base, column=2, pady=10)
        
        tabla = ttk.Treeview(self.contenedor, columns= list(self.campos.keys()), show="headings", height=5)
        tabla.grid(row=f_base + 1, column=0, columnspan=3, padx=5, pady=5)
        self.tabla = tabla
        
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_registro)


        for indice, (clave, texto_label) in enumerate(self.campos.items()):
            etiqueta  = tk.Label(self.contenedor, text=texto_label)
            campo = tk.Entry(self.contenedor)
            etiqueta.grid(row=indice, column=0, padx=5, pady=2, sticky="e")
            campo.grid(row=indice, column=1, padx=5, pady=2)
            self.entradas[clave] = campo
            self.tabla.heading(clave, text=texto_label)
            self.tabla.column(clave, width=100)
            
        for i in range(len(self.campos), f_base):
            tk.Label(self.contenedor, text="").grid(row=i, column=0, pady=2)
    
    
    def seleccionar_registro(self,event):
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
        
        self.memoria.append(datos)
        self.tabla.insert("", "end", values=datos)
        self.limpiar_campos()
        print("-" * 30)
        print("Éxito: Registro creado correctamente.")


    def actualizar_registro(self):
        seleccion = self.tabla.selection()
        
        if not seleccion:
            print("-" * 30)
            print("Error: Debe seleccionar un registro de la tabla para actualizar.")
            return

        nuevos_datos = self.obtener_datos_entradas()

        if self.validar_campos_vacios(nuevos_datos)        :
            return
        
        self.tabla.item(seleccion[0], values=nuevos_datos)
        self.limpiar_campos()
        print("-" * 30)
        print("Éxito: Registro actualizado correctamente.")
                
    
    def borrar_registro(self):
        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.delete(seleccion[0])
            self.limpiar_campos()
            print("-" * 30)
            print("Éxito: Registro eliminado correctamente.")
        else:
            print("-" * 30)
            print("Error: Debe seleccionar un registro de la tabla para eliminar.")
            
            
    def limpiar_campos(self):
        for entry in self.entradas.values():
                entry.delete(0, tk.END)
                
    def validar_campos_vacios(self, datos):
        if any(valor.strip() == "" for valor in datos):
            print("-" * 30)
            print("Error: Este campo es obligatorio y no puede quedar vacío.")
            return True
        return False
                

    def obtener_datos_entradas(self):
        nuevo_registro = []
        for clave, entry in self.entradas.items():
            nuevo_registro.append(entry.get())
        return nuevo_registro
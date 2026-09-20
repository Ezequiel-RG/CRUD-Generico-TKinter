import tkinter as tk
from tkinter import ttk
from PracticaTK2 import CRUDGenerico

root = tk.Tk()
root.title("Concesionaria")
root.geometry("550x450")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab_vehiculos = ttk.Frame(notebook)
tab_propietarios = ttk.Frame(notebook)

notebook.add(tab_vehiculos, text="Vehículos")
notebook.add(tab_propietarios, text="Propietarios")

vehiculos = {"marca": "Marca", "modelo": "Modelo", "anio": "Año de Fabricación"}
propietarios = {"nombre": "Nombre", "edad": "Edad", "dni": "DNI", "telefono": "Telefono"}

gestion_vehiculos = CRUDGenerico(tab_vehiculos, vehiculos, "vehiculos")
gestion_propietarios = CRUDGenerico(tab_propietarios, propietarios, "propietarios")

root.mainloop()
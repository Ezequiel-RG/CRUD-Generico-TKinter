import tkinter as tk
from PracticaTK2 import CRUDGenerico

root = tk.Tk()
root.title ("Concesionaria")

frame_vehiculos = tk.Frame(root)
frame_vehiculos.grid(row=0, column=0, sticky="n",padx=10, pady=10)

frame_propietarios = tk.Frame(root)
frame_propietarios.grid(row=0, column=2, sticky="n", padx=10, pady=10)

vehiculos = {"marca": "Marca", "modelo": "Modelo", "anio": "Año de Fabricación"}
propietarios = {"nombre": "Nombre", "edad": "Edad", "dni": "DNI", "telefono": "Telefono"}

fila_base = max(len(vehiculos), len(propietarios))

gestion_vehiculos = CRUDGenerico(frame_vehiculos,vehiculos,fila_base)
gestion_propietarios = CRUDGenerico(frame_propietarios,propietarios,fila_base)


root.mainloop()
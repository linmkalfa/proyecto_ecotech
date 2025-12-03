class Persona:
    def __init__(self, nombre, rut, direccion, email, telefono):
        self.nombre = nombre
        self.rut = rut
        self.direccion = direccion
        self.email = email
        self.telefono = telefono

    def mostrar_informacion(self):
        return f"Persona: {self.nombre}, (RUT: {self.rut})"
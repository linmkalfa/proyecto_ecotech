import sqlite3
from models.clases_base import Persona
from database.conexion import db

class Empleado(Persona):
    def __init__(self, nombre, rut, direccion, telefono, email, fecha_contrato, salario, depto_id=None, id_empleado=None):
        # Llamada al constructor de la clase base Persona, osea el PADRE
        super().__init__(nombre, rut, direccion, email, telefono)
        self.email = email
        self.fecha_contrato = fecha_contrato
        self.id_empleado = id_empleado
        self.depto_id = depto_id

        #Encapulsamiento con atributo privado __salario
        self.__salario = salario

    # Getter para salario
    @property
    def salario(self):
        return self.__salario
    
    # Setter para salario
    @salario.setter
    def salario(self, nuevo_salario):
        if nuevo_salario >= 0:
            self.__salario = nuevo_salario
        else:
            raise ValueError("El salario no puede ser negativo.")  
    
    def mostrar_informacion(self):
        return f"Empleado ID {self.id_empleado}: {self.nombre} - Cargo: Contratado el {self.fecha_contrato}"
    
    # --- Metodos CRUD ---
    
    def guardar(self):
        """Guarda (Create) el empleado en la base de datos."""
        sql = """INSERT INTO empleados (nombre, rut, direccion, email, telefono, fecha_contrato, salario, depto_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (self.nombre, self.rut, self.direccion, self.email, self.telefono,
                                 self.fecha_contrato, self.__salario, self.depto_id))
            conn.commit()
            print(f"Empleado {self.nombre} registrado exitosamente.")
        except sqlite3.IntegrityError:
            print(f"Error al registrar empleado: Ya exite un empleado con ese RUT.")
        except Exception as e:
            print(f"Error al registrar empleado: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        """Lee (Read) todos los empleados de la base de datos."""
        sql = "SELECT * FROM empleados"
        conn = db.conectar()
        lista_empleados = []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                # Mapeo de columnas a atributos de la clase Empleado
                empleado = Empleado(
                    id_empleado=fila[0],
                    nombre=fila[1],
                    rut=fila[2],
                    direccion=fila[3],
                    telefono=fila[4],
                    email=fila[5],
                    fecha_contrato=fila[6],
                    salario=fila[7],
                    depto_id=fila[8],
                )
                lista_empleados.append(empleado)
        except Exception as e:
            print(f"Error al listar empleados: {e}")
        finally:
            conn.close()
        return lista_empleados
    
    @staticmethod
    def actualizar_salario(id_emp, nuevo_salario):
        """UPDATE: Actualiza el salario de un empleado específico."""
        sql = "UPDATE empleados SET salario = ? WHERE id = ?"
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nuevo_salario, id_emp))
            conn.commit()
            print(f"Salario del empleado ID {id_emp} actualizado a {nuevo_salario}.")
        except Exception as e:
            print(f"Error al actualizar salario: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_emp):
        """DELETE: Elimina un empleado de la base de datos por su ID."""
        sql = "DELETE FROM empleados WHERE id = ?"
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            filas_afectadas = cursor.execute(sql, (id_emp,)).rowcount
            conn.commit()
            if filas_afectadas == 0:
                print("Empleado eliminado.")
            else:
                print("No se encontró el ID.")
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
        finally:
            conn.close()

class Departamento:
    def __init__(self, nombre, gerente, id_depto=None):
        self.id_depto = id_depto
        self.nombre = nombre
        self.gerente = gerente
    
    def mostrar_informacion(self):
        return f"Departamento: {self.nombre}, Gerente: {self.gerente}"
    
    def guardar(self):
        sql = "INSERT INTO departamentos (nombre, gerente) VALUES (?, ?)"
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (self.nombre, self.gerente))
            conn.commit()
            print(f"Departamento {self.nombre} registrado exitosamente.")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departamentos")
        data = cursor.fetchall()
        conn.close()
        # Retorna lista de diccionarios para facilitar la lectura
        return [{"id": d[0], "nombre": d[1], "gerente": d[2]} for d in data]
    
# --- CLASE PROYECTO ---
class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio, id_proyecto=None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def mostrar_informacion(self):
        return f"Proyecto: {self.nombre}, Iniciado el: {self.fecha_inicio}"
    
    def guardar(self):
        sql = "INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES (?, ?, ?)"
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (self.nombre, self.descripcion, self.fecha_inicio))
            conn.commit()
            print(f"Proyecto {self.nombre} registrado exitosamente.")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            conn.close()
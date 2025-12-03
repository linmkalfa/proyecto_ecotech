import sqlite3
import os

class DBManager:
    """
    Clase Singleton para manejar la conexión a la base de datos.
    Actualizada para Etapa 2 con tabla de indicadores.
    """
    
    def __init__(self, db_name="ecotech.db"):
        self.db_name = db_name

    def conectar(self):
        try:
            conexion = sqlite3.connect(self.db_name)
            return conexion
        except sqlite3.Error as e:
            print(f"Error crítico de conexión: {e}")
            return None

    def inicializar_tablas(self):
        # Script SQL completo (Etapa 1 + Etapa 2)
        sql_script = """
        -- Tabla Departamentos
        CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gerente TEXT
        );

        -- Tabla Proyectos
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT
        );

        -- Tabla Empleados (Con FK a Departamentos)
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rut TEXT UNIQUE NOT NULL,
            direccion TEXT,
            telefono TEXT,
            email TEXT,
            fecha_contrato TEXT,
            salario REAL,
            departamento_id INTEGER,
            FOREIGN KEY(departamento_id) REFERENCES departamentos(id)
        );

        -- Tabla Asignaciones (Relación Muchos a Muchos: Empleados <-> Proyectos)
        CREATE TABLE IF NOT EXISTS asignaciones (
            empleado_id INTEGER,
            proyecto_id INTEGER,
            FOREIGN KEY(empleado_id) REFERENCES empleados(id),
            FOREIGN KEY(proyecto_id) REFERENCES proyectos(id),
            PRIMARY KEY (empleado_id, proyecto_id)
        );

        -- NUEVA TABLA (Etapa 2): Registro de Indicadores Económicos
        CREATE TABLE IF NOT EXISTS indicadores_economicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicador TEXT NOT NULL,
            valor REAL NOT NULL,
            fecha_valor TEXT,
            fecha_consulta TEXT,
            usuario TEXT,
            origen TEXT
        );

        -- Insertar Departamentos
        INSERT INTO departamentos (nombre, gerente) VALUES ('Tecnología', 'Carlos Díaz');
        INSERT INTO departamentos (nombre, gerente) VALUES ('Recursos Humanos', 'Ana López');
        INSERT INTO departamentos (nombre, gerente) VALUES ('Finanzas', 'Roberto Gómez');

        -- Insertar Proyectos
        INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES ('Migración Cloud', 'Mover servidores a AWS', '2023-11-01');
        INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES ('Auditoría 2024', 'Revisión contable anual', '2024-01-15');
        INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES ('Portal Empleado', 'Nueva intranet corporativa', '2023-12-05');

        -- Insertar Empleados
        -- Notarás que el departamento_id (último número) coincide con los IDs de arriba (1, 2 o 3)
        INSERT INTO empleados (nombre, rut, direccion, telefono, email, fecha_contrato, salario, departamento_id) 
        VALUES ('Juan Pérez', '12.345.678-9', 'Av. Siempre Viva 123', '912345678', 'juan@ecotech.cl', '2022-03-15', 1500000, 1);

        INSERT INTO empleados (nombre, rut, direccion, telefono, email, fecha_contrato, salario, departamento_id) 
        VALUES ('María González', '9.876.543-2', 'Calle Falsa 456', '987654321', 'maria@ecotech.cl', '2021-08-20', 1800000, 1);

        INSERT INTO empleados (nombre, rut, direccion, telefono, email, fecha_contrato, salario, departamento_id) 
        VALUES ('Pedro Tapia', '15.555.444-K', 'Pasaje Los Olivos 90', '955554444', 'pedro@ecotech.cl', '2023-01-10', 950000, 2);

        -- Insertar Historial de Indicadores (Simulados)
        INSERT INTO indicadores_economicos (indicador, valor, fecha_valor, fecha_consulta, usuario, origen)
        VALUES ('uf', 36500.50, '2023-11-30', '2023-11-30 10:00:00', 'Admin', 'mindicador.cl');

        INSERT INTO indicadores_economicos (indicador, valor, fecha_valor, fecha_consulta, usuario, origen)
        VALUES ('dolar', 890.25, '2023-11-30', '2023-11-30 10:05:00', 'Admin', 'mindicador.cl');
        """
        
        conn = self.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.executescript(sql_script)
                conn.commit()
                print("Base de datos verificada (Tablas listas).")
            except sqlite3.Error as e:
                print(f"Error al inicializar tablas: {e}")
            finally:
                conn.close()

# Instancia global (MUY IMPORTANTE QUE ESTÉ AQUÍ)
db = DBManager()
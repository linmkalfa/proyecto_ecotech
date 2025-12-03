import sys
from database.conexion import db
from models.entidades import Empleado, Departamento, Proyecto
from models.servicios import GestorIndicadores 

def pausa():
    input("\nPresione Enter para continuar...")

def menu_principal():
    # Inicializa tablas (Etapa 1 y 2)
    db.inicializar_tablas()

    while True:
        print("\n" + "="*45)
        print("SISTEMA DE GESTIÓN ECO-TECH v2.0")
        print("="*45)
        print("1. Gestionar Empleados")
        print("2. Gestionar Departamentos")
        print("3. Gestionar Proyectos")
        print("4. Indicadores Económicos (API)")
        print("5. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            sub_menu_empleados()
        elif opcion == '2':
            sub_menu_departamentos()
        elif opcion == '3':
            sub_menu_proyectos()
        elif opcion == '4':
            sub_menu_indicadores()
        elif opcion == '5':
            print("Saliendo del programa...")
            sys.exit()
        else:
            print("Opción no válida.")
            pausa()

def sub_menu_empleados():
    while True:
        print("\n--- GESTIÓN DE EMPLEADOS ---")
        print("1. Agregar Empleado (Create)")
        print("2. Listar Empleados (Read)")
        print("3. Actualizar salario (Update)")
        print("4. Eliminar Empleado (Delete)")
        print("5. Volver")

        op = input("Opción: ")

        if op == '1':
            try:
                print("\n--- Nuevo Registro ---")
                nombre = input("Nombre: ")
                rut = input("RUT: ")
                direc = input("Dirección: ")
                email = input("Email: ")
                tel = input("Teléfono: ")
                fecha = input("Fecha Contrato (YYYY-MM-DD): ")
                
                while True:
                    try:
                        salario = float(input("Salario: "))
                        break
                    except ValueError:
                        print("El salario debe ser un número.")

                print("\nDepartamentos disponibles:")
                for d in Departamento.listar_todos():
                    print(f"ID {d['id']}: {d['nombre']}")
                
                # CORRECCIÓN DE BUG: Enter vacío
                entrada_depto = input("ID del Departamento (Enter para ninguno): ")
                if entrada_depto.strip():
                    depto_id = int(entrada_depto)
                else:
                    depto_id = None

                nuevo_emp = Empleado(nombre, rut, direc, tel, email, fecha, salario, depto_id)
                nuevo_emp.guardar()
            except ValueError as e:
                print(f"Error en los datos: {e}")
        
        elif op == '2':
            print("\n--- Nómina de Empleados ---")
            lista = Empleado.listar_todos()
            if not lista:
                print("No hay empleados registrados.")
            for emp in lista:
                print(f"{emp.mostrar_informacion()} | Salario: ${emp.salario}")
        
        elif op == '3':
            try:
                id_emp = int(input("ID del empleado a actualizar: "))
                monto = float(input("Nuevo salario: "))
                Empleado.actualizar_salario(id_emp, monto)
            except ValueError:
                print("Debe ingresar números válidos.")
        
        elif op == '4':
            try:
                id_emp = int(input("ID del empleado a eliminar: "))
                Empleado.eliminar(id_emp)
            except ValueError:
                print("ID inválido.")

        elif op == '5':
            break
        pausa()

def sub_menu_departamentos():
    while True:
        print("\n--- GESTIÓN DE DEPARTAMENTOS ---")
        print("1. Agregar Departamento")
        print("2. Listar Departamentos")
        print("3. Volver")

        op = input("Opción: ")

        if op == '1':
            nom = input("Nombre Depto: ")
            gerente = input("Gerente: ")
            d = Departamento(nom, gerente)
            d.guardar()
        elif op == '2':
            lista = Departamento.listar_todos()
            for d in lista:
                print(f"ID: {d['id']} | {d['nombre']} (Gerente: {d['gerente']})")
        elif op == '3':
            break
        pausa()

def sub_menu_proyectos():
    while True:
        print("\n--- GESTIÓN DE PROYECTOS ---")
        print("1. Crear Proyecto")
        print("2. Volver")
        op = input("Opción: ")

        if op == '1':
            nom = input("Nombre Proyecto: ")
            desc = input("Descripción: ")
            fecha = input("Fecha Inicio: ")
            p = Proyecto(nom, desc, fecha)
            p.guardar()
        elif op == '2':
            break
        pausa()

def sub_menu_indicadores():
    """Submenú para la Etapa 2: Consumo de APIs"""
    while True:
        print("\n--- INDICADORES ECONÓMICOS (API) ---")
        print("1. Consultar UF")
        print("2. Consultar Dólar")
        print("3. Consultar Euro")
        print("4. Consultar UTM")
        print("5. Ver Historial Local (Base de Datos)")
        print("6. Volver")
        
        op = input("Opción: ")
        indicador = ""
        
        if op == '1': indicador = "uf"
        elif op == '2': indicador = "dolar"
        elif op == '3': indicador = "euro"
        elif op == '4': indicador = "utm"
        elif op == '5':
            print("\n--- Historial de Consultas ---")
            historial = GestorIndicadores.listar_historial()
            if not historial:
                print("No hay consultas guardadas.")
            else:
                print(f"{'ID':<4} | {'Indicador':<10} | {'Valor':<12} | {'Fecha Consulta'}")
                print("-" * 60)
                for h in historial:
                    print(f"{h[0]:<4} | {h[1]:<10} | ${h[2]:<11} | {h[4]}")
            pausa()
            continue
        elif op == '6':
            break
        else:
            print("Opción inválida.")
            continue
            
        if indicador:
            print(f"\n📡 Conectando a mindicador.cl para consultar {indicador.upper()}...")
            resultado = GestorIndicadores.consultar_indicador(indicador)
            
            if resultado:
                print("\nConsulta Exitosa:")
                print(f"   • Indicador: {resultado['nombre']}")
                print(f"   • Valor: ${resultado['valor']} {resultado['unidad']}")
                print(f"   • Fecha Oficial: {resultado['fecha']}")
                print("   • Estado: Guardado en Base de Datos")
            pausa()

if __name__ == "__main__":
    menu_principal()
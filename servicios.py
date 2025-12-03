import requests
from datetime import datetime
from database.conexion import db

class GestorIndicadores:
    """
    Clase encargada de consumir la API externa (mindicador.cl)
    y guardar la información en la base de datos local.
    """
    
    BASE_URL = "https://mindicador.cl/api"

    @staticmethod
    def consultar_indicador(tipo_indicador, usuario="Admin"):
        """
        1. Conecta a la API.
        2. Obtiene el JSON.
        3. Guarda el historial en la BD.
        4. Retorna los datos para mostrarlos en consola.
        """
        # Construimos la URL (ej: https://mindicador.cl/api/dolar)
        url = f"{GestorIndicadores.BASE_URL}/{tipo_indicador}"
        print(f"🌍 Conectando con {url}...")
        
        try:
            # Hacemos la petición GET con un timeout de 10 segundos
            respuesta = requests.get(url, timeout=10)
            
            # Verificamos si la API respondió bien (Código 200 = OK)
            if respuesta.status_code != 200:
                print(f"Error: La API respondió con código {respuesta.status_code}")
                return None

            # Convertimos la respuesta de texto a Diccionario Python (JSON)
            data = respuesta.json()
            
            # Validamos que vengan datos reales
            if 'serie' not in data or len(data['serie']) == 0:
                print("La API no devolvió datos.")
                return None

            # La API devuelve una lista 'serie', tomamos el primero (el más actual)
            serie_actual = data['serie'][0]
            
            valor = serie_actual['valor']
            # Cortamos la fecha para que quede YYYY-MM-DD
            fecha_valor = serie_actual['fecha'][:10]
            # Fecha exacta de cuando TÚ hiciste la consulta
            fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            origen = "mindicador.cl"

            # Guardamos en la base de datos automáticamente
            GestorIndicadores.guardar_historial(
                tipo_indicador, valor, fecha_valor, fecha_consulta, usuario, origen
            )
            
            # Retornamos un diccionario limpio para usar en el menú
            return {
                "nombre": data['nombre'],
                "valor": valor,
                "unidad": data['unidad_medida'],
                "fecha": fecha_valor
            }

        except Exception as e:
            print(f"Error al consultar API: {e}")
            return None

    @staticmethod
    def guardar_historial(indicador, valor, fecha_valor, fecha_consulta, usuario, origen):
        """
        Método auxiliar para insertar el registro en la tabla 'indicadores_economicos'.
        """
        sql = """
        INSERT INTO indicadores_economicos 
        (indicador, valor, fecha_valor, fecha_consulta, usuario, origen)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        conn = db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (indicador, valor, fecha_valor, fecha_consulta, usuario, origen))
            conn.commit()
            print("Registro guardado en historial local.")
        except Exception as e:
            print(f"Error al guardar en BD: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_historial():
        """
        Recupera todo el historial guardado en la base de datos local
        ordenado desde el más reciente.
        """
        sql = "SELECT * FROM indicadores_economicos ORDER BY id DESC"
        conn = db.conectar()
        resultados = []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Error al leer historial: {e}")
        finally:
            conn.close()
        return resultados
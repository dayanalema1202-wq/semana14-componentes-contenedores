import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos: str | Path) -> None:
        self.carpeta_datos = Path(carpeta_datos)

    def leer_json(self, nombre_archivo: str) -> list:
        # Lee un archivo JSON de la carpeta de datos y entrega una lista.
        ruta = self.carpeta_datos / nombre_archivo

        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe aun. Se continua sin datos.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {nombre_archivo} no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print(f"No hay permisos para leer {nombre_archivo}.")
            return []

        if not isinstance(datos, list):
            print(f"El archivo {nombre_archivo} debe contener una lista de registros.")
            return []

        return datos

    def escribir_json(self, nombre_archivo: str, datos: list) -> bool:
        # Guarda la informacion en disco; se conserva para futuras entregas.
        ruta = self.carpeta_datos / nombre_archivo

        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos para escribir {nombre_archivo}.")
            return False

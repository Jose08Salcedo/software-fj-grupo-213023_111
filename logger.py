# =============================================================================
# Módulo: logger.py
# Responsable: Integrante 1
# Descripción: Configura el archivo de logs donde se registran todos los
#              eventos y errores del sistema (logs/software_fj.log).
# =============================================================================

import logging  # Módulo estándar de Python para registrar eventos
import os  # Permite crear carpetas y manejar rutas

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # Carpeta "logs" junto al proyecto
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")  # Ruta completa del archivo de log


def obtener_logger(nombre="SoftwareFJ"):  # Devuelve un logger configurado
    """Crea (una sola vez) y devuelve el logger del sistema."""
    try:  # Intentamos crear la carpeta de logs
        os.makedirs(CARPETA_LOGS, exist_ok=True)  # No falla si ya existe
    except OSError as error:  # Si no hay permisos o la ruta es inválida
        print(f"No se pudo crear la carpeta de logs: {error}")  # Avisamos pero no detenemos el programa

    logger = logging.getLogger(nombre)  # Obtiene (o crea) el logger con ese nombre
    if not logger.handlers:  # Evita agregar manejadores duplicados
        logger.setLevel(logging.DEBUG)  # Registra desde DEBUG hacia arriba
        formato = logging.Formatter(  # Define cómo se verá cada línea del log
            "%(asctime)s | %(levelname)-8s | %(message)s",  # Fecha | nivel | mensaje
            datefmt="%Y-%m-%d %H:%M:%S",  # Formato de la fecha
        )
        try:  # Intentamos abrir el archivo de log
            manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Escribe en el archivo
            manejador.setFormatter(formato)  # Aplica el formato definido
            logger.addHandler(manejador)  # Conecta el manejador al logger
        except OSError as error:  # Si no se puede escribir el archivo
            print(f"No se pudo abrir el archivo de log: {error}")  # Avisamos
            logger.addHandler(logging.NullHandler())  # Seguimos sin log en archivo para no romper la app
    return logger  # Devuelve el logger listo para usar

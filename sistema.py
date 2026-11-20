# =============================================================================
# Módulo: sistema.py
# Responsable: Integrante 5
# Descripción: Clase GestorSoftwareFJ que administra las LISTAS internas de
#              clientes, servicios y reservas (sin base de datos). Captura
#              las excepciones, las registra en el log y mantiene la app activa.
# =============================================================================

from cliente import Cliente  # Clase Cliente
from excepciones import (  # Excepciones del sistema
    ClienteInvalidoError,
    ReservaError,
    ServicioInvalidoError,
    SoftwareFJError,
)
from logger import obtener_logger  # Logger del sistema
from reserva import Reserva  # Clase Reserva
from servicios import AlquilerEquipo, Asesoria, ReservaSala  # Servicios concretos

log = obtener_logger()  # Logger compartido


class GestorSoftwareFJ:  # Controla todo el sistema
    """Gestiona clientes, servicios y reservas en memoria."""

    TIPOS_SERVICIO = {  # Relaciona un texto con la clase concreta (extensible)
        "sala": ReservaSala,
        "equipo": AlquilerEquipo,
        "asesoria": Asesoria,
    }

    def __init__(self):  # Crea las listas vacías
        self.__clientes = []  # Lista interna de clientes
        self.__servicios = []  # Lista interna de servicios
        self.__reservas = []  # Lista interna de reservas
        log.info("=== Sistema Software FJ iniciado ===")  # Log de inicio

    # ---------------- Clientes ----------------
    def registrar_cliente(self, nombre, documento, correo, telefono):  # Registra un cliente nuevo
        try:  # Intentamos crear el cliente
            if any(c.documento == str(documento) for c in self.__clientes):  # Documento repetido
                raise ClienteInvalidoError(f"Ya existe un cliente con documento {documento}")  # Error
            cliente = Cliente(nombre, documento, correo, telefono)  # Valida en el constructor
        except SoftwareFJError as error:  # Cualquier error propio
            log.error(f"Registro de cliente fallido: {error}")  # Se registra en el log
            raise  # Se relanza para que quien llama decida qué mostrar
        else:  # Si todo salió bien
            self.__clientes.append(cliente)  # Se agrega a la lista
            log.info(f"Cliente registrado: {cliente.describir()}")  # Log
            return cliente  # Devuelve el cliente creado

    # ---------------- Servicios ----------------
    def crear_servicio(self, tipo, **datos):  # Crea un servicio según su tipo
        try:  # Intentamos crear el servicio
            clase = self.TIPOS_SERVICIO[tipo]  # Busca la clase; KeyError si no existe
            servicio = clase(**datos)  # Crea el objeto; TypeError si faltan datos
        except KeyError as error:  # Tipo de servicio desconocido
            log.error(f"Tipo de servicio desconocido: '{tipo}'")  # Log
            raise ServicioInvalidoError(f"Tipo de servicio '{tipo}' no existe") from error  # ENCADENAMIENTO
        except TypeError as error:  # Parámetros faltantes o sobrantes
            log.error(f"Parámetros incorrectos para servicio '{tipo}': {error}")  # Log
            raise ServicioInvalidoError(f"Parámetros incorrectos para '{tipo}'") from error  # ENCADENAMIENTO
        except SoftwareFJError as error:  # Validación propia del servicio
            log.error(f"Creación de servicio fallida: {error}")  # Log
            raise  # Se relanza
        else:  # Si se creó correctamente
            self.__servicios.append(servicio)  # Se agrega a la lista
            log.info(f"Servicio creado: {servicio.describir()}")  # Log
            return servicio  # Devuelve el servicio

    # ---------------- Reservas ----------------
    def crear_reserva(self, cliente, servicio, horas, **detalles):  # Crea y confirma una reserva
        reserva = None  # Se inicializa por si falla la creación
        try:  # Intentamos crear y confirmar
            reserva = Reserva(cliente, servicio, horas, **detalles)  # Crea la reserva
            reserva.confirmar()  # Puede lanzar errores
        except SoftwareFJError as error:  # Cualquier error del sistema
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""  # Muestra la excepción encadenada
            log.error(f"Reserva fallida: {error}{causa}")  # Log con causa original
            raise  # Se relanza
        else:  # Reserva confirmada
            self.__reservas.append(reserva)  # Se guarda en la lista
            return reserva  # Devuelve la reserva
        finally:  # Siempre se ejecuta
            estado = reserva.estado if reserva else "NO CREADA"  # Estado final del intento
            log.debug(f"Intento de reserva finalizado. Estado: {estado}")  # Auditoría

    # ---------------- Consultas ----------------
    def buscar_cliente(self, documento):  # Busca un cliente por documento
        for cliente in self.__clientes:  # Recorre la lista
            if cliente.documento == str(documento):  # Coincide
                return cliente  # Lo devuelve
        raise ClienteInvalidoError(f"No existe cliente con documento {documento}")  # No se encontró

    def listar(self, tipo):  # Devuelve una copia de la lista pedida
        listas = {"clientes": self.__clientes, "servicios": self.__servicios, "reservas": self.__reservas}  # Mapa
        if tipo not in listas:  # Tipo inválido
            raise ReservaError(f"No existe la lista '{tipo}'")  # Error
        return list(listas[tipo])  # Copia para proteger la lista original (encapsulación)

    def resumen(self):  # Totales del sistema
        procesadas = [r for r in self.__reservas if r.estado == Reserva.PROCESADA]  # Reservas cobradas
        ingresos = sum(r.costo_final for r in procesadas)  # Suma de ingresos
        return {  # Diccionario con el resumen
            "clientes": len(self.__clientes),
            "servicios": len(self.__servicios),
            "reservas": len(self.__reservas),
            "procesadas": len(procesadas),
            "ingresos": ingresos,
        }

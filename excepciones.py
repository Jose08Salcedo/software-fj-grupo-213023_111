# =============================================================================
# Módulo: excepciones.py
# Responsable: Integrante 1
# Descripción: Define la jerarquía de excepciones personalizadas del sistema
#              Software FJ. Todas heredan de SoftwareFJError para poder
#              capturarlas de forma general o específica.
# =============================================================================


class SoftwareFJError(Exception):  # Excepción base de todo el sistema
    """Excepción raíz de Software FJ."""

    def __init__(self, mensaje, codigo="FJ-000"):  # Recibe mensaje y código de error
        super().__init__(mensaje)  # Inicializa la clase Exception con el mensaje
        self.mensaje = mensaje  # Guarda el mensaje legible del error
        self.codigo = codigo  # Guarda un código para identificar el tipo de error

    def __str__(self):  # Representación en texto del error
        return f"[{self.codigo}] {self.mensaje}"  # Ej: [FJ-101] Correo inválido


class ValidacionError(SoftwareFJError):  # Errores por datos inválidos
    """Se lanza cuando un dato no cumple las reglas de validación."""

    def __init__(self, mensaje, codigo="FJ-100"):  # Código por defecto 100
        super().__init__(mensaje, codigo)  # Llama al constructor de la base


class ClienteInvalidoError(ValidacionError):  # Datos de cliente incorrectos
    """Datos personales del cliente inválidos."""

    def __init__(self, mensaje):  # Solo necesita el mensaje
        super().__init__(mensaje, "FJ-101")  # Código propio de clientes


class ServicioInvalidoError(ValidacionError):  # Datos de servicio incorrectos
    """Parámetros de creación o uso de un servicio inválidos."""

    def __init__(self, mensaje):  # Solo necesita el mensaje
        super().__init__(mensaje, "FJ-102")  # Código propio de servicios


class ParametroFaltanteError(SoftwareFJError):  # Falta un dato obligatorio
    """Se lanza cuando un parámetro obligatorio no fue enviado."""

    def __init__(self, parametro):  # Recibe el nombre del parámetro faltante
        super().__init__(f"Falta el parámetro obligatorio: '{parametro}'", "FJ-200")  # Mensaje automático
        self.parametro = parametro  # Guarda el nombre del parámetro


class ServicioNoDisponibleError(SoftwareFJError):  # Servicio inactivo
    """El servicio solicitado no está disponible."""

    def __init__(self, nombre_servicio):  # Recibe el nombre del servicio
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "FJ-300")  # Mensaje automático


class ReservaError(SoftwareFJError):  # Errores generales de reservas
    """Error al crear, confirmar, cancelar o procesar una reserva."""

    def __init__(self, mensaje, codigo="FJ-400"):  # Código por defecto 400
        super().__init__(mensaje, codigo)  # Llama al constructor de la base


class OperacionNoPermitidaError(ReservaError):  # Acción inválida según el estado
    """Operación no permitida para el estado actual de la reserva."""

    def __init__(self, mensaje):  # Solo necesita el mensaje
        super().__init__(mensaje, "FJ-401")  # Código propio


class CalculoInconsistenteError(SoftwareFJError):  # Errores de cálculo de costos
    """El cálculo de un costo produjo un valor inválido."""

    def __init__(self, mensaje):  # Solo necesita el mensaje
        super().__init__(mensaje, "FJ-500")  # Código propio de cálculos

# =============================================================================
# Módulo: entidades.py
# Responsable: Integrante 2
# Descripción: Define la clase abstracta base EntidadSistema de la cual
#              heredan todas las entidades del sistema Software FJ
#              (Clientes, Servicios y Reservas).
# =============================================================================

from abc import ABC, abstractmethod  # Herramientas para clases y métodos abstractos
from datetime import datetime  # Permite registrar la fecha y hora de creación
from excepciones import ValidacionError, ParametroFaltanteError  # Excepciones del Integrante 1


class EntidadSistema(ABC):  # Clase abstracta raíz del modelo de dominio
    """Clase abstracta que representa una entidad general en Software FJ."""

    def __init__(self, id_entidad: str):  # Constructor base para toda entidad
        self._id_entidad = None  # Atributo protegido para el identificador
        self._fecha_creacion = datetime.now()  # Marca de tiempo automática
        self.id_entidad = id_entidad  # Asigna usando el setter para validar

    @property
    def id_entidad(self) -> str:  # Getter del identificador
        """Devuelve el identificador único de la entidad."""
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str):  # Setter con validación estricta
        """Valida que el ID sea enviado y no esté vacío."""
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError("id_entidad")  # Lanza excepción FJ-200
        if not isinstance(valor, str):
            raise ValidacionError("El ID de la entidad debe ser una cadena de texto.")
        self._id_entidad = valor.strip().upper()  # Normaliza en mayúsculas

    @property
    def fecha_creacion(self) -> datetime:  # Getter de solo lectura
        """Devuelve la fecha y hora en que se creó la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar_datos(self) -> bool:  # Método obligatorio para clases hijas
        """Valida la integridad de todos los atributos de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:  # Método polimórfico obligatorio
        """Devuelve una descripción legible de la entidad."""
        pass

    def __str__(self) -> str:  # Representación en texto estándar
        return self.obtener_resumen()

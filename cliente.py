# =============================================================================
# Módulo: cliente.py
# Responsable: Integrante 2
# Descripción: Implementa la clase Cliente heredando de EntidadSistema, con
#              encapsulación privada, validaciones estrictas, encadenamiento
#              de excepciones y registro en el archivo de logs del sistema.
# =============================================================================

import re  # Expresiones regulares para validar formato de correo
from entidades import EntidadSistema  # Clase abstracta base
from excepciones import ClienteInvalidoError, ParametroFaltanteError  # Excepciones Integrante 1
from logger import obtener_logger  # Logger configurado por el Integrante 1

logger = obtener_logger()  # Instancia compartida del sistema de logs


class Cliente(EntidadSistema):  # Hereda de la clase abstracta EntidadSistema
    """Representa un cliente de Software FJ con datos encapsulados y validados."""

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str, telefono: str):
        super().__init__(id_cliente)  # Inicializa y valida el ID en la clase padre

        # Atributos privados (encapsulación estricta)
        self.__nombre = None
        self.__documento = None
        self.__correo = None
        self.__telefono = None
        self.__activo = True

        # Asignación mediante setters para ejecutar todas las reglas de validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

        self.validar_datos()  # Verificación final de integridad
        logger.info(f"Cliente registrado correctamente: {self.obtener_resumen()}")

    # --- PROPIEDAD: NOMBRE ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError("nombre")  # Excepción FJ-200
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre '{valor}' inválido: mínimo 3 caracteres.")  # FJ-101
        if any(caracter.isdigit() for caracter in valor):
            raise ClienteInvalidoError(f"Nombre '{valor}' inválido: no debe contener números.")
        self.__nombre = valor.strip().title()

    # --- PROPIEDAD: DOCUMENTO (Con encadenamiento de excepciones) ---
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError("documento")  # Excepción FJ-200
        try:
            doc_limpio = str(valor).strip()  # Elimina espacios sobrantes
            numero_doc = int(doc_limpio)  # Intenta convertir a entero para validar dígitos
            if numero_doc <= 0 or len(doc_limpio) < 5:
                raise ValueError("El documento debe ser positivo y tener al menos 5 dígitos.")
            self.__documento = doc_limpio
        except (ValueError, TypeError) as error_original:
            # Encadenamiento de excepciones ('raise ... from error_original')
            raise ClienteInvalidoError(
                f"Documento '{valor}' inválido: debe contener solo números válidos."
            ) from error_original

    # --- PROPIEDAD: CORREO ELECTRÓNICO ---
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError("correo")  # Excepción FJ-200
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Patrón estándar usuario@dominio.ext
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise ClienteInvalidoError(f"Correo '{valor}' inválido: formato incorrecto.")  # FJ-101
        self.__correo = valor.strip().lower()

    # --- PROPIEDAD: TELÉFONO ---
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError("telefono")  # Excepción FJ-200
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or not (7 <= len(tel_limpio) <= 15):
            raise ClienteInvalidoError(
                f"Teléfono '{valor}' inválido: debe tener entre 7 y 15 dígitos."
            )
        self.__telefono = tel_limpio

    # --- PROPIEDAD: ESTADO ---
    @property
    def activo(self) -> bool:
        return self.__activo

    def desactivar(self):
        """Inhabilita el cliente sin eliminar su historial del sistema."""
        self.__activo = False
        logger.info(f"Cliente {self.id_entidad} marcado como inactivo.")

    # --- IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ---
    def validar_datos(self) -> bool:
        """Verifica que todos los campos obligatorios tengan información válida."""
        if not all([self.__nombre, self.__documento, self.__correo, self.__telefono]):
            raise ClienteInvalidoError("El cliente tiene atributos obligatorios incompletos.")
        return True

    def obtener_resumen(self) -> str:
        """Retorna una cadena formateada con los datos principales del cliente."""
        estado = "Activo" if self.__activo else "Inactivo"
        return (
            f"[Cliente {self.id_entidad}] {self.__nombre} | "
            f"Doc: {self.__documento} | Correo: {self.__correo} | "
            f"Tel: {self.__telefono} | Estado: {estado}"
        )


# =============================================================================
# Bloque de validación secuencial del módulo (pruebas unitarias rápidas)
# =============================================================================
if __name__ == "__main__":
    print("=== PRUEBAS DE VALIDACIÓN: MÓDULO CLIENTE ===")

    # Caso 1: Creación válida
    try:
        c1 = Cliente("cli-01", "Laura Gómez", "1020304050", "laura@softwarefj.com", "3001234567")
        print("OK ->", c1)
    except Exception as err:
        print("FALLO INESPERADO:", err)

    # Caso 2: Documento inválido (prueba encadenamiento de excepciones y código FJ-101)
    try:
        c2 = Cliente("cli-02", "Carlos Ruiz", "ABC999", "carlos@correo.com", "3109876543")
    except ClienteInvalidoError as err:
        logger.error(f"Error controlado en prueba de cliente: {err} | Causa: {err.__cause__}")
        print(f"OK (Excepción capturada) -> {err}")
        print(f"   Causa original encadenada -> {repr(err.__cause__)}")

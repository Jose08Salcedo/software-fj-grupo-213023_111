# =============================================================================
# Módulo: main.py
# Responsable: Integrante 5 (con casos de prueba aportados por todos)
# Descripción: Simula 15 operaciones completas (válidas e inválidas) para
#              demostrar que el sistema sigue funcionando ante errores.
# Ejecución:   python main.py
# =============================================================================

from excepciones import SoftwareFJError  # Excepción base del sistema
from logger import ARCHIVO_LOG, obtener_logger  # Logger y ruta del archivo
from sistema import GestorSoftwareFJ  # Gestor principal

log = obtener_logger()  # Logger compartido
resultados = {"exitosas": 0, "fallidas": 0}  # Contador de resultados


def ejecutar(numero, descripcion, operacion):  # Ejecuta una operación de forma segura
    """Ejecuta 'operacion' sin que un error detenga el programa."""
    print(f"\nOperación {numero:02d}: {descripcion}")  # Muestra qué se va a hacer
    try:  # Intentamos ejecutar la operación
        resultado = operacion()  # Llama a la función recibida
    except SoftwareFJError as error:  # Errores esperados del sistema
        resultados["fallidas"] += 1  # Cuenta como fallida
        print(f"   ✗ Error controlado: {error}")  # Muestra el error
        log.warning(f"Operación {numero} ({descripcion}) terminó con error controlado: {error}")  # Queda en el log
        if error.__cause__:  # Si hay excepción encadenada
            print(f"     Causa original: {type(error.__cause__).__name__}: {error.__cause__}")  # La muestra
    except Exception as error:  # Cualquier error inesperado (red de seguridad)
        resultados["fallidas"] += 1  # Cuenta como fallida
        log.critical(f"Error inesperado en operación {numero}: {error!r}")  # Log crítico
        print(f"   ✗ Error inesperado: {error!r}")  # Lo muestra
    else:  # Si no hubo error
        resultados["exitosas"] += 1  # Cuenta como exitosa
        print(f"   ✓ {resultado}")  # Muestra el resultado
    finally:  # Siempre se ejecuta
        log.debug(f"Operación {numero} finalizada")  # Auditoría


def main():  # Punto de entrada
    sistema = GestorSoftwareFJ()  # Crea el gestor
    datos = {}  # Guarda objetos creados para usarlos en operaciones posteriores

    print("=" * 70)  # Línea decorativa
    print("        SOFTWARE FJ - Sistema de Clientes, Servicios y Reservas")  # Título
    print("=" * 70)  # Línea decorativa

    # ---------------- CLIENTES ----------------
    def op1():  # Cliente válido
        datos["ana"] = sistema.registrar_cliente("Ana Gómez", "1020304050", "ana@correo.com", "3001234567")
        return datos["ana"]

    def op2():  # Cliente válido
        datos["luis"] = sistema.registrar_cliente("Luis Pérez", "98765432", "luis.perez@empresa.co", "3157654321")
        return datos["luis"]

    def op3():  # Cliente inválido: correo mal escrito
        return sistema.registrar_cliente("Carlos Ruiz", "11223344", "carlos-correo.com", "3101112233")

    def op4():  # Cliente inválido: documento duplicado
        return sistema.registrar_cliente("Ana María", "1020304050", "otra@correo.com", "3009998877")

    def op5():  # Cliente inválido: nombre vacío
        return sistema.registrar_cliente("", "55667788", "x@y.com", "3201234567")

    # ---------------- SERVICIOS ----------------
    def op6():  # Servicio válido: sala
        datos["sala"] = sistema.crear_servicio("sala", nombre="Sala Andes", tarifa_hora=50000, capacidad=10)
        return datos["sala"]

    def op7():  # Servicio válido: equipo
        datos["equipo"] = sistema.crear_servicio("equipo", nombre="Portátil HP", tarifa_hora=8000, unidades=5, deposito=100000)
        return datos["equipo"]

    def op8():  # Servicio válido: asesoría
        datos["asesoria"] = sistema.crear_servicio("asesoria", nombre="Asesoría Cloud", tarifa_hora=120000,
                                                   especialidad="AWS", nivel="experto")
        return datos["asesoria"]

    def op9():  # Servicio inválido: tarifa negativa
        return sistema.crear_servicio("sala", nombre="Sala Caribe", tarifa_hora=-2000, capacidad=8)

    def op10():  # Servicio inválido: tipo inexistente (encadenamiento KeyError -> ServicioInvalidoError)
        return sistema.crear_servicio("transporte", nombre="Van", tarifa_hora=30000)

    # ---------------- RESERVAS ----------------
    def op11():  # Reserva exitosa + procesamiento con IVA y descuento (sobrecarga)
        r = sistema.crear_reserva(datos["ana"], datos["sala"], 3, personas=8)
        r.procesar(impuesto=0.19, descuento=0.10)  # Variante sobrecargada: impuesto + descuento
        return f"{r} (incluye IVA 19% y descuento 10%)"

    def op12():  # Reserva fallida: supera capacidad de la sala (encadenamiento)
        return sistema.crear_reserva(datos["luis"], datos["sala"], 2, personas=25)

    def op13():  # Reserva fallida: servicio no disponible
        datos["asesoria"].cambiar_disponibilidad(False)
        try:
            return sistema.crear_reserva(datos["luis"], datos["asesoria"], 2)
        finally:
            datos["asesoria"].cambiar_disponibilidad(True)  # Se reactiva para las siguientes pruebas

    def op14():  # Reserva exitosa de equipos, luego cancelación
        r = sistema.crear_reserva(datos["luis"], datos["equipo"], 24, cantidad=3)
        r.cancelar("Cliente cambió de fecha")
        datos["cancelada"] = r
        return r

    def op15():  # Operación no permitida: procesar una reserva cancelada
        return datos["cancelada"].procesar()

    def op16():  # Cálculo inconsistente: descuento del 150 %
        r = sistema.crear_reserva(datos["ana"], datos["asesoria"], 2)
        return r.procesar(descuento=1.5)

    def op17():  # Reserva exitosa de asesoría, procesada solo con IVA
        r = sistema.crear_reserva(datos["luis"], datos["asesoria"], 4)
        r.procesar()
        return r

    operaciones = [  # Lista de (descripción, función)
        ("Registrar cliente válido (Ana)", op1),
        ("Registrar cliente válido (Luis)", op2),
        ("Registrar cliente con correo inválido", op3),
        ("Registrar cliente con documento duplicado", op4),
        ("Registrar cliente sin nombre", op5),
        ("Crear servicio: sala de reuniones", op6),
        ("Crear servicio: alquiler de portátiles", op7),
        ("Crear servicio: asesoría experta", op8),
        ("Crear servicio con tarifa negativa", op9),
        ("Crear servicio de tipo inexistente", op10),
        ("Reservar sala y procesar con IVA y descuento", op11),
        ("Reservar sala superando su capacidad", op12),
        ("Reservar servicio no disponible", op13),
        ("Reservar equipos y cancelar", op14),
        ("Procesar una reserva cancelada", op15),
        ("Procesar con descuento inconsistente (150 %)", op16),
        ("Reservar asesoría y procesar con IVA", op17),
    ]

    for i, (descripcion, funcion) in enumerate(operaciones, start=1):  # Ejecuta cada operación
        ejecutar(i, descripcion, funcion)  # Ninguna detiene el programa

    # ---------------- RESUMEN ----------------
    r = sistema.resumen()  # Obtiene los totales
    print("\n" + "=" * 70)  # Línea decorativa
    print("RESUMEN")  # Título
    print(f"  Operaciones exitosas: {resultados['exitosas']} | fallidas (controladas): {resultados['fallidas']}")
    print(f"  Clientes: {r['clientes']} | Servicios: {r['servicios']} | Reservas: {r['reservas']}")
    print(f"  Reservas procesadas: {r['procesadas']} | Ingresos: ${r['ingresos']:,.2f}")
    print("\n  Reservas registradas:")  # Lista de reservas
    for reserva in sistema.listar("reservas"):  # Recorre las reservas
        print(f"   - {reserva}")  # Muestra cada una
    print(f"\n  Log de eventos: {ARCHIVO_LOG}")  # Ruta del log
    print("=" * 70)  # Línea decorativa
    log.info("=== Simulación finalizada sin interrupciones ===")  # Log final


if __name__ == "__main__":  # Solo se ejecuta si se corre este archivo directamente
    main()  # Llama a la función principal

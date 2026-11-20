# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 – Prácticas simuladas** del curso Programación (213023), UNAD.

Sistema orientado a objetos en Python, **sin base de datos**, que gestiona clientes, servicios
(salas, alquiler de equipos y asesorías) y reservas, con manejo avanzado de excepciones y
registro de eventos en un archivo de logs.

## Cómo ejecutarlo

Requiere Python 3.8 o superior. No necesita librerías externas.

```bash
python main.py
```

Al terminar se crea el archivo `logs/software_fj.log` con todos los eventos y errores.

## Estructura del proyecto

| Archivo | Contenido | Responsable |
|---|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas | Integrante 1 |
| `logger.py` | Configuración del archivo de logs | Integrante 1 |
| `entidades.py` | Clase abstracta `EntidadBase` | Integrante 2 |
| `cliente.py` | Clase `Cliente` con validaciones y encapsulación | Integrante 2 |
| `servicios.py` | Clase abstracta `Servicio` + `ReservaSala`, `AlquilerEquipo`, `Asesoria` | Integrante 3 |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) | Integrante 4 |
| `sistema.py` | `GestorSoftwareFJ`: listas internas y control de errores | Integrante 5 |
| `main.py` | Simulación de 17 operaciones válidas e inválidas | Integrante 5 |

## Requisitos del enunciado y dónde se cumplen

| Requisito | Ubicación |
|---|---|
| Clase abstracta de entidades generales | `EntidadBase` en `entidades.py` |
| Cliente con validaciones y encapsulación | `cliente.py` (atributos privados + `@property`) |
| Servicio abstracto + 3 servicios derivados | `servicios.py` |
| Polimorfismo (métodos sobrescritos) | `costo_base`, `validar_parametros`, `describir` |
| Métodos sobrecargados | `Servicio.calcular_costo(horas, impuesto=None, descuento=None)` |
| Reserva con confirmación, cancelación y procesamiento | `reserva.py` |
| Excepciones personalizadas | `excepciones.py` (8 clases) |
| `try/except` | En todos los módulos |
| `try/except/else` | `Reserva.confirmar`, `GestorSoftwareFJ.registrar_cliente` |
| `try/except/finally` | `Reserva.procesar`, `GestorSoftwareFJ.crear_reserva`, `main.ejecutar` |
| Encadenamiento (`raise ... from ...`) | `Reserva.confirmar`, `Reserva.procesar`, `GestorSoftwareFJ.crear_servicio` |
| Archivo de logs | `logger.py` → `logs/software_fj.log` |
| Al menos 10 operaciones | `main.py` simula 17 |

## Flujo de trabajo en GitHub

1. Un integrante crea el repositorio y agrega a los demás como colaboradores.
2. Cada integrante clona el repositorio y crea su rama: `git checkout -b integrante-1`.
3. Sube sus archivos con commits claros, por ejemplo: `git commit -m "Agrega excepciones personalizadas"`.
4. Abre un *Pull Request* hacia `main`; otro integrante lo revisa y lo aprueba.
5. Al final, el integrante 5 ejecuta `main.py` con todo integrado y sube el log de evidencia.

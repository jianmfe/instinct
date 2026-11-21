# Instinct

**Instinct** es un entorno de simulación de criaturas autónomas controladas mediante un lenguaje de dominio específico (DSL) propio. Cada criatura ejecuta un programa que determina cómo percibe el entorno y cómo actúa dentro de un mundo organizado en una cuadrícula.

El proyecto combina un compilador desarrollado desde cero, un entorno de ejecución, un motor de simulación por turnos y una interfaz gráfica construida con **Python y Pygame CE**.

> **Estado del proyecto:** en desarrollo. El compilador, el runtime, el motor de simulación y una parte importante de la interfaz ya están implementados. La integración, las pruebas y la expansión de funcionalidades continúan en progreso.

## Contenido

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Recursos del mundo](#recursos-del-mundo)
- [Pruebas](#pruebas)
- [Documentación y seguimiento](#documentación-y-seguimiento)

## Características

### Lenguaje Instinct
- Lenguaje DSL propio para definir el comportamiento de las criaturas.
- Análisis léxico, sintáctico y semántico mediante componentes desarrollados para el proyecto.
- Generación y evaluación de un árbol de sintaxis abstracta (AST).
- Ejecución de instrucciones, condiciones, funciones y acciones mediante el runtime.

### Motor de simulación
- Mundo basado en una cuadrícula de casillas.
- Entidades diferenciadas: criaturas, terrenos y objetos.
- Sistema de acciones y percepciones para interactuar con el entorno.
- Simulación organizada en ticks.
- Gestión de eventos producidos durante la ejecución.
- Aplicación de reglas naturales del mundo.

### Interfaz gráfica
- Aplicación gráfica desarrollada con Pygame CE.
- Menú principal y escena de simulación.
- Renderizado de terrenos, objetos y criaturas.
- Cámara con desplazamiento y zoom.
- Animaciones visuales vinculadas a los eventos y acciones de las criaturas.
- Paneles de información, controles de simulación y registro de eventos.

La interfaz representa visualmente el estado del motor; la lógica de comportamiento y las reglas de simulación pertenecen al núcleo del proyecto.

## Arquitectura

El código fuente se organiza como un paquete Python dentro de `src/instinct/`.

```text
instinct/
├── resources/
│   ├── creatures/       # Programas de criaturas (.ins)
│   ├── maps/            # Definiciones de mapas (.map)
│   ├── objects/         # Definiciones de objetos (.ob)
│   └── terrains/        # Definiciones de terrenos (.te)
├── docs/
│   ├── instinct.pdf     # Documento de orientación del proyecto
│   └── PROGRESS.md      # Seguimiento del desarrollo
├── src/
│   └── instinct/
│       ├── actions/     # Acciones disponibles para las criaturas
│       ├── backend/     # Lexer, parser, AST y análisis semántico
│       ├── engine/      # Simulación, turnos, leyes y eventos
│       ├── frontend/    # Interfaz gráfica, escenas y renderizado
│       ├── functions/   # Funciones y operaciones registradas
│       ├── loaders/     # Carga y validación de recursos
│       ├── perceptions/ # Sensores y percepciones del entorno
│       ├── runtime/     # Entorno de ejecución e intérprete
│       ├── world/       # Entidades, casillas y cuadrícula
│       └── main.py      # Punto de entrada del paquete
├── tests/               # Pruebas automatizadas
├── pyproject.toml       # Configuración y dependencias
├── uv.lock
└── README.md
```

### Responsabilidades principales

| Módulo | Responsabilidad |
|---|---|
| `backend` | Convierte el código Instinct en una representación ejecutable y valida su estructura y semántica. |
| `runtime` | Ejecuta los programas y administra su contexto de ejecución. |
| `actions` | Define las acciones que las criaturas pueden realizar. |
| `perceptions` | Proporciona información del entorno y de la propia criatura. |
| `world` | Modela las entidades y la estructura espacial del mundo. |
| `engine` | Coordina los ticks, el orden de ejecución, las reglas naturales y los eventos. |
| `loaders` | Lee y valida las definiciones externas de criaturas, terrenos, objetos y mapas. |
| `frontend` | Presenta el mundo y sus estados mediante la interfaz gráfica. |

## Tecnologías

- **Python 3.13 o superior**
- **Pygame CE** para la interfaz gráfica.
- **uv** para la gestión del entorno y las dependencias.
- **pytest** para las pruebas automatizadas.

## Instalación

### Requisitos previos

Instala Python 3.13 o una versión compatible y [uv](https://docs.astral.sh/uv/).

Clona el repositorio:

```bash
git clone https://github.com/luisiafk/instinct.git
cd instinct
```

Crea y sincroniza el entorno del proyecto:

```bash
uv sync
```

## Ejecución

Inicia la aplicación gráfica desde la raíz del repositorio:

```bash
uv run python -m instinct.frontend.app
```

## Recursos del mundo

Los recursos de la simulación se definen mediante archivos de texto ubicados en `resources/`.

| Extensión | Recurso | Ubicación |
|---|---|---|
| `.ins` | Programa y comportamiento de una criatura | `resources/creatures/` |
| `.te` | Definición de un terreno | `resources/terrains/` |
| `.ob` | Definición de un objeto | `resources/objects/` |
| `.map` | Distribución de casillas del mapa | `resources/maps/` |

### Ejemplo de terreno

Archivo `resources/terrains/grass.te`:

```text
terrain Grass
char .
resource_max 100
regen 2
```

### Ejemplo de objeto

Archivo `resources/objects/rock.ob`:

```text
object Rock
char #
resource_max 100
```

### Mapas

Un archivo `.map` utiliza caracteres para referenciar los terrenos y objetos registrados. La primera línea identifica el mapa y las siguientes representan sus filas. Las filas deben mantener el mismo ancho.

Las criaturas se incorporan a la simulación por separado; no forman parte de la matriz de caracteres del mapa.

Los nombres, campos y caracteres de los recursos deben respetar las definiciones y validaciones del cargador correspondiente.

## Pruebas

Ejecuta la suite disponible con:

```bash
uv run pytest
```

Para ejecutar específicamente las pruebas del compilador:

```bash
uv run pytest tests/backend/test_compiler.py -v
```

La cobertura de pruebas continúa en desarrollo. Que una prueba individual pase no implica que todos los módulos o los flujos completos de la aplicación estén validados.

## Documentación y seguimiento

- **[Seguimiento del desarrollo](docs/PROGRESS.md):** funcionalidades completadas, trabajo en curso, pendientes y verificaciones.
- **[Documento de orientación](docs/instinct.pdf):** referencia general del proyecto.

El tracker es el documento de referencia para actualizar el estado del desarrollo. Este README debe mantenerse centrado en explicar el proyecto y cómo utilizarlo.

---

Desarrollado con Python, curiosidad y mucho Instinct.

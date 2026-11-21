# Instinct — Seguimiento del desarrollo

> Documento vivo. Actualizar este archivo al cerrar una tarea, descubrir un problema o cambiar una decisión técnica.
>
> **Última actualización:** 21 de noviembre de 2026  
> **Estado general:** desarrollo activo.

## Cómo leer este tracker

- [x] **Completado:** implementado y comprobado en el flujo de trabajo actual.
- [ ] **Pendiente:** todavía no implementado.
- [~] **En progreso:** implementación iniciada, pero no cerrada.
- [?] **Por verificar:** existe o se ha trabajado, pero falta una validación suficiente.

No marcar una tarea como completada únicamente porque el código exista: cuando corresponda, también debe probarse su comportamiento.

---

## 1. Lenguaje y compilador

- [x] Lexer y definición de tokens.
- [x] Parser y construcción del AST.
- [x] Analizador semántico.
- [x] Integración del compilador.
- [x] Correcciones de expresiones lógicas, identificadores, etiquetas e instrucciones inválidas realizadas durante la auditoría.
- [x] Validación de llamadas a funciones y acciones dentro del trabajo de corrección.
- [?] Revisión integral de casos límite del lexer.
- [?] Ampliar las pruebas unitarias del lexer.
- [?] Ampliar las pruebas unitarias del parser.
- [?] Ampliar las pruebas unitarias del análisis semántico.
- [ ] Documentar formalmente la gramática y las reglas del lenguaje.
- [ ] Incorporar ejemplos completos y comentados de programas `.ins`.

## 2. Runtime y ejecución

- [x] Entorno de ejecución y contexto.
- [x] Intérprete de instrucciones del AST.
- [x] Representación del programa ejecutable.
- [x] Integración de acciones y funciones con el contexto de ejecución.
- [?] Pruebas unitarias completas del intérprete.
- [?] Pruebas de variables, flujo de control y llamadas.
- [?] Verificar errores de ejecución y sus mensajes en español.
- [ ] Documentar el ciclo completo: código fuente → compilación → ejecución.

## 3. Mundo y entidades

- [x] Modelo de entidades del mundo.
- [x] Terrenos, objetos, criaturas y casillas.
- [x] Cuadrícula con operaciones de consulta y modificación.
- [x] Separación entre terreno y ocupante de una casilla.
- [x] Cargadores de terrenos, objetos, mapas y criaturas.
- [x] Gestor central de recursos y validaciones de recursos base.
- [x] Formatos externos `.te`, `.ob`, `.map` y `.ins` en uso.
- [x] Acciones de interacción con recursos, incluyendo consumo y agotamiento de objetos.
- [?] Completar pruebas de integración de los cargadores.
- [?] Verificar casos de recursos inválidos, referencias inexistentes y mapas mal formados.
- [ ] Documentar todos los campos admitidos por cada formato de recurso.
- [ ] Ampliar el catálogo de terrenos, objetos y mapas de prueba.

## 4. Motor de simulación

- [x] Simulación organizada por ticks.
- [x] Gestión del orden de ejecución de criaturas.
- [x] Aplicación de leyes naturales.
- [x] Sistema de eventos de acciones.
- [x] Registro de eventos.
- [x] Integración de acciones, percepciones y runtime.
- [?] Pruebas integrales de varios ticks con múltiples criaturas.
- [?] Verificar interacciones simultáneas y cambios del mundo durante un tick.
- [ ] Auditar los casos límite del ciclo de vida de las criaturas.
- [ ] Documentar el orden exacto de procesamiento de cada tick.

## 5. Frontend y experiencia visual

### Base de la aplicación
- [x] Aplicación Pygame CE.
- [x] Configuración de ventana y FPS.
- [x] Gestor de escenas.
- [x] Menú principal.
- [x] Navegación entre menú y escena de simulación.
- [x] Salida de la aplicación.

### Mundo y cámara
- [x] Renderizado de cuadrícula y terrenos.
- [x] Renderizado de objetos.
- [x] Renderizado de criaturas.
- [x] Selección de casillas y criaturas.
- [x] Cámara con desplazamiento y zoom.
- [x] Corrección del grosor de selección para zoom decimal.
- [x] Seguimiento de la criatura seleccionada implementado.
- [x] Interpolación visual del movimiento entre casillas.
- [?] Verificar seguimiento de cámara durante selección, muerte y cambio de criatura.
- [?] Revisar el comportamiento de la cámara al combinar seguimiento y desplazamiento manual.

### Animaciones
- [x] Máquina de estados visual por instancia de criatura.
- [x] Adaptador de eventos del motor a estados visuales.
- [x] Configuración de animaciones por especie.
- [x] Animación idle de Naruto.
- [x] Animación de movimiento.
- [x] Interpolación de movimiento vinculada a los eventos reales del motor.
- [x] Ajuste de velocidades visuales de caminar y correr.
- [~] Completar y verificar los estados especiales: ataque, daño, muerte y rugido.
- [ ] Completar animaciones adicionales que correspondan a las acciones soportadas.
- [ ] Verificar el fallback cuando una especie no tiene una animación configurada.
- [ ] Incorporar y validar spritesheets de las demás criaturas.

### Interfaz de simulación (HUD)
- [x] Gestor de temas.
- [x] Barra superior con información de simulación.
- [x] Panel de criaturas.
- [x] Tarjeta de estadísticas de criatura.
- [x] Panel de eventos.
- [x] Controles de pausa, avance manual y velocidad.
- [x] Widgets de interfaz reutilizables.
- [x] Panel de información de casilla, terreno y objeto.
- [x] Visualización de descripción y reserva del objeto en el panel contextual.
- [?] Revisar adaptación del HUD a diferentes resoluciones.
- [?] Revisar desbordamiento de textos y contenido en paneles.
- [ ] Completar ventanas de inspección y herramientas de código.
- [ ] Pulir la experiencia de creación y configuración de una nueva simulación.

## 6. Recursos gráficos

- [x] Definir especificaciones de tiles de terreno: PNG RGBA de 32×32 px, pixel art nítido y sin antialiasing.
- [x] Definir especificaciones de spritesheets: PNG RGBA con transparencia y frames de 64×64 px.
- [x] Integrar recursos de terreno y objetos en el renderizado.
- [x] Integrar spritesheet de Naruto para la animación idle y movimiento.
- [~] Completar el conjunto de animaciones de Naruto.
- [~] Completar los recursos visuales del entorno de Konoha.
- [ ] Revisar consistencia visual de escala, iluminación y estilo entre todos los recursos.
- [ ] Validar que las rutas y nombres de los assets coincidan con la configuración de cada especie.

## 7. Calidad, integración y pruebas

- [x] Configurar `uv` como gestor del entorno.
- [x] Incorporar Pygame CE.
- [x] Ejecutar y superar las pruebas del compilador realizadas durante la corrección.
- [x] Comprobar manualmente el arranque de la aplicación y la navegación básica.
- [x] Comprobar manualmente el movimiento interpolado y ajustar su velocidad.
- [~] Auditoría general del backend.
- [ ] Ejecutar la suite completa de pruebas y corregir los fallos encontrados.
- [ ] Completar pruebas de integración entre compilador, runtime, motor y frontend.
- [ ] Revisar imports, dependencias y módulos sin uso.
- [ ] Verificar que todos los mensajes de error visibles estén en español.
- [ ] Establecer una verificación de regresión antes de integrar cambios importantes.

## 8. Orden de trabajo recomendado

Este orden prioriza cerrar la experiencia de simulación antes de ampliar el alcance:

1. [ ] Terminar y probar los estados de animación pendientes.
2. [ ] Cerrar los detalles de HUD, paneles y cámara.
3. [ ] Completar el flujo de creación y configuración de simulaciones.
4. [ ] Integrar y probar varios programas de criaturas en un mismo mapa.
5. [ ] Completar pruebas de integración del backend y del motor.
6. [ ] Auditar el frontend completo y corregir regresiones.
7. [ ] Documentar la sintaxis del lenguaje y los formatos de recursos.
8. [ ] Ampliar mapas, criaturas, objetos y contenido visual.

## 9. Registro de cambios relevantes

| Fecha | Cambio |
|---|---|
| 2026-11-18 | Correcciones del compilador, lexer, parser y análisis semántico durante la auditoría. |
| 2026-11-18 | Revisión de la arquitectura y separación de responsabilidades del proyecto. |
| 2026-11-20 | Integración y pruebas iniciales de la interfaz con Pygame CE. |
| 2026-11-20 | Integración de terrenos, objetos, sprites y animaciones. |
| 2026-11-20 | Implementación y ajuste de movimiento visual interpolado. |
| 2026-11-21 | Avance del HUD, selección y panel contextual de información. |

---

## Criterio para cerrar tareas

Antes de marcar una tarea como completada:

1. Implementar el cambio sin duplicar responsabilidades existentes.
2. Probar el flujo afectado.
3. Ejecutar las pruebas automatizadas relevantes.
4. Comprobar que no se hayan introducido regresiones.
5. Actualizar este tracker con el resultado real.

**Nota:** este documento refleja el estado conocido durante el desarrollo. Las tareas marcadas como «por verificar» no deben considerarse terminadas hasta completar sus pruebas.

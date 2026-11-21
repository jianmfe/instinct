# Instinct — Seguimiento del desarrollo

> Documento vivo. Actualizar al cerrar tareas, descubrir problemas o cambiar decisiones técnicas.
>
> **Última actualización:** 21 de noviembre de 2026  
> **Estado general:** núcleo funcional; auditoría de integración visual realizada con hallazgos pendientes de corrección.

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
- [x] Correcciones de expresiones lógicas, identificadores, etiquetas e instrucciones inválidas.
- [x] Validación de llamadas a funciones y acciones.
- [x] Revisión de tipos y reglas del lenguaje dentro de la auditoría realizada.
- [ ] Documentar formalmente la gramática y las reglas del lenguaje.
- [ ] Incorporar ejemplos completos y comentados de programas `.ins`.
- [?] Ampliar los casos límite y la cobertura unitaria de lexer, parser y análisis semántico.

## 2. Runtime y ejecución

- [x] Entorno de ejecución y contexto.
- [x] Intérprete de instrucciones del AST.
- [x] Representación del programa ejecutable.
- [x] Integración de acciones y funciones con el contexto de ejecución.
- [x] Corrección de acceso y asignación de variables del entorno.
- [?] Ampliar pruebas unitarias completas del intérprete.
- [?] Probar variables, flujo de control y llamadas en escenarios complejos.
- [ ] Documentar el ciclo completo: código fuente → compilación → ejecución.

## 3. Mundo y entidades

- [x] Modelo de entidades del mundo.
- [x] Terrenos, objetos, criaturas y casillas.
- [x] Cuadrícula con operaciones de consulta y modificación.
- [x] Separación entre terreno y ocupante de una casilla.
- [x] Cargadores de terrenos, objetos, mapas y criaturas.
- [x] Gestor central de recursos y validaciones de recursos base.
- [x] Formatos externos `.te`, `.ob`, `.map` y `.ins` en uso.
- [x] Acciones de interacción con recursos, incluyendo consumo.
- [?] Ampliar pruebas de integración de los cargadores y recursos inválidos.
- [ ] Documentar todos los campos admitidos por cada formato.
- [ ] Ampliar el catálogo de terrenos, objetos y mapas de prueba.

## 4. Motor de simulación

- [x] Simulación organizada por ticks.
- [x] Gestión del orden de ejecución de criaturas.
- [x] Aplicación de leyes naturales.
- [x] Sistema de eventos de acciones.
- [x] Registro de eventos.
- [x] Integración de acciones, percepciones y runtime.
- [x] Corrección de la acción `consume` para publicar eventos de consumo y daño al consumir criaturas.
- [x] Pruebas automatizadas de los eventos de acciones.
- [ ] Completar la publicación de eventos visuales para las muertes producidas por leyes naturales.
- [?] Pruebas integrales de varios ticks con múltiples criaturas.
- [ ] Documentar el orden exacto de procesamiento de cada tick.

## 5. Frontend y experiencia visual

### Base de la aplicación

- [x] Aplicación Pygame CE.
- [x] Configuración de ventana y FPS.
- [x] Gestor de escenas.
- [x] Menú principal.
- [x] Navegación entre menú y escena de simulación.
- [x] Salida de la aplicación.
- [x] Punto de entrada compatible mediante `uv run instinct`.
- [x] Verificación de equivalencia entre `uv run instinct` y `uv run python -m instinct.frontend.app`.

### Mundo y cámara

- [x] Renderizado de cuadrícula, terrenos y objetos.
- [x] Renderizado de criaturas.
- [x] Selección de casillas y criaturas.
- [x] Cámara con desplazamiento y zoom decimal.
- [x] Seguimiento de la criatura seleccionada implementado.
- [x] Interpolación visual del movimiento entre casillas.
- [x] Corrección del grosor del borde de selección para zoom decimal.
- [ ] Revisar la interacción entre seguimiento automático y desplazamiento manual de cámara.
- [ ] Alinear el indicador de selección con la posición visual interpolada de la criatura.
- [?] Verificar seguimiento de cámara durante selección, muerte y cambio de criatura.

### Animaciones

- [x] Máquina de estados visual por instancia de criatura.
- [x] Adaptador de eventos del motor a estados visuales.
- [x] Configuración de animaciones por especie.
- [x] Animación idle de Naruto.
- [x] Animaciones de caminar y correr.
- [x] Interpolación de movimiento vinculada a eventos reales del motor.
- [x] Ajuste de velocidades visuales de caminar y correr.
- [x] Animaciones/recursos de ataque, consumo, muerte y rugido presentes en la carpeta de Naruto.
- [ ] Corregir el nombre de archivo asociado al estado `HURT`: la configuración busca `hurt.png`, pero el recurso existente se llama `damage.png`.
- [ ] Restaurar el estado de movimiento cuando una animación `HURT` termina mientras todavía queda movimiento interpolado pendiente.
- [ ] Añadir o definir el recurso de `REPRODUCE` para Naruto; actualmente no existe `reproduce.png`.
- [ ] Añadir transición visual de muerte para criaturas retiradas por las leyes naturales.
- [ ] Definir el comportamiento de las animaciones mientras la simulación está pausada.
- [ ] Verificar fallback a `IDLE` cuando falte una spritesheet de una especie.
- [ ] Incorporar y validar spritesheets de otras criaturas.

### Interfaz de simulación (HUD)

- [x] Gestor de temas.
- [x] Barra superior con información de simulación.
- [x] Panel de criaturas y tarjeta de estadísticas.
- [x] Panel de eventos.
- [x] Controles de pausa, avance manual y velocidad.
- [x] Widgets reutilizables.
- [x] Panel de información de casilla, terreno y objeto.
- [?] Revisar adaptación del HUD a diferentes resoluciones.
- [?] Revisar desbordamiento de textos y contenido en paneles.
- [ ] Completar ventanas de inspección y herramientas de código.
- [ ] Pulir la experiencia de creación y configuración de una nueva simulación.

---

## 6. Recursos gráficos

- [x] Especificación de tiles: PNG RGBA de 32×32 px, pixel art nítido y sin antialiasing.
- [x] Especificación de spritesheets: PNG RGBA con transparencia y frames de 64×64 px.
- [x] Integración de recursos de terreno y objetos.
- [x] Integración de spritesheets de Naruto para los estados ya disponibles.
- [x] Organización de spritesheets dentro de la carpeta de cada criatura.
- [~] Completar recursos visuales de Naruto, incluyendo los estados pendientes.
- [~] Completar los recursos visuales del entorno de Konoha.
- [ ] Revisar consistencia de escala, iluminación y estilo.
- [ ] Validar rutas, nombres y metadatos de todos los assets.

## 7. Calidad, integración y pruebas

### Verificaciones cerradas

- [x] Configuración de `uv`.
- [x] Incorporación de Pygame CE.
- [x] Ambos puntos de entrada de la aplicación comprobados.
- [x] Suite completa de pruebas: **30 passed**.
- [x] Ruff: `uv run ruff check src tests` — **All checks passed**.
- [x] Mypy: `uv run mypy src` — **Success, no issues found in 107 source files**.

### Auditoría de frontend — 21/11/2026

- [x] Revisar `ActionEvent` y `ActionEventLog`.
- [x] Revisar publicación de eventos en acciones de movimiento, ataque, daño, consumo y muerte.
- [x] Revisar `EventAdapter` y el cursor de lectura.
- [x] Revisar prioridades y transiciones de la FSM.
- [x] Revisar cola de movimientos e interpolación.
- [x] Revisar reproducción y selección de spritesheets.
- [x] Revisar integración con `SimulationScene`, cámara, selección y HUD.
- [x] Revisar control de pausa, avance manual y velocidad.
- [~] Corregir los hallazgos funcionales identificados:
  1. Las muertes por desgaste de vida o esperanza de vida no publican `ActionEvent`; la criatura desaparece sin animación `DEATH`.
  2. El estado `HURT` intenta cargar `hurt.png`, pero Naruto dispone de `damage.png`.
  3. Si `HURT` finaliza antes que un movimiento pendiente, la FSM vuelve a `IDLE` mientras el desplazamiento continúa.
  4. El indicador de selección utiliza la posición lógica, no la posición visual interpolada.
  5. La pausa detiene los ticks, pero no congela la actualización de animaciones e interpolación.
  6. No existe todavía un recurso `reproduce.png` para Naruto.
- [ ] Repetir pruebas automatizadas después de corregir los hallazgos.
- [ ] Ejecutar pruebas manuales de muerte natural, daño durante movimiento, pausa durante movimiento y reproducción.

## 8. Orden de trabajo recomendado

1. [ ] Corregir la publicación y visualización de muertes naturales.
2. [ ] Corregir el nombre del recurso de daño y verificar la animación `HURT`.
3. [ ] Corregir la transición de `HURT` cuando hay movimiento pendiente.
4. [ ] Resolver la sincronización del indicador de selección con el sprite.
5. [ ] Definir y aplicar el comportamiento de pausa para animaciones e interpolación.
6. [ ] Completar el recurso de reproducción si se mantiene ese estado visual.
7. [ ] Repetir Ruff, Mypy y pytest.
8. [ ] Continuar con pruebas de integración de varias criaturas en un mismo mapa.
9. [ ] Documentar la sintaxis del lenguaje y los formatos de recursos.
10. [ ] Ampliar mapas, criaturas, objetos y contenido visual.

## 9. Registro de cambios relevantes

| Fecha | Cambio |
|---|---|
| 2026-11-18 | Correcciones del compilador, lexer, parser y análisis semántico. |
| 2026-11-18 | Revisión de arquitectura y separación de responsabilidades. |
| 2026-11-20 | Integración inicial de la interfaz con Pygame CE. |
| 2026-11-20 | Integración de terrenos, objetos, sprites y animaciones. |
| 2026-11-20 | Implementación y ajuste de movimiento visual interpolado. |
| 2026-11-21 | Avance del HUD, selección y panel contextual de información. |
| 2026-11-21 | Punto de entrada `uv run instinct` verificado junto al módulo de aplicación. |
| 2026-11-21 | Suite completa: 30 pruebas aprobadas; Ruff y Mypy sin errores. |
| 2026-11-21 | Auditoría del flujo de eventos y animaciones: hallazgos registrados para la siguiente sesión. |

---

## Criterio para cerrar tareas

Antes de marcar una tarea como completada:

1. Implementar el cambio sin duplicar responsabilidades existentes.
2. Probar el flujo afectado.
3. Ejecutar las pruebas automatizadas relevantes.
4. Comprobar que no se hayan introducido regresiones.
5. Actualizar este tracker con el resultado real.

**Nota:** este documento refleja el estado conocido al 21 de noviembre de 2026. Los hallazgos de auditoría están registrados como pendientes; no deben considerarse corregidos hasta implementar y probar sus soluciones.

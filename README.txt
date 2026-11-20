# Parche de animaciones de Instinct

Copia el contenido de `src/` sobre el `src/` de tu proyecto, conservando la estructura.

Archivos incluidos:
- frontend/animation/animation_state.py
- frontend/animation/animation_state_machine.py
- frontend/animation/animation_controller.py
- frontend/animation/animations_config.py
- frontend/animation/event_adapter.py
- frontend/world_view/creature_renderer.py
- frontend/scenes/simulation_scene.py

Las spritesheets se buscan en:
`src/instinct/frontend/assets/creatures/sprites/<especie>/<estado>.png`

Estados esperados: idle, walk, run, attack, hurt, death, roar, consume, reproduce.

La configuración predeterminada supone 4 fotogramas para idle, 6 para walk/run/attack/death,
3 para hurt y 5 para roar/consume/reproduce. Ajusta `AnimationConfig.register(...)`
si alguna spritesheet tiene otra cantidad de fotogramas.

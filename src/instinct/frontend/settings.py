
# Configuración general de Instinct

# Ventana
WINDOW_TITLE = "Instinct"
DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
WINDOW_WIDTH = DESIGN_WIDTH
WINDOW_HEIGHT = DESIGN_HEIGHT

RESIZABLE = True
FULLSCREEN = False

# Renderizado
TARGET_FPS = 60

# Simulación
DEFAULT_SIMULATION_SPEED = 1.0

SIMULATION_SPEEDS = (
    0.5,
    1.0,
    2.0,
    4.0,
    8.0,
)

# Colores generales
DARK_THEME = {
    "background": (17, 22, 41),
    "panel": (41, 39, 71),
    "accent": (118, 84, 168),
    "gold": (212, 174, 98),
    "text": (242, 239, 250),
    "secondary_text": (170, 166, 190),
}

LIGHT_THEME = {
    "background": (238, 232, 217),
    "panel": (216, 208, 194),
    "accent": (118, 84, 168),
    "gold": (178, 139, 67),
    "text": (41, 39, 71),
    "secondary_text": (105, 99, 117),
}

DEFAULT_THEME = "dark"

# Cámara
DEFAULT_TILE_SIZE = 32
MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
DEFAULT_ZOOM = 1.0

# Recursos
ASSETS_DIR = "src/instinct/frontend/assets"

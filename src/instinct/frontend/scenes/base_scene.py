
class BaseScene:
    """Interfaz base para todas las escenas de Instinct."""

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        """Procesa eventos de entrada."""

    def update(self, dt):
        """Actualiza el estado de la escena."""

    def draw(self, screen):
        """Dibuja la escena."""

    def on_enter(self):
        """Se ejecuta al entrar en la escena."""

    def on_exit(self):
        """Se ejecuta al abandonar la escena."""

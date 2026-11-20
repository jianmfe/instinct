
class BaseScene:
    """Interfaz base para todas las escenas de Instinct."""

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        """Procesa eventos de entrada."""
        pass

    def update(self, dt):
        """Actualiza el estado de la escena."""
        pass

    def draw(self, screen):
        """Dibuja la escena."""
        pass

    def on_enter(self):
        """Se ejecuta al entrar en la escena."""
        pass

    def on_exit(self):
        """Se ejecuta al abandonar la escena."""
        pass


class SceneManager:
    """Administra las escenas de la aplicación."""

    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def change_scene(self, new_scene):
        """Cambia la escena activa."""

        if self.current_scene is not None:
            self.current_scene.on_exit()

        self.current_scene = new_scene
        self.current_scene.on_enter()

    def handle_event(self, event):
        if self.current_scene is not None:
            self.current_scene.handle_event(event)

    def update(self, dt):
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene is not None:
            self.current_scene.draw(screen)

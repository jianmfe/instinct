
from instinct.frontend.settings import DARK_THEME, LIGHT_THEME


class ThemeManager:
    """Administra los temas visuales de Instinct."""

    def __init__(self, initial_theme="dark"):
        self.themes = {
            "dark": DARK_THEME,
            "light": LIGHT_THEME,
        }

        self.current_theme = initial_theme

    @property
    def colors(self):
        return self.themes[self.current_theme]

    def set_theme(self, theme_name):
        if theme_name not in self.themes:
            raise ValueError(
                f"Tema desconocido: {theme_name}"
            )

        self.current_theme = theme_name

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.set_theme("light")
        else:
            self.set_theme("dark")

    def get_color(self, color_name):
        return self.colors.get(color_name)

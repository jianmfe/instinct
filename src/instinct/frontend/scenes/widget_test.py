
import pygame

from instinct.frontend.interface.theme_manager import ThemeManager
from instinct.frontend.interface.widgets.button import Button
from instinct.frontend.interface.widgets.checkbox import Checkbox
from instinct.frontend.interface.widgets.dropdown import Dropdown
from instinct.frontend.interface.widgets.label import Label
from instinct.frontend.interface.widgets.panel import Panel
from instinct.frontend.interface.widgets.scroll_panel import ScrollPanel
from instinct.frontend.interface.widgets.slider import Slider
from instinct.frontend.scenes.base_scene import BaseScene


class WidgetTestScene(BaseScene):
    """Escena temporal para probar los componentes de interfaz."""

    def __init__(self, game):
        super().__init__(game)

        self.theme_manager = ThemeManager()
        self.font = pygame.font.Font(None, 32)

        self._build_widgets()

    def _build_widgets(self):
        colors = self.theme_manager.colors

        self.background = colors["background"]
        self.text_color = colors["text"]
        self.secondary_color = colors["secondary_text"]

        self.panel = Panel(
            (100, 130, 1720, 820),
            background=colors["panel"],
            border_color=colors["accent"],
        )

        self.title = Label(
            "PRUEBA DE COMPONENTES - INSTINCT",
            font_size=55,
            color=colors["gold"],
            align="center",
        )

        self.button = Button(
            (150, 250, 300, 65),
            "Boton de prueba",
            callback=self._button_clicked,
            background=colors["background"],
            hover_color=colors["accent"],
            text_color=colors["text"],
            border_color=colors["gold"],
        )

        self.theme_button = Button(
            (150, 340, 300, 65),
            "Cambiar tema",
            callback=self._toggle_theme,
            background=colors["background"],
            hover_color=colors["accent"],
            text_color=colors["text"],
            border_color=colors["gold"],
        )

        self.slider_value = 50

        self.slider = Slider(
            (550, 280, 400, 12),
            minimum=0,
            maximum=100,
            value=self.slider_value,
            callback=self._slider_changed,
            track_color=colors["background"],
            fill_color=colors["accent"],
            knob_color=colors["gold"],
        )

        self.dropdown = Dropdown(
            (550, 420, 400, 45),
            options=[
                "Bosque",
                "Desierto",
                "Montaña",
                "Pantano",
                "Llanura",
            ],
            callback=self._biome_changed,
            background=colors["background"],
            text_color=colors["text"],
            accent=colors["gold"],
        )

        self.checkbox_value = False

        self.checkbox = Checkbox(
            (550, 550, 350, 30),
            "Mostrar cuadrícula",
            callback=self._checkbox_changed,
            box_color=colors["gold"],
            text_color=colors["text"],
        )

        self.scroll_panel = ScrollPanel(
            (1100, 250, 550, 550),
            background=colors["background"],
        )

        self.scroll_panel.set_content_height(1000)

        self.message = "Interfaz lista para probar."

    def _button_clicked(self):
        self.message = "¡El botón funciona correctamente!"

    def _toggle_theme(self):
        self.theme_manager.toggle_theme()
        self._build_widgets()

    def _slider_changed(self, value):
        self.slider_value = round(value, 1)

    def _biome_changed(self, biome):
        self.message = f"Bioma seleccionado: {biome}"

    def _checkbox_changed(self, checked):
        self.checkbox_value = checked

    def handle_event(self, event):
        self.button.handle_event(event)
        self.theme_button.handle_event(event)
        self.slider.handle_event(event)
        self.dropdown.handle_event(event)
        self.checkbox.handle_event(event)
        self.scroll_panel.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from instinct.frontend.scenes.main_menu import MainMenu

            self.game.scene_manager.change_scene(
                MainMenu(self.game)
            )

    def draw(self, screen):
        screen.fill(self.background)

        self.panel.draw(screen)

        self.title.draw(
            screen,
            (960, 175),
        )

        self.button.draw(screen)
        self.theme_button.draw(screen)

        Label(
            "Slider: " + str(self.slider_value),
            30,
            self.text_color,
        ).draw(screen, (550, 230))

        self.slider.draw(screen)

        Label(
            "Seleccion de bioma",
            30,
            self.text_color,
        ).draw(screen, (550, 380))

        self.dropdown.draw(screen)
        self.checkbox.draw(screen)

        Label(
            "Registro de prueba",
            30,
            self.text_color,
        ).draw(screen, (1100, 210))

        def draw_messages(surface):
            for index in range(20):
                message = self.font.render(
                    f"Evento de prueba numero {index + 1}",
                    True,
                    self.text_color,
                )

                surface.blit(
                    message,
                    (15, 15 + index * 45),
                )

        self.scroll_panel.draw(
            screen,
            draw_messages,
        )

        Label(
            self.message,
            28,
            self.secondary_color,
        ).draw(screen, (150, 700))

        Label(
            "ESC: volver al menu",
            25,
            self.secondary_color,
        ).draw(screen, (150, 900))

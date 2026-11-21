
import pygame

from instinct.frontend.interface.widgets.button import Button
from instinct.frontend.interface.widgets.slider import Slider


class SimulationControls:
    """Controles principales de ejecución de la simulación."""

    def __init__(self, rect, controller, theme_manager):
        self.rect = pygame.Rect(rect)
        self.controller = controller
        self.theme_manager = theme_manager

        self.speeds = list(controller.SPEEDS)

        self.info_font = pygame.font.Font(None, 23)
        self.speed_font = pygame.font.Font(None, 28)
        self.mark_font = pygame.font.Font(None, 19)

        self.play_button = None
        self.step_button = None
        self.speed_slider = None

        self._create_controls()

    def _create_controls(self):
        colors = self.theme_manager.colors

        button_y = self.rect.y + 20
        button_height = 42

        self.play_button = Button(
            pygame.Rect(
                self.rect.x + 15,
                button_y,
                130,
                button_height,
            ),
            "Reanudar",
            callback=self._toggle_pause,
            font_size=25,
        )

        self.step_button = Button(
            pygame.Rect(
                self.rect.x + 160,
                button_y,
                130,
                button_height,
            ),
            "Avanzar tick",
            callback=self._step,
            font_size=25,
        )

        current_index = min(
            range(len(self.speeds)),
            key=lambda index: abs(
                self.speeds[index] - self.controller.speed
            ),
        )

        slider_rect = pygame.Rect(
            self.rect.x + 365,
            button_y + 18,
            max(100, self.rect.width - 395),
            8,
        )

        self.speed_slider = Slider(
            slider_rect,
            minimum=0,
            maximum=len(self.speeds) - 1,
            value=current_index,
            steps=list(range(len(self.speeds))),
            callback=self._set_speed_index,
            track_color=colors["secondary_text"],
            fill_color=colors["accent"],
            knob_color=colors["gold"],
        )

    def _toggle_pause(self):
        self.controller.toggle_pause()

    def _step(self):
        self.controller.step()

    def _set_speed_index(self, index):
        index = int(index)
        speed = self.speeds[index]

        self.controller.set_speed(speed)

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

        button_y = self.rect.y + 20

        self.play_button.rect.topleft = (
            self.rect.x + 15,
            button_y,
        )

        self.step_button.rect.topleft = (
            self.rect.x + 160,
            button_y,
        )

        self.speed_slider.rect = pygame.Rect(
            self.rect.x + 365,
            button_y + 18,
            max(100, self.rect.width - 395),
            8,
        )

    def handle_event(self, event):
        if self.play_button.handle_event(event):
            return True

        if self.step_button.handle_event(event):
            return True

        if self.speed_slider.handle_event(event):
            return True

        return False

    def draw(self, screen):
        colors = self.theme_manager.colors

        pygame.draw.rect(
            screen,
            colors["panel"],
            self.rect,
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            colors["accent"],
            self.rect,
            width=2,
            border_radius=12,
        )

        self.play_button.text = (
            "Reanudar"
            if self.controller.paused
            else "Pausar"
        )

        self.play_button.draw(screen)
        self.step_button.draw(screen)

        # Información del selector de velocidad.
        label = self.info_font.render(
            "VELOCIDAD",
            True,
            colors["secondary_text"],
        )

        screen.blit(
            label,
            (
                self.speed_slider.rect.x,
                self.rect.y + 7,
            ),
        )

        self.speed_slider.draw(screen)

        # Marcas de las velocidades disponibles.
        for index, speed in enumerate(self.speeds):
            ratio = (
                index / (len(self.speeds) - 1)
                if len(self.speeds) > 1
                else 0
            )

            x = int(
                self.speed_slider.rect.x
                + ratio * self.speed_slider.rect.width
            )

            text = self.mark_font.render(
                f"{speed:g}x",
                True,
                colors["secondary_text"],
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(x, self.rect.bottom - 12)
                ),
            )

        current_speed = self.speed_font.render(
            f"{self.controller.speed:g}x",
            True,
            colors["gold"],
        )

        screen.blit(
            current_speed,
            (
                self.speed_slider.rect.right + 12,
                self.speed_slider.rect.y - 9,
            ),
        )

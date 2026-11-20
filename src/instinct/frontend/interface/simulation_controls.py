import pygame

from instinct.frontend.interface.widgets.button import Button
from instinct.frontend.interface.widgets.dropdown import Dropdown


class SimulationControls:
    def __init__(self, rect, controller, theme_manager):
        self.rect = pygame.Rect(rect)
        self.controller = controller
        self.theme_manager = theme_manager

        colors = theme_manager.colors

        button_y = self.rect.y + 23
        button_height = 42

        self.play_button = Button(
            pygame.Rect(self.rect.x + 15, button_y, 130, button_height),
            "Reanudar",
            callback=self._toggle_pause,
            font_size=25,
        )

        self.step_button = Button(
            pygame.Rect(self.rect.x + 160, button_y, 130, button_height),
            "Avanzar tick",
            callback=self._step,
            font_size=25,
        )

        self.speed_dropdown = Dropdown(
            pygame.Rect(self.rect.x + 320, button_y, 130, button_height),
            options=list(controller.SPEEDS),
            selected=controller.speed,
            callback=self._set_speed,
            background=colors["panel"],
            text_color=colors["text"],
            accent=colors["accent"],
        )

        self.info_font = pygame.font.Font(None, 23)

    def _toggle_pause(self):
        self.controller.toggle_pause()

    def _step(self):
        self.controller.step()

    def _set_speed(self, speed):
        self.controller.set_speed(speed)

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

        button_y = self.rect.y + 23

        self.play_button.rect.topleft = (
            self.rect.x + 15,
            button_y,
        )

        self.step_button.rect.topleft = (
            self.rect.x + 160,
            button_y,
        )

        self.speed_dropdown.rect.topleft = (
            self.rect.x + 320,
            button_y,
        )

    def handle_event(self, event):
        mouse_position = getattr(event, "pos", None)

        if mouse_position is not None:
            dropdown_area = self.speed_dropdown.rect.union(
                pygame.Rect(
                    self.speed_dropdown.rect.x,
                    self.speed_dropdown.rect.bottom,
                    self.speed_dropdown.rect.width,
                    self.speed_dropdown.option_height * len(
                        self.speed_dropdown.options
                    ),
                )
            )

            if (
                self.speed_dropdown.opened
                and dropdown_area.collidepoint(mouse_position)
            ):
                self.speed_dropdown.handle_event(event)
                return True

        if self.play_button.rect.collidepoint(
            pygame.mouse.get_pos()
        ) or self.play_button.pressed:
            self.play_button.handle_event(event)
            return True

        if self.step_button.rect.collidepoint(
            pygame.mouse.get_pos()
        ) or self.step_button.pressed:
            self.step_button.handle_event(event)
            return True

        if self.speed_dropdown.rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            self.speed_dropdown.handle_event(event)
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
            "Reanudar" if self.controller.paused else "Pausar"
        )

        self.play_button.draw(screen)
        self.step_button.draw(screen)
        self.speed_dropdown.draw(screen)

        label = self.info_font.render(
            "VELOCIDAD",
            True,
            colors["secondary_text"],
        )

        screen.blit(
            label,
            (
                self.speed_dropdown.rect.x,
                self.speed_dropdown.rect.y - 17,
            ),
        )

import pygame


class Slider:
    """Control deslizante para valores numéricos."""

    def __init__(
        self,
        rect,
        minimum=0,
        maximum=100,
        value=50,
        callback=None,
        track_color=(65, 62, 90),
        fill_color=(118, 84, 168),
        knob_color=(212, 174, 98),
    ):
        self.rect = pygame.Rect(rect)

        self.minimum = minimum
        self.maximum = maximum
        self.value = max(minimum, min(maximum, value))

        self.callback = callback

        self.track_color = track_color
        self.fill_color = fill_color
        self.knob_color = knob_color

        self.dragging = False
        self.knob_radius = 9

    def _value_to_x(self):
        ratio = (self.value - self.minimum) / (
            self.maximum - self.minimum
        )

        return self.rect.x + ratio * self.rect.width

    def _update_value(self, mouse_x):
        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))

        new_value = self.minimum + ratio * (
            self.maximum - self.minimum
        )

        if new_value != self.value:
            self.value = new_value

            if self.callback:
                self.callback(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.inflate(0, 20).collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.track_color,
            self.rect,
            border_radius=5,
        )

        knob_x = int(self._value_to_x())

        fill_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            knob_x - self.rect.x,
            self.rect.height,
        )

        pygame.draw.rect(
            surface,
            self.fill_color,
            fill_rect,
            border_radius=5,
        )

        pygame.draw.circle(
            surface,
            self.knob_color,
            (knob_x, self.rect.centery),
            self.knob_radius,
        )

import pygame


class Slider:
    """Control deslizante con soporte para valores discretos."""

    def __init__(
        self,
        rect,
        minimum=0,
        maximum=100,
        value=50,
        callback=None,
        steps=None,
        track_color=(65, 62, 90),
        fill_color=(118, 84, 168),
        knob_color=(212, 174, 98),
    ):
        self.rect = pygame.Rect(rect)

        self.minimum = minimum
        self.maximum = maximum
        self.value = max(minimum, min(maximum, value))

        self.callback = callback
        self.steps = steps

        self.track_color = track_color
        self.fill_color = fill_color
        self.knob_color = knob_color

        self.dragging = False
        self.knob_radius = 9

    def _normalize_value(self, value):
        value = max(self.minimum, min(self.maximum, value))

        if self.steps:
            value = min(self.steps, key=lambda step: abs(step - value))

        return value

    def _value_to_x(self):
        if self.maximum == self.minimum:
            return self.rect.centerx

        ratio = (
            (self.value - self.minimum)
            / (self.maximum - self.minimum)
        )

        return self.rect.x + ratio * self.rect.width

    def _update_value(self, mouse_x):
        if self.rect.width <= 0:
            return

        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))

        new_value = self.minimum + ratio * (
            self.maximum - self.minimum
        )

        new_value = self._normalize_value(new_value)

        if new_value != self.value:
            self.value = new_value

            if self.callback:
                self.callback(self.value)

    def set_value(self, value, notify=False):
        new_value = self._normalize_value(value)

        if new_value == self.value:
            return

        self.value = new_value

        if notify and self.callback:
            self.callback(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hitbox = self.rect.inflate(0, 24)

            if hitbox.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
                return True

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
            return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True

        return False

    def draw(self, surface):
        track = self.rect.copy()
        track.height = 6
        track.centery = self.rect.centery

        pygame.draw.rect(
            surface,
            self.track_color,
            track,
            border_radius=5,
        )

        knob_x = int(self._value_to_x())

        fill_rect = pygame.Rect(
            track.x,
            track.y,
            max(0, knob_x - track.x),
            track.height,
        )

        pygame.draw.rect(
            surface,
            self.fill_color,
            fill_rect,
            border_radius=5,
        )

        if self.steps:
            for step in self.steps:
                ratio = (
                    (step - self.minimum)
                    / (self.maximum - self.minimum)
                    if self.maximum != self.minimum
                    else 0
                )

                tick_x = int(
                    self.rect.x + ratio * self.rect.width
                )

                pygame.draw.circle(
                    surface,
                    self.track_color,
                    (tick_x, self.rect.centery),
                    3,
                )

        pygame.draw.circle(
            surface,
            self.knob_color,
            (knob_x, self.rect.centery),
            self.knob_radius,
        )

        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (knob_x, self.rect.centery),
            self.knob_radius,
            2,
        )

import pygame


class CreatureCard:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 30)
        self.info_font = pygame.font.Font(None, 24)

    def draw(self, surface, creature, rect, colors):
        rect = pygame.Rect(rect)

        pygame.draw.rect(
            surface,
            colors["panel"],
            rect,
            border_radius=10,
        )

        pygame.draw.rect(
            surface,
            colors["accent"],
            rect,
            width=2,
            border_radius=10,
        )

        if creature is None:
            text = self.info_font.render(
                "Selecciona una criatura",
                True,
                colors["secondary_text"],
            )

            surface.blit(
                text,
                text.get_rect(center=rect.center),
            )
            return

        x = rect.x + 16
        y = rect.y + 16

        title = self.title_font.render(
            creature.name,
            True,
            colors["gold"],
        )

        surface.blit(title, (x, y))
        y += 42

        details = [
            f"Facción: {creature.faction}",
            f"Vida actual: {creature.health}",
            f"Visión: {creature.vision}",
            f"Edad: {creature.age}",
            f"Esperanza de vida: {creature.lifespan}",
            f"Posición: ({creature.x}, {creature.y})",
            f"Programa: {'Asignado' if creature.program else 'Sin programa'}",
        ]

        for detail in details:
            text = self.info_font.render(
                detail,
                True,
                colors["text"],
            )

            surface.blit(text, (x, y))
            y += 31
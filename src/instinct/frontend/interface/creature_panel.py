import pygame

from instinct.frontend.interface.creature_card import CreatureCard


class CreaturePanel:
    def __init__(self):
        self.card = CreatureCard()
        self.title_font = pygame.font.Font(None, 32)

    def draw(self, screen, rect, creatures, colors):
        rect = pygame.Rect(rect)

        pygame.draw.rect(
            screen,
            colors["panel"],
            rect,
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            colors["accent"],
            rect,
            width=2,
            border_radius=12,
        )

        title = self.title_font.render(
            "CRIATURA",
            True,
            colors["gold"],
        )

        screen.blit(
            title,
            (rect.x + 16, rect.y + 16),
        )

        selected = creatures[0] if creatures else None

        card_rect = pygame.Rect(
            rect.x + 10,
            rect.y + 62,
            rect.width - 20,
            rect.height - 75,
        )

        self.card.draw(
            screen,
            selected,
            card_rect,
            colors,
        )
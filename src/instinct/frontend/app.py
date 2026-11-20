
from instinct.frontend.core.game import Game
from instinct.frontend.scenes.main_menu import MainMenu


def main():
    game = Game()
    game.scene_manager.change_scene(MainMenu(game))
    game.run()


if __name__ == "__main__":
    main()

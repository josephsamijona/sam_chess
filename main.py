# chess_game/main.py

import pygame
import pygame_menu
from gui.board import ChessBoard

def start_the_game():
    """Démarre le jeu d'échecs."""
    board = ChessBoard()
    board.run()

def main():
    """Crée le menu principal et gère les événements."""
    pygame.init()
    surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Jeu d\'échecs')

    menu = pygame_menu.Menu('Bienvenue', 800, 600, theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Jouer', start_the_game)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        menu.update(events)
        menu.draw(surface)
        pygame.display.flip()

if __name__ == "__main__":
    main()

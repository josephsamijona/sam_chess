# chess_game/gui/pieces.py

import os
import pygame

def load_piece_images():
    """Charge les images des pièces d'échecs et les stocke dans un dictionnaire."""
    pieces = {}
    pieces_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'pieces')
    
    piece_names = [
        'W_Pawn', 'B_Pawn', 'W_Knight', 'B_Knight', 'W_Bishop', 'B_Bishop',
        'W_Rook', 'B_Rook', 'W_Queen', 'B_Queen', 'W_King', 'B_King'
    ]
    
    for piece in piece_names:
        pieces[piece] = pygame.image.load(os.path.join(pieces_path, f'{piece}.png'))
    
    return pieces

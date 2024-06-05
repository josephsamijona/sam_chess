import pygame
import os
import chess
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from gui.pieces import load_piece_images
from logic.game import ChessGame

def init_pygame():
    """Initialise Pygame et configure la fenêtre avec OpenGL."""
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, 8, 0, 8)

def draw_board(board_image):
    """Dessine l'échiquier en utilisant l'image de l'échiquier comme texture."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, board_image)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex2f(0.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex2f(8.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex2f(8.0, 8.0)
    glTexCoord2f(0.0, 1.0); glVertex2f(0.0, 8.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def load_texture(file):
    """Charge une image et la transforme en texture OpenGL."""
    image = pygame.image.load(file)
    image = pygame.transform.flip(image, False, True)
    image_data = pygame.image.tostring(image, "RGBA", 1)
    width, height = image.get_rect().size
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture

def draw_pieces(pieces, board):
    """Dessine les pièces d'échecs sur l'échiquier."""
    piece_size = 1
    piece_map = {
        'P': 'Pawn',
        'N': 'Knight',
        'B': 'Bishop',
        'R': 'Rook',
        'Q': 'Queen',
        'K': 'King'
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = 'W' if piece.color == chess.WHITE else 'B'
            piece_image = pieces[f'{color}_{piece_map[piece.symbol().upper()]}']
            col, row = chess.square_file(square), chess.square_rank(square)
            x, y = col, 7 - row
            glRasterPos2f(x + piece_size / 2, y + piece_size / 2)
            glDrawPixels(piece_image.get_width(), piece_image.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(piece_image, "RGBA", 1))

class ChessBoard:
    """Classe représentant l'échiquier d'un jeu d'échecs."""
    def __init__(self):
        self.board_image = None
        self.pieces = load_piece_images()
        self.chess_game = ChessGame()
        self.selected_square = None
        self.init_display()

    def init_display(self):
        """Initialise Pygame et charge la texture de l'échiquier."""
        init_pygame()
        assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'board.png')
        self.board_image = load_texture(assets_path)

    def handle_click(self, row, col):
        """Gère le clic de l'utilisateur sur l'échiquier."""
        square = chess.square(col, 7 - row)
        if self.selected_square is None:
            piece = self.chess_game.board.piece_at(square)
            if piece and piece.color == chess.WHITE:  # Assume that the user plays white
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if self.chess_game.make_move(move):
                self.selected_square = None
            else:
                self.selected_square = None  # Reset selection if move is illegal

    def run(self):
        """Boucle principale du jeu, gère les événements et le rendu."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = int(y // 100), int(x // 100)
                    self.handle_click(row, col)
            draw_board(self.board_image)
            draw_pieces(self.pieces, self.chess_game.board)
            pygame.display.flip()
            pygame.time.wait(100)

if __name__ == "__main__":
    board = ChessBoard()
    board.run()

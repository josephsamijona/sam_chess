# chess_game/logic/game.py

import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        """Effectue un mouvement si celui-ci est légal."""
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def get_legal_moves(self):
        """Retourne tous les mouvements légaux possibles."""
        return list(self.board.legal_moves)

    def is_game_over(self):
        """Vérifie si la partie est terminée."""
        return self.board.is_game_over()

    def get_board_fen(self):
        """Retourne la représentation FEN du plateau."""
        return self.board.fen()

    def reset_game(self):
        """Réinitialise le jeu."""
        self.board.reset()

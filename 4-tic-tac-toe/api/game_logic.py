# Initialisation du jeu
game_state = {
    'board': [[' ' for _ in range(8)] for _ in range(8)],
    'current_player': 1,  # 1 starts
    'winner': None,
}

def check_win(board, player):
    # Vérification horizontale, verticale et diagonale
    for row in range(8):
        for col in range(8):
            if row <= 4 and all(board[row + i][col] == player for i in range(4)):
                return True
            if col <= 4 and all(board[row][col + i] == player for i in range(4)):
                return True
            if row <= 4 and col <= 4 and all(board[row + i][col + i] == player for i in range(4)):
                return True
            if row >= 3 and col <= 4 and all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def reset_game():
    game_state['board'] = [[' ' for _ in range(8)] for _ in range(8)]
    game_state['current_player'] = 1
    game_state['winner'] = None

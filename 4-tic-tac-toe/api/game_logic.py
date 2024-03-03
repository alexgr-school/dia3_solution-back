import random

game_state = {
    'game_mode': 'pvp', # Modes: pvp (player vs player), pve (player vs environment/IA)
    'board': [[' ' for _ in range(8)] for _ in range(8)],
    'current_player': 1,  # 1 starts
    'winner': None,
}

def set_game_mode(mode):
    if mode in ['pvp', 'pve']:
        game_state['game_mode'] = mode
        reset_game()  # Réinitialiser le jeu lors du changement de mode
    else:
        raise ValueError("Invalid game mode. Choose 'pvp' or 'pve'.")

def check_win(board, player):
    # Vérification horizontale, verticale et diagonale
    for row in range(8):
        for col in range(8):
            if row <= 4 and all(board[row + i][col] == player for i in range(4)):
                return [(row + i, col) for i in range(4)]
            if col <= 4 and all(board[row][col + i] == player for i in range(4)):
                return [(row, col + i) for i in range(4)]
            if row <= 4 and col <= 4 and all(board[row + i][col + i] == player for i in range(4)):
                return [(row + i, col + i) for i in range(4)]
            if row >= 3 and col <= 4 and all(board[row - i][col + i] == player for i in range(4)):
                return [(row - i, col + i) for i in range(4)]
    return None


def reset_game():
    game_state['board'] = [[' ' for _ in range(8)] for _ in range(8)]
    game_state['current_player'] = 1
    game_state['winner'] = None

def ai_move():
    # Trouve toutes les positions vides
    available_moves = [(row, col) for row in range(8) for col in range(8) if game_state['board'][row][col] == ' ']
    
    # Si aucune position n'est disponible, retourne None (ce qui indiquerait un plateau plein et donc un match nul)
    if not available_moves:
        return None, None
    
    # Choisis une position aléatoirement parmi les positions disponibles
    row, col = random.choice(available_moves)
    
    # Applique le mouvement de l'IA sur le plateau
    game_state['board'][row][col] = 2  # On suppose ici que 2 représente l'IA
    
    # Retourne les coordonnées du mouvement pour que l'API puisse informer le client
    return row, col

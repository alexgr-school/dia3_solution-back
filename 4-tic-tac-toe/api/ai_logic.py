def evaluate_board(grid, player):
    """
    Évalue l'état du plateau pour le joueur spécifié.
    """
    opponent = 1 if player == 2 else 2
    score = 0

    # Fonction pour évaluer chaque ligne, colonne, et diagonales
    def evaluate_line(line):
        nonlocal score
        if line.count(player) == 4:
            score += 100
        elif line.count(player) == 3 and line.count(' ') == 1:
            score += 10
        if line.count(opponent) == 3 and line.count(' ') == 1:
            score -= 50

    # Parcourir le plateau pour évaluer chaque ligne/colonne/diagonale possible
    for row in range(8):
        for col in range(8):
            if col <= 4:  # Horizontal
                evaluate_line([grid[row][c] for c in range(col, col + 4)])
            if row <= 4:  # Vertical
                evaluate_line([grid[r][col] for r in range(row, row + 4)])
            if row <= 4 and col <= 4:  # Diagonale \
                evaluate_line([grid[row+i][col+i] for i in range(4)])
            if row <= 4 and col >= 3:  # Diagonale /
                evaluate_line([grid[row+i][col-i] for i in range(4)])

    return score

def minimax(grid, depth, alpha, beta, is_maximizing, player):
    opponent = 1 if player == 2 else 2
    if depth == 0 or check_win(grid, player) or check_win(grid, opponent):
        return evaluate_board(grid, player), None, None

    if is_maximizing:
        max_eval = float('-inf')
        best_move = (None, None)  # Initialisé à None pour les deux
        for row, col in available_moves(grid):
            grid[row][col] = player
            eval, _, _ = minimax(grid, depth-1, alpha, beta, False, player)
            grid[row][col] = ' '  # Annuler le coup
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)  # Mise à jour du meilleur coup
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move[0], best_move[1]
    else:
        min_eval = float('inf')
        best_move = (None, None)  # Initialisé à None pour les deux
        for row, col in available_moves(grid):
            grid[row][col] = opponent
            eval, _, _ = minimax(grid, depth-1, alpha, beta, True, player)
            grid[row][col] = ' '  # Annuler le coup
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)  # Mise à jour du meilleur coup
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move[0], best_move[1]


def available_moves(grid):
    """
    Retourne une liste de tous les mouvements possibles.
    """
    return [(row, col) for row in range(8) for col in range(8) if grid[row][col] == ' ']

def check_win(grid, player):
    """
    Vérifie si le joueur spécifié a gagné.
    """
    for row in range(8):
        for col in range(8):
            if grid[row][col] == player:
                # Vérifications horizontales
                if col <= 4:
                    if all(grid[row][col+i] == player for i in range(4)):
                        return True
                # Vérifications verticales
                if row <= 4:
                    if all(grid[row+i][col] == player for i in range(4)):
                        return True
                # Vérifications diagonales (haut gauche à bas droite)
                if row <= 4 and col <= 4:
                    if all(grid[row+i][col+i] == player for i in range(4)):
                        return True
                # Vérifications diagonales (bas gauche à haut droite)
                if row >= 3 and col <= 4:
                    if all(grid[row-i][col+i] == player for i in range(4)):
                        return True
    return False

def get_optimal_move(grid, player):
    """
    Trouve le meilleur mouvement pour l'IA.
    """
    score, row, col = minimax(grid, 4, float('-inf'), float('inf'), True, player)
    return row, col  # Retourner directement les coordonnées

if __name__  == "__main__":
    grid = [[' ' for _ in range(8)] for _ in range(8)]
    grid[0][0] = 1
    # Exemple d'exécution de minimax
    score, row, col = minimax(grid, 4, float('-inf'), float('inf'), True, 2)
    print(f"minimax returned: score={score}, row={row}, col={col}")

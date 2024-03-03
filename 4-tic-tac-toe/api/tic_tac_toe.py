from ai_logic import get_optimal_move

class TicTacToe:
    def __init__(self):
        # Initialiser les paramètres du jeu
        self.game_mode = 'pvp' # Modes : pvp (joueur contre joueur), pve (joueur contre environnement/IA)
        self.grid = [[' ' for _ in range(8)] for _ in range(8)]
        self.current_player = 1  # Le joueur 1 commence
        self.winner = None
        self.size = 8

    def set_game_mode(self, mode):
        # Définir le mode de jeu et réinitialiser le jeu
        if mode in ['pvp', 'pve']:
            self.game_mode = mode
            self.reset_game()
        else:
            raise ValueError("Invalid game mode. Choose 'pvp' or 'pve'.")
        
    def reset_game(self):
        # Réinitialiser le jeu à son état initial
        self.grid = [[' ' for _ in range(8)] for _ in range(8)]
        self.current_player = 1
        self.winner = None

    def check_win(self, player):
        """
        Vérifier les conditions de victoire (horizontales, verticales et diagonales) pour aligner 4 cases.
        """
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == player:
                    # Vérifications horizontales
                    if col <= 4:
                        if all(self.grid[row][col+i] == player for i in range(4)):
                            return True
                    # Vérifications verticales
                    if row <= 4:
                        if all(self.grid[row+i][col] == player for i in range(4)):
                            return True
                    # Vérifications diagonales (haut gauche à bas droite)
                    if row <= 4 and col <= 4:
                        if all(self.grid[row+i][col+i] == player for i in range(4)):
                            return True
                    # Vérifications diagonales (bas gauche à haut droite)
                    if row >= 3 and col <= 4:
                        if all(self.grid[row-i][col+i] == player for i in range(4)):
                            return True
        return False

    def get_winning_cells(self, player):
        """
        Retourne un booléen indiquant si le joueur a gagné et les positions des cases gagnantes.
        """
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == player:
                    # Vérifications horizontales
                    if col <= 4:
                        if all(self.grid[row][col+i] == player for i in range(4)):
                            return [(row, col+i) for i in range(4)]
                    # Vérifications verticales
                    if row <= 4:
                        if all(self.grid[row+i][col] == player for i in range(4)):
                            return [(row+i, col) for i in range(4)]
                    # Vérifications diagonales (haut gauche à bas droite)
                    if row <= 4 and col <= 4:
                        if all(self.grid[row+i][col+i] == player for i in range(4)):
                            return [(row+i, col+i) for i in range(4)]
                    # Vérifications diagonales (bas gauche à haut droite)
                    if row >= 3 and col <= 4:
                        if all(self.grid[row-i][col+i] == player for i in range(4)):
                            return [(row-i, col+i) for i in range(4)]
        return []
        
    def get_valid_moves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == ' ':
                    if any(self.grid[r][c] != ' ' for r, c in self.get_neighbors(row, col)):
                        moves.append((row, col))
        return moves

    def get_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            if 0 <= row + dr < self.size and 0 <= col + dc < self.size:
                yield row + dr, col + dc

    def move(self, row, col, player):
        # Valider le mouvement et mettre à jour l'état du jeu
        if self.winner is not None:
            raise ValueError("Game has ended.")
        
        if player not in [1, 2]:
            raise ValueError("Invalid player.")
        if self.current_player != player:
            raise ValueError("Not your turn.")
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError("Move out of bounds.")
        if self.grid[row][col] != ' ':
            raise ValueError("Cell is already taken.")
        
        # Exécuter le mouvement
        self.grid[row][col] = player
        if self.check_win(player):
            self.winner = player
            return "Player {player} has won!", self.grid, self.current_player, self.winner, self.get_winning_cells(player)
        
        # Vérifier le match nul
        if all(all(cell != ' ' for cell in row) for row in self.grid):
            self.winner = 0
            return "Draw", self.grid, self.current_player, self.winner, []
        
        # Gérer le mouvement de l'IA en mode PvE
        if self.game_mode == 'pve' and player == 1:
            return self.ai_move()
        
        # Changer de joueur
        if self.game_mode == 'pvp':
            self.current_player = 2 if player == 1 else 1
            return "Move successful.", self.grid, self.current_player, self.winner, []
    
    def ai_move(self):
        # Déterminer et exécuter le meilleur mouvement pour l'IA
        if self.game_mode == 'pve':
            self.current_player = 2
            tmp_grid = [row[:] for row in self.grid]

            row, col = get_optimal_move(tmp_grid, self.current_player)

            if row is not None and col is not None:
                self.grid[row][col] = self.current_player
                
                # Vérifie si l'IA a gagné avec ce mouvement
                if self.check_win(self.current_player):
                    self.winner = self.current_player
                    return f"AI has won!", self.grid, self.current_player, self.winner, self.get_winning_cells(self.current_player)
                
                # Vérifie si le plateau est complet après le mouvement de l'IA
                if all(all(cell != ' ' for cell in row) for row in self.grid):
                    self.winner = 0
                    return "Draw", self.grid, self.current_player, self.winner, []
                
                self.current_player = 1
                return "AI moved.", self.grid, self.current_player, self.winner, [{'row': row, 'col': col}]
            else:
                self.current_player = 1
                return "No valid moves for AI.", self.grid, self.current_player, self.winner, []
        else:
            raise ValueError("AI move called in PvP mode.")

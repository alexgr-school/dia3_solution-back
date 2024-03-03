from flask import jsonify, request
from game_logic import game_state, check_win, reset_game, ai_move, set_game_mode

def register_routes(app):
    @app.route('/set_mode', methods=['POST'])
    def set_mode():
        data = request.json
        mode = data.get('mode')
        
        try:
            set_game_mode(mode)
            return jsonify({'message': f'Game mode set to {mode}', 'game_mode': mode})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/move', methods=['POST'])
    def move():
        if game_state['winner'] is not None:
            return jsonify({'error': 'Game has ended.'}), 400

        data = request.json
        row, col, player = data.get('row'), data.get('col'), data.get('player')
        
        # S'assure que le joueur est valide et qu'il est son tour de jouer
        if player not in [1, 2]:
            return jsonify({'error': 'Invalid player.'}), 400
        if game_state['current_player'] != player:
            return jsonify({'error': 'Not your turn.'}), 400
        if not (0 <= row < 8 and 0 <= col < 8):
            return jsonify({'error': 'Move out of bounds.'}), 400
        if game_state['board'][row][col] != ' ':
            return jsonify({'error': 'Cell is already taken.'}), 400
        
        # Applique le mouvement du joueur
        game_state['board'][row][col] = player
        winning_positions = check_win(game_state['board'], player)
        if winning_positions:
            game_state['winner'] = player
            return jsonify({'message': f'Player {player} has won!', 'winner': player, 'winning_positions': winning_positions, 'board': game_state['board']})
        elif all(all(cell != ' ' for cell in row) for row in game_state['board']):
            game_state['winner'] = 0
            return jsonify({'message': 'Draw', 'winner': 0, 'board': game_state['board']})
            
        # Change le joueur si en mode PvP
        if game_state['game_mode'] == 'pvp':
            game_state['current_player'] = 2 if player == 1 else 1
            return jsonify({'message': 'Move successful', 'game_mode': game_state['game_mode'], 'board': game_state['board'], 'current_player': game_state['current_player'], 'winner': game_state['winner']})
        
        # Si en mode PvE et que c'est au tour de l'IA
        if game_state['game_mode'] == 'pve' and player == 1:
            ai_row, ai_col = ai_move()
            ai_winning_positions = check_win(game_state['board'], 2)
            if ai_winning_positions:
                game_state['winner'] = 2
                return jsonify({'message': 'AI has won!', 'game_mode': game_state['game_mode'], 'winner': 2, 'board': game_state['board'], 'winning_positions': ai_winning_positions, 'ai_move': {'row': ai_row, 'col': ai_col}})
            elif all(all(cell != ' ' for cell in row) for row in game_state['board']):
                game_state['winner'] = 0
                return jsonify({'message': 'Draw', 'winner': 0, 'board': game_state['board']})
            else:
                # C'est toujours au tour du joueur 1 après le mouvement de l'IA
                game_state['current_player'] = 1
                return jsonify({'message': 'Move successful', 'game_mode': game_state['game_mode'], 'board': game_state['board'], 'current_player': game_state['current_player'], 'winner': game_state['winner'], 'ai_move': {'row': ai_row, 'col': ai_col}})
        
        return jsonify({'error': 'Unexpected state.'}), 500

    @app.route('/board', methods=['GET'])
    def get_board():
        return jsonify({'board': game_state['board'], 'game_mode': game_state['game_mode'], 'current_player': game_state['current_player'], 'winner': game_state['winner']})

    @app.route('/reset', methods=['POST'])
    def reset():
        reset_game()
        return jsonify({'message': 'Game reset'})

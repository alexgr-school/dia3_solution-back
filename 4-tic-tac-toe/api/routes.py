from flask import jsonify, request
from game_logic import game_state, check_win, reset_game

def register_routes(app):
    @app.route('/move', methods=['POST'])
    def move():
        if game_state['winner'] is not None:
            return jsonify({'error': 'Game has ended.'}), 400
        
        data = request.json
        row, col, player = data.get('row'), data.get('col'), data.get('player')
        
        if player not in [1, 2]:
            return jsonify({'error': 'Invalid player.'}), 400
        if game_state['current_player'] != player:
            return jsonify({'error': 'Not your turn.'}), 400
        if not (0 <= row < 8 and 0 <= col < 8):
            return jsonify({'error': 'Move out of bounds.'}), 400
        if game_state['board'][row][col] != ' ':
            return jsonify({'error': 'Cell is already taken.'}), 400
        
        game_state['board'][row][col] = player
        if check_win(game_state['board'], player):
            game_state['winner'] = player
            return jsonify({'message': f'Player {player} has won!', 'winner': player, 'board': game_state['board']})
        
        if all(all(cell != ' ' for cell in row) for row in game_state['board']):
            game_state['winner'] = 0
            return jsonify({'message': 'Draw', 'winner': 0, 'board': game_state['board']})
        
        game_state['current_player'] = 2 if player == 1 else 1
        return jsonify({'message': 'Move successful', 'board': game_state['board'], 'current_player': game_state['current_player'], 'winner': game_state['winner']})

    @app.route('/board', methods=['GET'])
    def get_board():
        return jsonify({'board': game_state['board'], 'current_player': game_state['current_player'], 'winner': game_state['winner']})

    @app.route('/reset', methods=['POST'])
    def reset():
        reset_game()
        return jsonify({'message': 'Game reset'})

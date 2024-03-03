from flask import jsonify, request

def register_routes(app, game):
    @app.route('/set_mode', methods=['POST'])
    def set_mode():
        data = request.json
        mode = data.get('mode')
        
        try:
            game.set_game_mode(mode)
            return jsonify({'message': f'Game mode set to {mode}', 'game_mode': mode})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/move', methods=['POST'])
    def move():
        if game.winner is not None:
            return jsonify({'error': 'Game has ended.'}), 400

        data = request.json
        row, col, player = data.get('row'), data.get('col'), data.get('player')

        try:
            message, grid, current_player, winner, winning_cells = game.move(row, col, player)
            response = {
                'message': message,
                'grid': grid,
                'current_player': current_player,
                'winner': winner,
                'winning_cells': winning_cells
            }
            if 'ai_move' in message:
                response['ai_move'] = {'row': row, 'col': col}
            return jsonify(response)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/grid', methods=['GET'])
    def get_grid():
        return jsonify({
            'grid': game.grid,
            'game_mode': game.game_mode,
            'current_player': game.current_player,
            'winner': game.winner
        })

    @app.route('/reset', methods=['POST'])
    def reset():
        game.reset_game()
        return jsonify({'message': 'Game reset'})

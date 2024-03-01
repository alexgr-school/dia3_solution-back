import numpy

class TictactoeGrid:
	def __init__(self):
		self.grid = numpy.zeros((3, 3))
		self.game_in_progress = True
		self.winner = 0


	def winning_check(self):
		# DRY : don't repeat yourself
		there_is_winner = (numpy.all(self.grid[0,:] == self.grid[0, 0]) and self.grid[0, 0] != 0 ) or\
						  		(numpy.all(self.grid[1,:] == self.grid[1, 0]) and self.grid[1, 0] != 0 ) or\
						  		(numpy.all(self.grid[2,:] == self.grid[2, 0]) and self.grid[2, 0] != 0 ) or\
						 		(numpy.all(self.grid[:, 0] == self.grid[0,0]) and self.grid[0, 0] != 0 ) or\
						  		(numpy.all(self.grid[:, 1] == self.grid[0,1]) and self.grid[0, 1] != 0 ) or\
						  		(numpy.all(self.grid[:, 2] == self.grid[0,2]) and self.grid[0, 2] != 0 ) or\
						  		(numpy.all(self.grid.diagonal() == self.grid[0,0]) and self.grid[0, 0] != 0)or\
						  		(numpy.all(numpy.fliplr(self.grid).diagonal() == self.grid[0,2]) and self.grid[0, 2] != 0)

		return there_is_winner


	def get_game_state(self):
		return numpy.any(self.grid == 0)



	def human_move(self, index_line, index_column):
		self.grid[index_line, index_column] = 1
		
		self.game_in_progress = self.get_game_state()
		self.there_is_winner = self.winning_check()

		if self.there_is_winner:
			self.game_in_progress = False
			self.winner = 1
		

	def robot_move(self):
		index_line, index_column = self.get_optimal_cell()
		self.grid[index_line, index_column] = 2
		
		self.game_in_progress = self.get_game_state()
		self.there_is_winner = self.winning_check()

		if self.there_is_winner:
			self.game_in_progress = False
			self.winner = 2
			
		return index_line, index_column


	def get_optimal_cell(self):

		best_score = -float('inf')
		best_index_line, best_index_column = None, None

		for index_line in range(0, 3):
			for index_column in range(0, 3):
				if self.grid[index_line, index_column] == 0:
					self.grid[index_line, index_column] = 2
					score = self.minmax(robot_turn=False)
					if score > best_score:
						best_score = score
						best_index_line = index_line
						best_index_column = index_column
					self.grid[index_line, index_column] = 0	

		return best_index_line, best_index_column


	def minmax(self, robot_turn):
		
		if self.winning_check():
			return -1 if robot_turn else 1 
		elif not self.get_game_state():
			return 0
		

		best_score = -float('inf') if robot_turn else float('inf')

		for index_line in range(0, 3):
			for index_column in range(0, 3):
				if self.grid[index_line, index_column] == 0:
					self.grid[index_line, index_column] = 2 if robot_turn else 1
					score = self.minmax(not robot_turn)
					self.grid[index_line, index_column] = 0
					best_score = max(score, best_score) if robot_turn else min(score, best_score)
					
		return best_score
import pickle

class Handler:
	def __init__(self):
		self.players=[]

	def add_player(self,player):
		while player.get_info('ID') in self.players:
			player.new_ID()

		self.players.append(player)

	def get_players(self):
		return self.players

	def delete_player(self,index):
		self.players.pop(index)

	def results(self,player_1,player_2,winner):
		p1_games=player_1.get_game_numbers() 
		p2_games=player_2.get_game_numbers() 

		if p1_games < 10 :
			









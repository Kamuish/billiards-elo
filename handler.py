import pickle

#Elo system that stores all players in a list.
class Handler:
	def __init__(self):
		self.players=[]
		self.removed_players=[]

	def add_player(self,player):
		while player.get_info('ID') in self.players:
			player.new_ID()

		self.players.append(player)

	def get_player(self,index):
		return self.players[index]

	def get_players(self):
		return self.players

	def delete_player(self,index):
		self.removed_players.append(self.players.pop(index))
		

	def __str__(self):
		string=''

		for j in self.players:
			string+='- name:'+str(j.get_info('name'))+' -elo:'+str(j.get_info('elo'))
		return string
	def sort(self):
		try:
			update_list=[self.players[0]]

			for j in self.players[1:]:
				index=0

				for k in update_list:
					if j.get_info('elo')<= k.get_info('elo'):
						index+=1
				update_list.insert(index,j)
			self.players=update_list
			del update_list
		except:
			pass



	def results(self,player_1,player_2,winner,k_factor=20):


		p1_elo=player_1.get_info('elo')
		p2_elo=player_2.get_info('elo')

		esp_score_p1=1/(1+10**((p2_elo-p1_elo)/400))
		esp_score_p2=1/(1+10**((p1_elo-p2_elo)/400))

		if winner==None:
			score_p1=score_p2=0.5
			

		elif winner.get_info('ID')==player_1.get_info('ID'):
			score_p1=1
			score_p2=0

			
		elif winner.get_info('ID')==player_2.get_info('ID'):
			score_p1=0
			score_p2=1

		player_1.record_game(player_2,score_p1)
		player_2.record_game(player_1,score_p2)


		new_elo_p1=p1_elo+k_factor*(score_p1-esp_score_p1)
		new_elo_p2=p2_elo+k_factor*(score_p2-esp_score_p2)

		player_1.update_elo(new_elo_p1)
		player_2.update_elo(new_elo_p2)


		print(new_elo_p1,new_elo_p2)

					
if __name__=='__main__':
	from player import player

	a=player('a')
	b=player('b')

	handler=Handler()
	handler.add_player(a)
	handler.add_player(b)

	b.update_elo(1000)

	handler.results(a,b,b)









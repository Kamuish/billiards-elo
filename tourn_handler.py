from player import player
from random import shuffle
class Stage():
	def __init__(self,players,handler):
		self.players=players



		self.passing=['TBD' for j in range(int(len(players)/2))]


		count=0
		for j in range(0,len(players)-1,2):
			if players[j] =='Open':
				self.passing[count]=players[j+1]

			elif players[j+1]=='Open':
				self.passing[count]=players[j]
			count+=1
			
		self.handler=handler


	def __str__(self):
		return ''.join(self.players)

	def __len__(self):
		return len(self.players)

	def get_players(self):
		return self.players

	def add_player(self,player,position):

		self.players.insert(position,add_player)


	def game_result(self,player1,player2,winner):
		self.handler.results(player1,player2,winner)

		if winner.get_info('ID')==player1.get_info('ID'):
			score_p1=1
			score_p2=0

			self.passing.append(player1)

			
		elif winner.get_info('ID')==player2.get_info('ID'):
			score_p1=0
			score_p2=1
			self.passing.append(player2)




class Brackets():
	"""docstring for Bracket"""
	def __init__(self,handler,players):
		self.handler=handler

		#Checks if the number of players is a multiple of 2
		if not (len(players) != 0 and ((len(players) & (len(players) - 1)) == 0)):
			while  not(len(players) != 0 and ((len(players) & (len(players) - 1)) == 0)):
				players.append('Open')
			shuffle(players)

		self.stages=[Stage(players,handler)]

		val=len(players)
		while val>=2:
			self.stages.append(Stage(self.stages[-1].passing,handler))
			val=val//2
	

	def print_stages(self):
		for j in range(len(self.stages)):
			
			players=self.stages[j].get_players()

			if players[0]=='Open' or players[0]=='TBD':
				string=players[0]
			else:
				string = players[0].get_info('name')

			for elem in players[1:]:
				if elem=='Open' or elem=='TBD':
					string+='\t'+elem
				else:
					string+='\t'+elem.get_info('name')
			print(string)

	def stages_numb(self):
		return len(self.stages)



class tournament(Brackets):
	def __init__(self,name,handler,players):
		super().__init__(handler,players)

		self.name=name
		self.all_players=players
		self.handler=handler
		self.name

		self.print_stages()
		
		

	

if __name__=='__main__':
	b=tournament(None,['a' for i in range(10)])
	b.print_stages()
	
from random import randint
import pickle


class player:
	def __init__(self,name):
		self.elo=1200

		self.ID=randint(0,10000)
		self.games=[]
		self.oponnent_elo=[]
		self.results=[]
		self.name=name

		self.tournament_result={}

	def __str__(self):
		
		return 'ID:'+str(self.ID)+'-name:'+self.name+'-elo:'+str(self.elo)


	def new_ID(self):
		self.ID=randint(0,10000)


	def record_game(self,player_2,result):
		
		self.games.append(player_2)
		self.oponnent_elo.append(player_2.get_info('elo'))
		self.results.append(result)

	def tourn_result(self,tourn,result,brackets):
		if tourn in self.tournament_result:

			self.tournament_result[tourn].append([str(result)+'/'+str(brackets)])
		else:

			self.tournament_result[tourn]=[str(result)+'/'+str(brackets)]


	def get_game_numbers(self):
		return len(self.games)

	def get_info(self,param):
		return getattr(self,param)

	def update_elo(self,value):
		self.elo=value

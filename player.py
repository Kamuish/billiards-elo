from random import randint
import pickle
x='qaa'
print(x)
x=x[:-1]+']'
print(x)


class player:
	def __init__(self,name):
		self.elo=1200

		self.ID=randint(0,10000)
		self.games=[]
		self.oponnent_elo=[]
		self.results=[]
		self.name=name

	def __str__(self):
		games_str='['
		for j in self.games:
			games_str+= j + ','

		if len(self.games)!=0:
			games_str=games_str[:-1]+']'
		else:
			games_str+=']'
		return 'ID:'+str(self.ID)+'-name:'+self.name+'-games:'+games_str+'-elo:'+str(self.elo)

	def new_ID(self):
		self.ID=randint(0,10000)


	def record_game(self,player_2,result):
		self.games.append(player_2)
		self.oponnent_elo.append(player_2.get_info('elo'))
		self.results.append(result)

		
	def get_game_numbers(self):
		return len(self.games)

	def get_info(self,param):
		return getattr(self,param)

	def update_elo(self,value):
		self.elo=value

x=player('aa')

if 0:
	pickle_out=open("test.pickle",'wb')
	pickle.dump(x,pickle_out)
	pickle_out.close
if 0:
	pickle_in=open("test.pickle",'rb')
	x=pickle.load(pickle_in)
	print(x)
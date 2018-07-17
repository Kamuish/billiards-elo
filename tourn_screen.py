import tkinter as tk
import pickle
from tkinter import ttk

from handler import Handler
from player import player

import jsonpickle
from tourn_handler import tournament

from functools import partial

Large_Font=('Verdana',15)
Normal_Font=('Verdana',11)
Small_Font=('Verdana',10)

winners={}
listas=[]
all_winners={}

def tour_graph(controller,handler,tour):
	root=tk.Toplevel()

	global windows
	windows=[]
	winners=[]
	all_winners={}
	listas=[]

	

	tour.print_stages()


	def hit_button(brack,p1,p2,val):
		global winners
		global listas
		if val=='one':
			other_p=p2
			p_ind=p1
		else:
			other_p=p1
			p_ind=p2
			
		if brack in winners:
			if p_ind in winners[brack]:
				button1=listas[brack][p1]
				button2=listas[brack][p2]

				tmp=tk.Button(root)
				color=tmp['bg']
				winners[brack].remove(p_ind)
				button1['bg']=color
				button2['bg']=color

				del tmp
				return


			if other_p in winners[brack]:
				winners[brack][winners[brack].index(other_p)]=p_ind
			else:
				winners[brack].append(p_ind)
			# O resto da divisao inteira por 2 da a posicao dos butoes na lista

		else:
			winners[brack]=[p_ind]
		
		button1=listas[brack][p1]
		button2=listas[brack][p2]

		if val=='one':
			button1['bg']='cyan'
			button2['bg']='brown2'

		if val=='two':
			button1['bg']='brown2'
			button2['bg']='cyan'

	def on_ex():
		global listas
		global windows
		global all_winners
		global winners
		for k in listas:
			for j in k:
				j.destroy()
		for w in windows:
			w.destroy()
		all_winners={}
		winners={}
		listas=[]
		windows=[]
		print('on ex')
		print(handler)
		root.destroy()
	root.protocol("WM_DELETE_WINDOW", on_ex	)


		

	def draw_stages():
		span=1


		for j in range(len(tour.stages)):
			win=tk.Frame(root)
			win.grid(row=0,column=j,rowspan=len(tour.stages[0].get_players()))
			windows.append(win)
			global listas
			listas.append([])
			players=tour.stages[j].get_players()

			count=0
			
			for k in range(0,len(players)-1,2):
				var1=tk.StringVar()
				var2=tk.StringVar()
				try:	
					but1=tk.Button(win,text=players[k].get_info('name'),command=partial( hit_button, j,k,k+1,'one'))
				except:
					but1=tk.Button(win,text=players[k])
					if players[k]=='Open':
						but1['state']=tk.DISABLED
				try:	
					but2=tk.Button(win,text=players[k+1].get_info('name'),command=partial(hit_button,j,k,k+1,'two'))	
					
				except:
					but2=tk.Button(win,text=players[k+1])

					if players[k+1]=='Open':
						but2['state']=tk.DISABLED
				
				
				but1.grid(row=count ,column=0,rowspan=span,sticky='NSEW',padx=[0,10],pady=[3*span,3*span])
			
				but2.grid(row=count+span,column=0,rowspan=span,sticky='NSEW',padx=[0,10],pady=[3*span,3*span])
				

				listas[-1].append(but1)
				listas[-1].append(but2)
				del but1,but2
				count+=span*2
			if len(players)==1:
				try:
					but1=tk.Button(win,text=players[0].get_info('name'))
				except:
					but1=tk.Button(win,text=players[0])
				but1.grid(row=0,column=0,rowspan=span,sticky='NSEW')
				listas[-1].append(but1)
				del but1

			span*=2


	def update_handler(handler):
		tour.update()

		global winners
		for key in winners:
			for j in winners[key]:
				if j%2==0:
					tour.stages[key].game_result(handler,tour.stages[key].get_player(j),tour.stages[key].get_player(j+1),tour.stages[key].get_player(j),int(j/2))
				else:
					tour.stages[key].game_result(handler,tour.stages[key].get_player(j),tour.stages[key].get_player(j-1),tour.stages[key].get_player(j),int((j-1)/2))
		

		
		global windows
		global listas
		for win in windows:
			win.destroy()

		windows=[]
		listas=[]
		draw_stages()

		
		all_winners.update(winners)
		for key in range(len(listas)):	
			for j in range(len(listas[key])):
				try:
					if j in all_winners[key]:
						listas[key][j]['bg']='cyan'
					elif tour.has_lost(tour.stages[key].get_player(j)):
						listas[key][j]['bg']='brown2'
				except:
					pass
		winners={}
		controller.event_generate("<<new_player>>")
	draw_stages()

	button=tk.Button(root,text='Update',command=lambda: update_handler(handler))
	button.grid(row=len(tour.stages[0].get_players())+1,column=0,pady=[10,0])


def tourn_page(controller,handler):

	global tour_holder
	global active_tour
	root=tk.Toplevel()

	jsonpickle.set_encoder_options('json',indent=4)

	jsonpickle.set_decoder_options('json')
	#Tour_holder is a list with the names of all the tournaments

	try:
		file_2=open('tour_holder.json','r')
		val=file_2.read()
		file_2.close()

		tour_holder = jsonpickle.decode(val)  
	except Exception as e:
		print(e)
		tour_holder=[]


	
	active_tour=None


	label=tk.Label(root,text='tournaments',font=Normal_Font)
	label.grid(row=0,column=0,rowspan=1,columnspan=2)

	
	list_tour=tk.Listbox(root)
	list_tour.grid(row=1,column=0,columnspan=2,rowspan=2,padx=[0,10],sticky='NSEW')

	def draw_list():
		list_tour.delete(0,tk.END)
		for j in tour_holder:
			list_tour.insert(tk.END,j.name)

	draw_list()
	root.bind("<<new_tour>>",lambda y: draw_list())

	def create_tour():
		window=tk.Toplevel()
		list_p=tk.Listbox(window,selectmode=tk.MULTIPLE)
		list_p.grid(row=0,column=0,columnspan=1,rowspan=3,padx=[0,10],sticky='NSEW')

		list_p.delete(0,tk.END)
		handler.sort()
		for j in handler.get_players():
			list_p.insert(tk.END,j.get_info('name')+'  - MMR: %s'%round(j.get_info('elo')))


		label=tk.Label(window,text='Tour name',font=Normal_Font)
		label.grid(row=0,column=1)
		entry=tk.Entry(window,font=Normal_Font)
		entry.grid(row=1,column=1)


		def active():
			
			global tour_holder
			index=list_p.curselection()
			players=[]
			if len(index)!=0:
				for j in index:
					players.append(handler.get_player(j))

				active_tour=tournament(entry.get(),handler,players)
				tour_holder.append(active_tour)
			root.event_generate("<<new_tour>>")

			
			js = jsonpickle.encode(tour_holder)
			file=open('tour_holder.json','w')
			file.write(js)
			file.close()


			window.destroy()



		add_game=tk.Button(window,text='Create',command= lambda :active())
		add_game.grid(row=3,column=0,sticky='NSEW')



	def load_tour():
		global active_tour
		try:
			active_tour=tour_holder[list_tour.curselection()[0]]
		except:
			pass

		
	add_game=tk.Button(root,text='Create Tour',command= lambda :create_tour())
	add_game.grid(row=3,column=0,sticky='NSEW')

	load_game=tk.Button(root,text='Load Tour',command= lambda :load_tour())
	load_game.grid(row=3,column=1,sticky='NSEW')


	add_game=tk.Button(root,text='Start Tour',command= lambda :tour_graph(controller,handler,active_tour))
	add_game.grid(row=3,column=2,sticky='NSEW')




	def on_ex():
		print('here')
		js = jsonpickle.encode(tour_holder)
		file=open('tour_holder.json','w')
		file.write(js)
		file.close()
		root.destroy()

	root.protocol("WM_DELETE_WINDOW", on_ex	)

if __name__=='__main__':
	app=tourn_page(None)


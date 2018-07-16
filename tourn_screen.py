import tkinter as tk
import pickle
from tkinter import ttk

from handler import Handler
from player import player

import jsonpickle
from tourn_handler import tournament

Large_Font=('Verdana',15)
Normal_Font=('Verdana',11)
Small_Font=('Verdana',10)


def tour_graph(tour):
	1

def tourn_page(handler):

	
	root=tk.Toplevel()

	jsonpickle.set_encoder_options('json',indent=4)

	jsonpickle.set_decoder_options('json',indent=4)
	#Tour_holder is a list with the names of all the tournaments

	try:
		file_2=open('tour_holder.json','r')
		val=file_2.read()
		file_2.close()

		tour_holder = jsonpickle.decode(val)  
	except:
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
			

			index=list_p.curselection()
			players=[]
			if len(index)!=0:
				for j in index:
					players.append(handler.get_player(j))

				active_tour=tournament(entry.get(),handler,players)
				tour_holder.append(active_tour)
			root.event_generate("<<new_tour>>")
			window.destroy()



		add_game=tk.Button(window,text='Create',command= lambda :active())
		add_game.grid(row=3,column=0,sticky='NSEW')



	add_game=tk.Button(root,text='Create Tour',command= lambda :create_tour())
	add_game.grid(row=3,column=0,sticky='NSEW')

	load_game=tk.Button(root,text='Load Tour',command= lambda :create_game())
	load_game.grid(row=3,column=1,sticky='NSEW')





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


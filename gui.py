import tkinter as tk
import pickle
from tkinter import ttk

from handler import Handler
from player import player
from tourn_screen import tourn_page
import jsonpickle




# https://gist.github.com/i000313/90b1f3c556b1b1ad8278
Large_Font=('Verdana',15)
Normal_Font=('Verdana',11)
Small_Font=('Verdana',10)

def add_player(main_window,handler):

	#TODO: adicionar uma lista pra ver os jogadores e ser possível editar/eliminar jogadores


	window=tk.Toplevel()
	window.title("Add")

	label=tk.Label(window,text='Name',font=Normal_Font)
	label.grid(row=1,column=1,rowspan=1)
	name=ttk.Entry(window)

	name.insert(0, 'Name')
	name.grid(row=1,column=2)


	list_players=tk.Listbox(window)
	list_players.grid(row=0,column=0,rowspan=2)

	for j in handler.get_players():
		list_players.insert(tk.END,j.get_info('name'))


	
	def add_handler():
		name_p=name.get()
		new_player=player(name_p)
		handler.add_player(new_player)
		list_players.insert(tk.END,name_p)
		main_window.event_generate('<<new_player>>')
		

	def del_handler():
		try:
			index=list_players.curselection()[0]
			list_players.delete(index)
			handler.delete_player(index)
			main_window.event_generate('<<new_player>>')
		except Exception as e:
			print(e)
			pass



	add_button=tk.Button(window,text='Add',command= lambda :add_handler())
	add_button.grid(row=0,column=1,sticky='EW')

	add_button=tk.Button(window,text='Del',command= lambda :del_handler())
	add_button.grid(row=0,column=2,sticky='EW')

	window.bind('<Control-w>', lambda y:  window.destroy())

def gui():

	jsonpickle.set_preferred_backend('json')
	root=tk.Tk()
	#root.geometry('520x520')


	try:
		file_2=open('teste.json','r')
		val=file_2.read()
		file_2.close()


		handler = jsonpickle.decode(val)  


	except:
		handler=Handler()

	label=tk.Label(root,text='All players',font=Normal_Font)
	label.grid(row=0,column=0,rowspan=1,columnspan=2)

	label=tk.Label(root,text='Active game',font=Normal_Font)
	label.grid(row=0,column=4,rowspan=1)

	list_players=tk.Listbox(root,selectmode=tk.MULTIPLE)
	list_players.grid(row=1,column=0,columnspan=2,rowspan=2,padx=[0,10],sticky='NSEW')

	

	game_players=tk.Listbox(root,selectmode=tk.SINGLE)
	game_players.grid(row=1,column=4,columnspan=1,rowspan=2)


	def create_game():
		global current_game
		current_game=[]
		try:
			players_index=list_players.curselection()

			player_1=handler.get_player(players_index[0])
			player_2=handler.get_player(players_index[1])

			current_game.append(player_1)
			current_game.append(player_2)

			game_players.delete(0,tk.END)
			game_players.insert(tk.END,player_1.get_info('name')+'  - MMR: %s'% round(player_1.get_info('elo')))
			game_players.insert(tk.END,player_2.get_info('name')+'  - MMR: %s'%round(player_2.get_info('elo')))

			root.event_generate("<<created>>")
		except:
			pass

	def stop_game():

		current_game=[]
		game_players.delete(0,tk.END)
		list_players.selection_clear(0,tk.END)

		root.event_generate("<<created>>")


	add_game=tk.Button(root,text='Create game',command= lambda :create_game())
	add_game.grid(row=3,column=0,sticky='NSEW')

	delete_game=tk.Button(root,text='Stop game',command= lambda :stop_game())
	delete_game.grid(row=3,column=1,sticky='NSEW',padx=[0,10])
	delete_game['state']='disabled'

	def end_game():	

		winner=current_game[game_players.curselection()[0]]

		handler.results(current_game[0],current_game[1],winner)

		stop_game()
		root.event_generate("<<new_player>>")
	record_result=tk.Button(root,text='Record',command= lambda :end_game())


	record_result.grid(row=3,column=4,sticky='NSEW')


	def create_list_all_players():	
		list_players.delete(0,tk.END)
		print('creating list gui')
		handler.sort()
		for j in handler.get_players():
			list_players.insert(tk.END,j.get_info('name')+'  - MMR: %s'%round(j.get_info('elo')))

	def change_bt_state():
		if add_game['state']=='disabled':
			add_game['state']='normal'
			delete_game['state']='disabled'
		else:
			add_game['state']='disabled'
			delete_game['state']='normal'

	create_list_all_players()

	root.bind("<<new_player>>",lambda y: create_list_all_players())
	root.bind("<<created>>",lambda y: change_bt_state())


	def on_ex():

		js = jsonpickle.encode(handler)
		file=open('teste.json','w')
		file.write(js)
		file.close()

		root.quit()

	menubar=tk.Menu(root)
	filemenu=tk.Menu(menubar,tearoff=0)
	filemenu.add_command(label='Add players',command= lambda:add_player(root,handler),font=Normal_Font)

	filemenu.add_separator()
	filemenu.add_command(label='Exit',command=lambda: on_ex(),font=Normal_Font)


	tour=tk.Menu(menubar,tearoff=0)
	tour.add_command(label='Tournament',command=lambda: tourn_page(root,handler),font=Normal_Font)


	menubar.add_cascade(label='Player Handler',menu=filemenu,font=Normal_Font)
	menubar.add_cascade(label='Tournament',menu=tour,font=Normal_Font)

	tk.Tk.config(root,menu=menubar)


	

	root.protocol("WM_DELETE_WINDOW", on_ex	)

	root.bind('<Control-w>', lambda y:  on_ex())
	root.bind('<Control-W>', lambda y:  on_ex())
	root.mainloop()


app=gui()

import tkinter as tk
import pickle
from tkinter import ttk

from handler import Handler
from player import player




# https://gist.github.com/i000313/90b1f3c556b1b1ad8278
Large_Font=('Verdana',15)
Normal_Font=('Verdana',11)
Small_Font=('Verdana',10)

def add_player(main_window,handler):

	#TODO: adicionar uma lista pra ver os jogadores e ser possível editar/eliminar jogadores


	window=tk.Toplevel()
	window.title("Add")

	label=tk.Label(window,text='Name',font=Normal_Font)
	label.grid(row=1,column=1)
	name=ttk.Entry(window)

	name.insert(0, 'Name')
	name.grid(row=1,column=2)


	list_players=tk.Listbox(window)
	list_players.grid(row=0,column=0)

	for j in handler.get_players():
		list_players.insert(tk.END,j.get_info('name'))


	

	def add_handler():
		print('weeee')
		name_p=name.get()
		new_player=player(name_p)
		handler.add_player(new_player)
		list_players.insert(tk.END,name_p)
		main_window.event_generate('<<new_player>>')
		

	def del_handler():
		index=list_players.curselection()[0]
		list_players.delete(index)
		handler.delete_player(index)
		main_window.event_generate('<<new_player>>')



	add_button=tk.Button(window,text='Add',command= lambda :add_handler())
	add_button.grid(row=0,column=1)

	add_button=tk.Button(window,text='Del',command= lambda :del_handler())
	add_button.grid(row=0,column=2)

	window.bind('<Control-w>', lambda y:  window.destroy())

def gui():

	root=tk.Tk()
	root.geometry('920x720')


	try:
		pickle_in = open('players.pickle','rb')
		handler=pickle.load(pickle_in)
	except:
		handler=Handler()

	list_players=tk.Listbox(root)
	list_players.grid(row=0,column=0)

	for j in handler.get_players():
		list_players.insert(tk.END,j.get_info('name'))


	def create_list():	
		list_players.delete(0,tk.END)
		for j in handler.get_players():
			list_players.insert(tk.END,j.get_info('name'))



	root.bind("<<new_player>>",lambda y: create_list())


	def on_ex():
		file= open("players.pickle","wb") 
		pickle.dump(handler,file)
		file.close()
		root.quit()

	menubar=tk.Menu(root)
	filemenu=tk.Menu(menubar,tearoff=0)
	filemenu.add_command(label='Add players',command= lambda:add_player(root,handler),font=Normal_Font)

	filemenu.add_separator()
	filemenu.add_command(label='Exit',command=lambda: on_ex(),font=Normal_Font)


	menubar.add_cascade(label='File',menu=filemenu,font=Normal_Font)

	tk.Tk.config(root,menu=menubar)



	root.protocol("WM_DELETE_WINDOW", on_ex	)

	root.bind('<Control-w>', lambda y:  on_ex())
	root.mainloop()


app=gui()

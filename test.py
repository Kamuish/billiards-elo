class stud(object):
	def __init__(self,name):
		self.name=name
		self.age=10

a=stud('a')


import jsonpickle

js = jsonpickle.encode(stud('a'))

file=open('teste.json','w')
file.write(js)
file.close()

file_2=open('teste.json','r')
val=file_2.read()
file_2.close()


c = jsonpickle.decode(val)  


print(c.name)


x=[1,2,3]
print(x[1:])
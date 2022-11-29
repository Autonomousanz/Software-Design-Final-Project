from tkinter import *
import PIL
from PIL import Image
from abc import ABC,abstractmethod
import copy
import random

# Obstacle abstract factory class

class Obstacles(ABC) :

	"""This is an abstract factory class with ghosts, house, castle , tree acting as product"""

	def __init__(self,x=650,y=670,name = 'NotGhost'):
		
		#directory where images are stored
		self.dir = "downsized_images/"
		# x co-ordinate of obstacle
		self.x = x
		# y co-ordinate of obstacle
		self.y = y
		# name of the obstacle
		self.name = name
	
	@abstractmethod
	def get_obstacle(self):
		pass

#obstacle ghost class
class Ghost(Obstacles):
	""" returns a ghost obstacle """
	def __init__(self,x=650,y=670,name = 'Ghost'):
		super().__init__(x,y,name)
		#image of the obstacle
		img = (Image.open("images/ghost.png"))
		#resize to fit
		resized_image= img.resize((150, 105), Image.Resampling.LANCZOS)
		#save the image in new folder
		self.img = resized_image.save(self.dir + "downsize_ghost.png")
		

	def get_obstacle(self):
		#add the image to tkinter and return it
		self.image = PhotoImage(file=self.dir + "downsize_ghost.png")
		return self.image

class Castle1(Obstacles):
	""" returns a castle1 obstacle """
	def __init__(self,x=650,y=670,name = 'Castle1'):
		super().__init__(x,y,name)
		img = (Image.open("images/castle1.png"))
		resized_image= img.resize((200, 405), Image.Resampling.LANCZOS)
		self.im1 = resized_image.save(self.dir + "downsize_castle1.png")

	def get_obstacle(self):
		self.image = PhotoImage(file=self.dir + "downsize_castle1.png")
		return self.image

class Castle2(Obstacles):
	""" returns a castle2 obstacle """
	def __init__(self,x=650,y=670,name = 'Castle2'):
		super().__init__(x,y,name)
		img = (Image.open("images/castle2.png"))
		resized_image= img.resize((200, 405), Image.Resampling.LANCZOS)
		self.im1 = resized_image.save(self.dir + "downsize_castle2.png")

	def get_obstacle(self):
		self.image = PhotoImage(file= self.dir + "downsize_castle2.png")
		return self.image

class Tree(Obstacles):
	""" returns a tree obstacle """
	def __init__(self,x=650,y=670,name = 'Tree'):
		super().__init__(x,y,name)
		img = (Image.open("images/tree.png"))
		resized_image= img.resize((200, 405), Image.Resampling.LANCZOS)
		self.im1 = resized_image.save(self.dir + "downsize_tree.png")

	def get_obstacle(self):
		self.image = PhotoImage(file = self.dir + "downsize_tree.png")
		return self.image


class House(Obstacles):
	""" returns a tree obstacle """
	def __init__(self,x=650,y=670,name = 'House'):
		super().__init__(x,y,name)
		img = (Image.open("images/house.png"))
		resized_image= img.resize((200, 405), Image.Resampling.LANCZOS)
		self.im1 = resized_image.save(self.dir + "downsize_house.png")

	def get_obstacle(self):
		self.image = PhotoImage(file = self.dir + "downsize_house.png")
		return self.image

class Pumpkin(Obstacles):
	""" returns a tree obstacle """
	def __init__(self,x=650,y=670,name = 'Pumpkin'):
		super().__init__(x,y,name)
		img = (Image.open("images/pumpkin.png"))
		resized_image= img.resize((100, 100), Image.Resampling.LANCZOS)
		self.im1 = resized_image.save(self.dir + "downsize_pumpkin.png")
		

	def get_obstacle(self):
		self.image = PhotoImage(file = self.dir + "downsize_pumpkin.png")
		return self.image



# factory class to return the obstacles and also clone it when needed
class Factory():
	def __init__ (self):
		self.obstacles = {
		"Ghost": Ghost,
       	"Castle1": Castle1,
        "Castle2": Castle2,
       	"Tree": Tree,
		"House" : House,
		"Pumpkin" : Pumpkin
	}
	# get new obstacle
	def create(self,obstacle_name = "Ghost",x=0,y=0):
		return self.obstacles[obstacle_name](x,y)
	
	# Clone design pattern the obstacle with new co-ordinates
	def clone(self,obj):
		"""This is clone design pattern implementation of cloning objects"""

		newObj = copy.deepcopy(obj)
		if newObj.name == 'Ghost':
			newObj.y = random.randint(50, 330)
		return newObj

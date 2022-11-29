from tkinter import *
from PIL import Image
import random
import os
from abc import ABC,abstractmethod
from ObstacleFactory import Factory
import time
import tkinter.font as font

#class for handling collision and motion of obstacles
class ObsDynamics():

    def __init__(self,Gamew):
        #Initialize obstacle factory and create objects of obstacles
        self.facObj = Factory()
        self.ghost = self.facObj.create("Ghost",550,random.randint(100, 300))
        self.castle1 = self.facObj.create("Castle1",550,random.randint(600, 600))
        self.castle2 = self.facObj.create("Castle2",550,random.randint(600, 600))
        self.house = self.facObj.create("House",550,random.randint(600, 600))
        self.tree = self.facObj.create("Tree",550,random.randint(600, 600))
        self.pumpkin = self.facObj.create("Pumpkin",650,670) 

        #array of obstacles we create at the bottom of the screen
        self.obs_pool = [self.castle1, self.castle2, self.tree,self.house,self.pumpkin]
        #instance of GameWindow class passed throught GameWindow constructor
        self.gw = Gamew
        #initial score set to zero
        self.score = 0
        #score on screen
        self.sWin = self.gw.getCanvas().create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)
        #seed for random int to get new object
        random.seed(10)

    #method used for getting the obstacle image and placing it at correct co-ordinates
    def get_rand_obs(self):

        self.obs_obj = self.obs_pool[random.randint(0,3)]
        self.cloned_obj = self.facObj.clone(self.obs_obj)
        self.pump_obj =self.facObj.clone(self.pumpkin)

        self.obsFig = self.gw.getCanvas().create_image(self.cloned_obj.x, self.cloned_obj.y, image=self.cloned_obj.get_obstacle())
        self.pumpFig = self.gw.getCanvas().create_image(self.pump_obj.x, self.pump_obj.y, image=self.pump_obj.get_obstacle())
        self.clonned_ghost = self.facObj.clone(self.ghost)
        self.ghostFig = self.gw.getCanvas().create_image(self.clonned_ghost.x, self.clonned_ghost.y, image=self.clonned_ghost.get_obstacle())

    #method used for motion of the obstacles from left to right
    def ObsMotion(self):
        #Decrement x to make obstacles move
        self.clonned_ghost.x -= 5
        self.pump_obj.x -= 5
        self.gw.getCanvas().coords(self.ghostFig,self.clonned_ghost.x, self.clonned_ghost.y)
        self.gw.getCanvas().coords(self.obsFig,self.clonned_ghost.x, self.cloned_obj.y)
        self.gw.getCanvas().coords(self.pumpFig,self.pump_obj.x,self.pump_obj.y)
        
        # When obstacles go out of frame, bring them back in frame 
        if self.clonned_ghost.x < -100 :
            self.score += 1
            self.gw.getCanvas().itemconfig(self.sWin, text=str(self.score))
            self.get_rand_obs()

        if self.gw.pause == False :
            self.gw.getWindow().after(self.gw.framerate,self.ObsMotion)

    #method used for detecting if witch has collided with any obstacle on the screen
    def DetectCollision(self):

        if (self.clonned_ghost.x < 150 and self.clonned_ghost.x + 100 >= 55) and ((self.gw.posY >= self.clonned_ghost.y - 10 and self.gw.posY < self.clonned_ghost.y + 10)  or (self.gw.posY >= self.cloned_obj.y - 100)):
            
            self.gw.pause = True
            self.ScoreBoard()
            self.EndGameScreen()
        
        if self.gw.pause == False :
            self.gw.getWindow().after(self.gw.framerate,self.DetectCollision)

    #method to show current score and update the high score if needed
    def ScoreBoard(self):
        self.bestScore = 0

        if os.path.isfile("data.dat"):
            scoreFile = open('data.dat')
            self.bestScore = int(scoreFile.read())
            scoreFile.close()
        else:
            scoreFile = open('data.dat', 'w')
            scoreFile.write(str(self.bestScore))
            scoreFile.close()

        if self.score > self.bestScore:
            self.bestScore = self.score 
            scoreFile = open('data.dat', 'w')
            scoreFile.write(str(self.bestScore))
            scoreFile.close()


    def restartBtn(self):          
        self.rbutton = Button(self.gw.getWindow(),text ="Restart Game",pady=30, bg ="red",command=self.RestartGame)
        self.rbutton['font'] = font.Font(size = 30)
        self.restart = self.gw.getCanvas().create_window(250,400,window = self.rbutton)
	
    #method to render end game screen text
    def EndGameScreen(self):

        self.gw.getCanvas().delete(self.ghostFig)
        self.gw.getCanvas().delete(self.obsFig)
        self.gw.getCanvas().delete(self.gw._witch)
        
        self.startgame = False
        self.GameOver = self.gw.getCanvas().create_text(170, 170, text="Game Over", font='Impact 50', fill='#FF0000', anchor=W)
        self.endScore = self.gw.getCanvas().create_text(170, 230, text="Your score: " + str(self.score), font='Impact 40', fill='#FFFF00', anchor=W)
        self.endBest = self.gw.getCanvas().create_text(170, 280, text="Best score: " + str(self.bestScore), font='Impact 40', fill='#FFFF00', anchor=W)
        
        self.restartBtn()
        
    
    #if witch collides and if spacebar is pressed again game restarts
    def RestartGame(self):

        self.gw.getCanvas().delete(self.GameOver)
        self.gw.getCanvas().delete(self.endScore)
        self.gw.getCanvas().delete(self.endBest)
        self.gw.getCanvas().delete(self.ghostFig)
        self.gw.getCanvas().delete(self.obsFig)
        self.gw.getCanvas().delete(self.restart)
    

        self.gw.posY = 200
        self.clonned_ghost.x = 550
        self.score = 0
        self.gw.getCanvas().itemconfig(self.sWin, text=str(self.score))
        self.gw.pause = False
        self.gw._witch = self.gw.getCanvas().create_image(self.gw.posX,self.gw.posY,image=self.gw.witchImg)
        self.gw.run()

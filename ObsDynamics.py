from tkinter import *
from PIL import Image
import random
import os
from abc import ABC,abstractmethod
from ObstacleFactory import Factory



class ObsDynamics():

    def __init__(self,Gamew):

        self.facObj = Factory()
        self.ghost = self.facObj.create("Ghost")
        self.castle1 = self.facObj.create("Castle1")
        self.castle2 = self.facObj.create("Castle2")
        self.house = self.facObj.create("House")
        self.tree = self.facObj.create("Tree") 
        self.pumpkin = self.facObj.create("Pumpkin") 
        self.obs_pool = [self.castle1, self.castle2, self.tree,self.house,self.pumpkin]
        self.gw = Gamew
        self.score = 0
        self.sWin = self.gw.getCanvas().create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)
        random.seed(10)


    def get_rand_obs(self):
        self.obs_x = 550
        
        self.ghost_pos = random.randint(100, 300)
        self.obs_y = random.randint(600, 600)

        self.obs_obj = self.obs_pool[random.randint(0,3)]
        self.cloned_obj = self.facObj.clone(self.obs_obj)
        self.pump_obj =self.facObj.clone(self.pumpkin)
       
        self.obsFig = self.gw.getCanvas().create_image(self.obs_x, self.obs_y, image=self.cloned_obj.get_obstacle())
        self.pumpFig = self.gw.getCanvas().create_image(self.pump_obj.x, self.pump_obj.y, image=self.pump_obj.get_obstacle())
        self.clonned_ghost = self.facObj.clone(self.ghost)
        self.ghostObs = self.gw.getCanvas().create_image(self.obs_x, self.ghost_pos, image=self.clonned_ghost.get_obstacle())

    def ObsMotion(self):

        #Decrement x to make obstacles move
        self.obs_x -= 5
        self.pump_obj.x -= 5
        self.gw.getCanvas().coords(self.ghostObs,self.obs_x, self.ghost_pos)
        self.gw.getCanvas().coords(self.obsFig,self.obs_x, self.obs_y)
        self.gw.getCanvas().coords(self.pumpFig,self.pump_obj.x,self.pump_obj.y)
        
        # When obstacles go out of frame, bring them back in frame
        if self.obs_x < -100 :
            self.score += 1
            self.gw.getCanvas().itemconfig(self.sWin, text=str(self.score))
            self.get_rand_obs()

        if self.gw.pause == False :
            self.gw.getWindow().after(20,self.ObsMotion)

    def DetectCollision(self):

        if (self.obs_x < 150 and self.obs_x + 100 >= 55) and ((self.gw.posY >= self.ghost_pos - 10 and self.gw.posY < self.ghost_pos + 10)  or (self.gw.posY >= self.obs_y - 100)):
            
            self.gw.pause = True
            self.ScoreBoard()
            self.EndGameScreen()
        
        if self.gw.pause == False :
            self.gw.getWindow().after(20,self.DetectCollision)

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
			
    def EndGameScreen(self):
        self.endRectangle = self.gw.getCanvas().create_rectangle(0, 0, 550, 700, fill='#4EC0CA')
        self.endScore = self.gw.getCanvas().create_text(15, 200, text="Your score: " + str(self.score), font='Impact 50', fill='#ffffff', anchor=W)
        self.endBest = self.gw.getCanvas().create_text(15, 280, text="Best score: " + str(self.bestScore), font='Impact 50', fill='#ffffff', anchor=W)


    def RestartGame(self):

        self.gw.posY = 200
        self.obs_x = 550
        self.score = 0
        self.gw.getCanvas().itemconfig(self.sWin, text=str(self.score))
        self.gw.pause = False
        self.gw.getCanvas().delete(self.endScore)
        self.gw.getCanvas().delete(self.endRectangle)
        self.gw.getCanvas().delete(self.endBest)
        self.gw.getCanvas().delete(self.ghostObs)
        self.gw.getCanvas().delete(self.obsFig)

        self.gw.run()

    






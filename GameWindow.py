from tkinter import *
from ObsDynamics import ObsDynamics
from PIL import Image
import tkinter.font as font
import pygame

class GameWindow:
    """This is a singleton class of creating a CANVAS of game window, buttons """

    __instance = None
    @staticmethod
    def getInstance():
        if GameWindow.__instance == None:
            GameWindow()
        return GameWindow.__instance

    def __init__(self) -> None:
       
        if GameWindow.__instance != None:
            raise Exception("This class is a Singleton") 
        else:
            GameWindow.__instance = self
            self.posY = 200
            self.posX = 100
            self.framerate = 20
            self.pause = False 
            self.upcount = 0
            self._window=Tk()
            self.startgame = False

            #Creating witch button just once 
            
            self._window.title("Witchy Witch")
            self._window.geometry('550x700')
            self._window.resizable(width=False,height= False)
            self._canvas = Canvas(self._window, width = 550, height = 700, background = "#10104E")
            img = (Image.open("Background.png"))
            resized_image= img.resize((550,600), Image.Resampling.LANCZOS)
            self.im1 = resized_image.save("Background.png")
            self.background = PhotoImage(file="Background.png")
            self._backimage = self._canvas.create_image(0,0,anchor= NW, image=self.background)
            self.createBtn()
            self._canvas.pack(expand= True)
            self.witchImg = PhotoImage(file="flyingwitch.png")
            self._witch = self._canvas.create_image(self.posX,self.posY,image=self.witchImg)
            self.Obstacles = ObsDynamics(self.getInstance())

    # witch movement functions

    def witchDown(self):
        
        self.posY += 8
        if self.posY >= 700:   
            self.posY= 700
            self.pause = True
            self.Obstacles.ScoreBoard()
            self.Obstacles.EndGameScreen()

        self._canvas.coords(self._witch,self.posX, self.posY)    
        if self.pause == False :
            self._window.after(self.framerate,self.witchDown) 

    def witchUp(self,event = None):

        if self.pause == False: 
            self.posY-= 20
            if self.posY <= 0:
                self.pause = True
                self.Obstacles.ScoreBoard()
                self.Obstacles.EndGameScreen()
            self._canvas.coords(self._witch, self.posX, self.posY)  
            if self.upcount < 5:
                self.upcount += 1
                self._window.after(self.framerate,self.witchUp) 
               
            else: self.upcount = 0  


    def getCanvas(self):        
        return self._canvas
    def getWindow(self):
        return self._window

    def callback(self):
        self.startgame = True
        pygame.mixer.init()
        pygame.mixer.music.load("1.mp3")
        pygame.mixer.music.play(loops=30)
        

    def createBtn(self):   
        self.title = self._canvas.create_text(100, 250, text="Witchy Witch!", font='Impact 50', fill='#FFD700', anchor=W)       
        self.button = Button(self._window,text ="Start Game",pady=30, bg ="red",command = self.callback)
        self.button['font'] = font.Font(size = 30)
      
        self.start = self._canvas.create_window(275,400,window = self.button)
 
    def run(self):
        "Run application"
        
        if self.startgame :
            # after pressing the start button , start the game
            
            self._window.after(self.framerate,self.witchDown)
            self._window.after(self.framerate,self.Obstacles.get_rand_obs)
            self._window.after(self.framerate,self.Obstacles.ObsMotion)
            self._window.after(self.framerate,self.Obstacles.DetectCollision)
            self._window.bind("<space>", self.witchUp)
            self._canvas.delete(self.start)
            self._canvas.delete(self.title)
        else :
            self._window.after(200,self.run)
        self._window.mainloop()



def main():

    "EntryPoint"
    gw = GameWindow.getInstance()
    gw.run()

if __name__ == '__main__':
    main()
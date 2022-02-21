# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 14:03:41 2022

@author: Tom
"""

from tkinter import *
from tkinter import ttk
import random
import os

class mainWindow:
    def __init__(self,root):
        def play():
            playingwindow=Toplevel(root)
            gameWindow(playingwindow,root,self)
        def leaderboardopen():
            scorewindow=Toplevel(root)
            leaderBoard(scorewindow,self.leaderboard)
            scorewindow.geometry("")
        def settings():
            return 0
        def exitgame():
            root.destroy()
        self.leaderboard = []
        self.leaderboardtemp=[]
        try:
            leaderfile = open("scores.txt", "r")
            self.leaderboardtemp=leaderfile.readlines()
            for i in self.leaderboardtemp:
                self.leaderboard.append(int(i))
            leaderfile.close()
        except:
            print("No scores to load")
        root.title("Snake Game")
        root.geometry("400x300")
        mainframe = ttk.Frame(root, padding=("12 12 12 12"))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure([0,1,2,3], weight=1)
        ttk.Button(mainframe, text="Play", command=play).grid(column=0, row=0)
        ttk.Button(mainframe, text="Leaderboard", command=leaderboardopen).grid(column=0, row=1)
        ttk.Button(mainframe, text="Settings", command=settings).grid(column=0, row=2)
        ttk.Button(mainframe, text="Exit", command=exitgame).grid(column=0, row=3)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
    def newScore(self,score):
        self.leaderboard.append(score)
        self.leaderboard.sort(reverse=True)
        self.leaderboard=self.leaderboard[:11]
        self.saveScore()
    def saveScore(self):
        try:
            os.remove("scores.txt")
            leaderfile = open("scores.txt","x")
            for i in self.leaderboard:
                leaderfile.write(str(i)+"\n")
        except:
            print("Couldn't save scores")

class leaderBoard:
    def __init__(self,window,scores):
        window.title("High Scores")
        windowmainframe = ttk.Frame(window, padding=("3 3 3 3"))
        windowmainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        i=1
        for score in scores:
            ttk.Label(windowmainframe, text="".join([str(i),".  ",str(score)])).grid(column=0,row=i+1)
            i+=1
        windowmainframe.columnconfigure(0, weight=1)
        for child in windowmainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

class gameWindow:
    def __init__(self, window, masterWindow, parentObject):
        def gamequit():
            self.window.destroy()
        def gameStart():
            gameInternal(gameframe,self.squares,self,masterWindow)
        def keyPress(event):
            if event.char=="w" and self.currentDirection!=0:
                self.latestDirection=2
            elif event.char=="d" and self.currentDirection!=3:
                self.latestDirection=1
            elif event.char=="s" and self.currentDirection!=2:
                self.latestDirection=0
            elif event.char=="a" and self.currentDirection!=1:
                self.latestDirection=3
        self.window = window
        self.latestDirection=1
        self.currentDirection=1
        self.parentObject=parentObject
        window.bind("<Key>",keyPress)
        window.title("Snake Game")
        windowmainframe = ttk.Frame(window, padding=("3 3 3 3"))
        windowmainframe.grid(column=0, row=0, sticky="nesw")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        gameframe = ttk.Frame(windowmainframe)
        gameframe.grid(column=0,row=0,rowspan=3)
        scorelblstatic = ttk.Label(windowmainframe, text="Score:")
        scorelblstatic.grid(column=1,row=0)
        self.scorelbl = ttk.Label(windowmainframe, text="0")
        self.scorelbl.grid(column=1,row=1)
        buttonframe=ttk.Frame(windowmainframe)
        buttonframe.grid(column=1,row=2)
        playbtn=ttk.Button(buttonframe, text="Play", command=gameStart)
        playbtn.grid(column=0, row=0)
        exitbtn=ttk.Button(buttonframe, text="Quit", command=gamequit)
        exitbtn.grid(column=0, row=1)
        self.squares=[]
        style=ttk.Style()
        style.configure('background.TFrame', background='white', relief=GROOVE)
        style.configure('head.TFrame', background='red', relief=GROOVE)
        style.configure('body.TFrame', background='yellow', relief=GROOVE)
        style.configure('food.TFrame', background='green', relief=GROOVE)
        for i in range(0,13):
            templist=[]
            for j in range(0,13):
                templist.append(ttk.Frame(master=gameframe, height=20, width=20, style='background.TFrame'))
                templist[j].grid(column=i, row=j)
            self.squares.append(templist)
        self.squares[6][6]['style']='head.TFrame'

    def updateScore(self, score):
        self.scorelbl['text']=str(score)
    def updateSquare(self,coord,style):
        self.squares[coord[0]][coord[1]]['style']=style


class gameInternal: #1=N,2=E,3=S,4=W .... [x,y]
    def __init__(self, gameFrame, squares, parentWindow, masterWindow):
        self.score=0
        self.bodyPoints=[[6,6]]
        self.directionToCoord=[[0,1],[1,0],[0,-1],[-1,0]]
        self.parentWindow=parentWindow
        self.masterWindow=masterWindow
        self.keepGoing=True
        self.foodLocation = self.newFoodLocation()
        while (self.foodLocation==[6,6]):
            self.foodLocation = self.newFoodLocation()
        squares[self.foodLocation[0]][self.foodLocation[1]]['style']='food.TFrame'
        self.runGame()
    def runGame(self):
        if self.keepGoing:
            self.gameTick()
            self.masterWindow.update_idletasks()
            self.masterWindow.after(100,self.runGame)
        else:
            messagebox.showerror("Game Over", "You score was "+str(self.score))
            self.parentWindow.window.destroy()
            self.parentWindow.parentObject.newScore(self.score)

    def newFoodLocation(self):
        return [random.randrange(0,13),random.randrange(0,13)]
    
    @staticmethod
    def addCoords(a,b):
        return [a[0]+b[0],a[1]+b[1]]

    def gameTick(self):
        nextPoint=self.addCoords(self.bodyPoints[0],self.directionToCoord[self.parentWindow.latestDirection])
        if nextPoint in self.bodyPoints:
            self.gameOver()
            return
        if max(nextPoint[0],nextPoint[1])>12 or min(nextPoint[0],nextPoint[1])<0:
            self.gameOver()
            return

        self.bodyPoints.insert(0,nextPoint)

        if self.foodLocation!=self.bodyPoints[0]:
            self.bodyPoints.pop()
        else:
            self.score=self.score+1
            self.parentWindow.updateScore(self.score)
            while self.foodLocation in self.bodyPoints:
                self.foodLocation=self.newFoodLocation()
        self.parentWindow.currentDirection=self.parentWindow.latestDirection
        self.drawScreen()

    def drawScreen(self):
        #Background
        for i in range(0,13):
            for j in range(0,13):
                self.parentWindow.updateSquare([i,j], 'background.TFrame')

        #Food
        self.parentWindow.updateSquare(self.foodLocation, 'food.TFrame')

        #Head
        self.parentWindow.updateSquare(self.bodyPoints[0], 'head.TFrame')

        #Body
        for point in self.bodyPoints[1:]:
            self.parentWindow.updateSquare(point, 'body.TFrame')

    def gameOver(self):
        self.keepGoing=False

root=Tk()
mainWindow(root)
root.mainloop()
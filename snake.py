# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 14:03:41 2022

@author: Tom
"""

import tkinter
from tkinter import ttk
import random
import os

class MainWindow:
    """
    A class used to create the top level window of the GUI.

    '''

    Attrubutes
    ----------
    leaderboard : list
        The top 10 scores stored as integers in descending order.

    Methods
    -------
    new_score(score):
        Add a new score to the leaderboard.
    """
    def __init__(self,internal_root):
        def play():
            playingwindow=tkinter.Toplevel(internal_root)
            GameWindow(playingwindow,internal_root,self)
        def leaderboard_open():
            scorewindow=tkinter.Toplevel(internal_root)
            scorewindow.title("High Scores")
            windowmainframe = ttk.Frame(scorewindow, padding=("3 3 3 3"))
            windowmainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W,
                                                          tkinter.E, tkinter.S))
            scorewindow.columnconfigure(0, weight=1)
            scorewindow.rowconfigure(0, weight=1)
            i=1
            for score in self.leaderboard:
                temp=ttk.Label(windowmainframe,
                               text="".join([str(i),".  ",str(score)]))
                temp.grid(column=0,row=i+1)
                i+=1
            windowmainframe.columnconfigure(0, weight=1)
            for child in windowmainframe.winfo_children():
                child.grid_configure(padx=5, pady=5)
            scorewindow.geometry("")
        def settings():
            return 0
        def exitgame():
            internal_root.destroy()
        self.leaderboard = []
        leaderboardtemp=[]
        try:
            leaderfile = open("scores.txt", "r")
            leaderboardtemp=leaderfile.readlines()
            for i in leaderboardtemp:
                self.leaderboard.append(int(i))
            leaderfile.close()
        except: # pylint: disable=bare-except
            print("No scores to load")
        internal_root.title("Snake Game")
        internal_root.geometry("400x300")
        mainframe = ttk.Frame(internal_root, padding=("12 12 12 12"))
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W,
                                                tkinter.E, tkinter.S))
        internal_root.columnconfigure(0, weight=1)
        internal_root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure([0,1,2,3], weight=1)
        ttk.Button(mainframe, text="Play", command=play).grid(column=0, row=0)
        ttk.Button(mainframe, text="Leaderboard", command=leaderboard_open).grid(column=0, row=1)
        ttk.Button(mainframe, text="Settings", command=settings).grid(column=0, row=2)
        ttk.Button(mainframe, text="Exit", command=exitgame).grid(column=0, row=3)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
    def new_score(self,score):
        """
        Adds a new score to the leaderboard list.
        Append the score to the list, sort the list into descending order,
        truncate to the largest 10 scores, save the list to disc.

        Parameters
        ----------
        score : integer
            The new score to be added to the leaderboard.

        Returns
        -------
        None.

        """
        self.leaderboard.append(score)
        self.leaderboard.sort(reverse=True)
        self.leaderboard=self.leaderboard[:10]
        self._save_score()

    def _save_score(self):
        try:
            os.remove("scores.txt")
            leaderfile = open("scores.txt","x")
            for i in self.leaderboard:
                leaderfile.write(str(i)+"\n")
        except: # pylint: disable=bare-except
            print("Couldn't save scores")

class GameWindow:
    """
    A class used to create the game window GUI and manage user input.

    '''

    Attributes
    ----------
    window : tkinter TopLevel object
        The window object containing the game.
    latest_direction : integer
        An integer between 1 and 4 representing the direction the user inputs
        for the next game tick.
    current_direction : integer
        An integer between 1 and 4 representing the direction of movement of
        the current game tick.
    parent_object : MainWindow class object
        The MainWindow class object which created this window.
    scorelbl : tkinter Label object
        The label displaying the current score.
    squares : list
        A 2D list representing the grid of squares comprising the game grid.

    Methods
    -------
    update_score(score):
        Update the score shown to the user to the given value.
    update_square(coord,style):
        Change the square at the given coordinate to the given style.
    """
    def __init__(self, window, master_window, parentObject):
        def game_quit():
            self.window.destroy()
        def game_start():
            GameInternal(self.squares,self,master_window)
        def key_press(event):
            if event.char=="w" and self.current_direction!=0:
                self.latest_direction=2
            elif event.char=="d" and self.current_direction!=3:
                self.latest_direction=1
            elif event.char=="s" and self.current_direction!=2:
                self.latest_direction=0
            elif event.char=="a" and self.current_direction!=1:
                self.latest_direction=3
        self.window = window
        self.latest_direction=1
        self.current_direction=1
        self.parent_object=parentObject
        window.bind("<Key>",key_press)
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
        playbtn=ttk.Button(buttonframe, text="Play", command=game_start)
        playbtn.grid(column=0, row=0)
        exitbtn=ttk.Button(buttonframe, text="Quit", command=game_quit)
        exitbtn.grid(column=0, row=1)
        self.squares=[]
        style=ttk.Style()
        style.configure('background.TFrame', background='white',
                        relief=tkinter.GROOVE)
        style.configure('head.TFrame', background='red',
                        relief=tkinter.GROOVE)
        style.configure('body.TFrame', background='yellow',
                        relief=tkinter.GROOVE)
        style.configure('food.TFrame', background='green',
                        relief=tkinter.GROOVE)
        for i in range(0,13):
            templist=[]
            for j in range(0,13):
                templist.append(ttk.Frame(master=gameframe,
                                          height=20,
                                          width=20,
                                          style='background.TFrame'))
                templist[j].grid(column=i, row=j)
            self.squares.append(templist)
        self.squares[6][6]['style']='head.TFrame'

    def update_score(self, score):
        """
        Update the score shown to the user.

        Parameters
        ----------
        score : integer
            The number to be displayed as the current score.

        Returns
        -------
        None.

        """
        self.scorelbl['text']=str(score)
    def update_square(self,coord,style):
        """
        Updates the square at the coordinate to the given style.

        Parameters
        ----------
        coord : list
            A list of length 2. The first entry is the x coordinate, the
            second entry is the y coordinate.
        style : string
            The style to change the square to. Possible styles are
            'background.TFrame', 'food.TFrame', 'head.TFrame', 'body.TFrame'.

        Returns
        -------
        None.

        """
        self.squares[coord[0]][coord[1]]['style']=style


class GameInternal: #1=N,2=E,3=S,4=W .... [x,y]
    """
    A class for containing the game logic.

    '''

    Attributes
    ----------
    score : integer
        The current score.
    body_points : list
        A list of coordintes (in the form of a length 2 list) of the points
        where the snakes body is (with the first being the head).
    direction_to_coord : list
        A list of vectors which relates an integer between 1 and 4
        (the direction) as the index to a unit direction.
    parent_window : GameWindow class object
        The GameWindow object which created this instance.
    master_window : MainWindow class object
        The MainWindow object which created the parent of the parent_window.
    keep_going : Boolean
        A check which is used to tell when the game should end.
    food_location : list
        A length 2 list which stores the coordinates of where the food
        currently is.

    Methods
    -------
    run_game():
        A function to check if the game and running & schedulling the next
        tick if so. Also manages ending the game.
    new_food_location():
        A function which gives an empty square. Used to find somewhere to
        spawn a new food.
    game_tick():
        Processes a single game tick.
    draw_screen():
        Updates the display.
    game_over():
        Sets the boolean check to end the game to False.
    """
    def __init__(self, squares, parent_window, master_window):
        self.score=0
        self.body_points=[[6,6]]
        self.direction_to_coord=[[0,1],[1,0],[0,-1],[-1,0]]
        self.parent_window=parent_window
        self.master_window=master_window
        self.keep_going=True
        self.food_location = self.new_food_location()
        while (self.food_location==[6,6]):
            self.food_location = self.new_food_location()
        squares[self.food_location[0]][self.food_location[1]]['style']='food.TFrame'
        self.run_game()
    def run_game(self):
        """
        Manages running the game, scheduling next ticks and ending the game.

        Returns
        -------
        None.

        """
        if self.keep_going:
            self.game_tick()
            self.master_window.update_idletasks()
            self.master_window.after(100,self.run_game)
        else:
            tkinter.messagebox.showerror("Game Over",
                                         "You score was "+str(self.score))
            self.parent_window.window.destroy()
            self.parent_window.parent_object.new_score(self.score)

    def new_food_location(self):
        """
        Used for generating a location for spawning new food.

        Returns
        -------
        list
            A length 2 list representing coordinates of an empty space
            intended to be a location when spawning new food.

        """
        return [random.randrange(0,13),random.randrange(0,13)]
    @staticmethod
    def add_coords(vector_a,vector_b):
        """
        Adds two length 2 lists together pointwise

        Parameters
        ----------
        vector_a : list
            A length 2 list representing coordinates.
        vector_b : list
            A length 2 list representing coordinates.

        Returns
        -------
        list
            The pointwise sum of the two input vectors.

        """
        return [vector_a[0]+vector_b[0],vector_a[1]+vector_b[1]]

    def game_tick(self):
        """
        A function to run a single tick of the game and update the screen

        Returns
        -------
        None.

        """
        next_point=self.add_coords(
            self.body_points[0],
            self.direction_to_coord[self.parent_window.latest_direction])

        if next_point in self.body_points:
            self.game_over()
            return
        if max(next_point[0],next_point[1])>12 or min(next_point[0],next_point[1])<0:
            self.game_over()
            return

        self.body_points.insert(0,next_point)

        if self.food_location!=self.body_points[0]:
            self.body_points.pop()
        else:
            self.score=self.score+1
            self.parent_window.update_score(self.score)
            while self.food_location in self.body_points:
                self.food_location=self.new_food_location()
        self.parent_window.current_direction=self.parent_window.latest_direction
        self.draw_screen()

    def draw_screen(self):
        """
        Updates the styles of the squares in order to update what is shown to
        the user.

        Returns
        -------
        None.

        """
        #Background
        for i in range(0,13):
            for j in range(0,13):
                self.parent_window.update_square([i,j], 'background.TFrame')

        #Food
        self.parent_window.update_square(self.food_location, 'food.TFrame')

        #Head
        self.parent_window.update_square(self.body_points[0], 'head.TFrame')

        #Body
        for point in self.body_points[1:]:
            self.parent_window.update_square(point, 'body.TFrame')

    def game_over(self):
        """
        Sets the keep_going variable to false in order to end the game

        Returns
        -------
        None.

        """
        self.keep_going=False

root=tkinter.Tk()
MainWindow(root)
root.mainloop()

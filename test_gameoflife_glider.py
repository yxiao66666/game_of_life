# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution

Created on Tue Jan 15 12:37:52 2019

@author: shakes
"""
import conway

#N = 64

# Part E
#N = 1024

# Part G
N = 2048

#create the game of life object
life = conway.GameOfLife(N)

# Part A
#life.insertBlinker((30,10))

# Part B
#life.insertGlider((35,20))

# Part C
#life.insertGliderGun((0,0))

# Part D P5_diamond New_gun_1 30P25_oscillator 
# Part E P59_glidergun
#life.insertFromPlainText('C:\\Users\\29448\\OneDrive\\Documents\\Uni Study\\Year 3\\Semester 1\\COMP2048\\Assessment\\Assignment 2\\P59_glidergun.txt')

# Part F gosperglidergun Lightweight_spaceship Centinal_reflector
# Part G turingmachine
with open('C:\\Users\\29448\\OneDrive\\Documents\\Uni Study\\Year 3\\Semester 1\\COMP2048\\Assessment\\Assignment 2\\turingmachine.rle', 'r') as file:
    rle_content = file.read()   

life.insertFromRLE(rle_content)

cells = life.getStates() #initial state

#-------------------------------
#plot cells
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

plt.gray()

img = plt.imshow(cells, animated=True)

def animate(i):
    """perform animation step"""
    global life
    
    life.evolve()
    cellsUpdated = life.getStates()
    
    img.set_array(cellsUpdated)
    
    return img,

interval = 200 #ms

#animate 24 frames with interval between them calling animate function at each frame
ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)

plt.show()


# https://upload.wikimedia.org/wikipedia/commons/9/96/Animated_glider_emblem.gif

"""
Part H
Game of Life is Turing complete as it can simulate behaviours of a universal constructor or any other Turing machine.

References
Rendell, P. (n.d.). This is a Turing Machine implemented in Conway's Game of Life. 
Retrieved from Rendell-attic: http://rendell-attic.org/gol/tm.htm

Wikipedia. (2024). Conway's Game of Life. 
Retrieved from Wikipedia: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#:~:text=It%20is%20Turing%20complete%20and,or%20any%20other%20Turing%20machine.


"""
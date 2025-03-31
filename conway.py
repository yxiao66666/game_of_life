# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

Created on Tue Jan 15 12:21:17 2019

@author: shakes
"""
import numpy as np
from scipy import signal
import rle

class GameOfLife:
    '''
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    '''
    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N,N), np.int64)
        # Weighted sum of neighbors 
        self.neighborhood = np.ones((3,3), np.int64) # 8 connected kernel
        self.neighborhood[1,1] = 0 #do not count centre pixel

        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        
    def getStates(self):
        '''
        Returns the current states of the cells
        '''
        return self.grid
    
    def getGrid(self):
        '''
        Same as getStates()
        '''
        return self.getStates()
               
    def evolve(self):
        '''
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
        '''
        #get weighted sum of neighbors
        #PART A & E CODE HERE
        neighbors_count = self.get_weighted_sum()

        #implement the GoL rules by thresholding the weights
        #PART A CODE HERE
        self.grid[(self.grid == self.aliveValue) & (neighbors_count < 2)] = self.deadValue  # Underpopulation
        self.grid[(self.grid == self.aliveValue) & (neighbors_count.any() == 2 or neighbors_count.any() == 3)] = self.aliveValue  # Survival
        self.grid[(self.grid == self.aliveValue) & (neighbors_count > 3)] = self.deadValue  # Overpopulation
        self.grid[(self.grid == self.deadValue) & (neighbors_count == 3)] = self.aliveValue  # Reproduction

        #update the grid
#        self.grid = #UNCOMMENT THIS WITH YOUR UPDATED GRID
        self.grid = np.copy(self.grid)
    
    def get_weighted_sum(self):
        '''
        Calculate the weighted sum of neighbors for each cell.
        '''
        # Define the weights for the neighbors
        weights = self.neighborhood
        
        # Convolve the grid with the weights
        neighbors_count = signal.convolve(self.grid, weights, mode='same')
        
        return neighbors_count


    def insertBlinker(self, index=(0,0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        
    def insertGlider(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+2] = self.aliveValue
        self.grid[index[0]+2, index[1]] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+2] = self.aliveValue
        
    def insertGliderGun(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0]+1, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+2, index[1]+23] = self.aliveValue
        self.grid[index[0]+2, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+3, index[1]+13] = self.aliveValue
        self.grid[index[0]+3, index[1]+14] = self.aliveValue
        self.grid[index[0]+3, index[1]+21] = self.aliveValue
        self.grid[index[0]+3, index[1]+22] = self.aliveValue
        self.grid[index[0]+3, index[1]+35] = self.aliveValue
        self.grid[index[0]+3, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+4, index[1]+12] = self.aliveValue
        self.grid[index[0]+4, index[1]+16] = self.aliveValue
        self.grid[index[0]+4, index[1]+21] = self.aliveValue
        self.grid[index[0]+4, index[1]+22] = self.aliveValue
        self.grid[index[0]+4, index[1]+35] = self.aliveValue
        self.grid[index[0]+4, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+5, index[1]+1] = self.aliveValue
        self.grid[index[0]+5, index[1]+2] = self.aliveValue
        self.grid[index[0]+5, index[1]+11] = self.aliveValue
        self.grid[index[0]+5, index[1]+17] = self.aliveValue
        self.grid[index[0]+5, index[1]+21] = self.aliveValue
        self.grid[index[0]+5, index[1]+22] = self.aliveValue
        
        # 6th
        self.grid[index[0]+6, index[1]+1] = self.aliveValue
        self.grid[index[0]+6, index[1]+2] = self.aliveValue
        self.grid[index[0]+6, index[1]+11] = self.aliveValue
        self.grid[index[0]+6, index[1]+15] = self.aliveValue
        self.grid[index[0]+6, index[1]+17] = self.aliveValue # 17
        self.grid[index[0]+6, index[1]+18] = self.aliveValue # 17
        self.grid[index[0]+6, index[1]+23] = self.aliveValue
        self.grid[index[0]+6, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+7, index[1]+11] = self.aliveValue
        self.grid[index[0]+7, index[1]+17] = self.aliveValue
        self.grid[index[0]+7, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+8, index[1]+12] = self.aliveValue
        self.grid[index[0]+8, index[1]+16] = self.aliveValue
        
        self.grid[index[0]+9, index[1]+13] = self.aliveValue
        self.grid[index[0]+9, index[1]+14] = self.aliveValue

    def insertFromPlainText(self, txtString, pad=0):
        '''
        Assumes txtString contains the entire pattern as a human readable pattern without comments
        '''
        with open(txtString, 'r') as file:
            lines = file.readlines()
            # Iterate over each line in the file
            for y, line in enumerate(lines):
                if line.startswith('!'):
                    # Ignore comments
                    continue
                # Iterate over each character in the line
                for x, char in enumerate(line.strip()):
                    if char == 'O':
                        # Alive cell
                        self.grid[y + pad, x + pad] = self.aliveValue
        
    def insertFromRLE(self, rleString, pad=0):
        '''
        Given string loaded from RLE file, populate the game grid
        '''
        # Initialise the given RunLengthEncodedParser
        rle_parser = rle.RunLengthEncodedParser(rleString)

        # Get pattern size
        size_x = rle_parser.size_x
        size_y = rle_parser.size_y
        print(size_x)
        print(size_y)

        # Get the pattern 2D array
        pattern_array = rle_parser.pattern_2d_array

        # Iterate over each line of the pattern
        for y, line in enumerate(pattern_array):
            # Iterate over each character in the line
            for x, char in enumerate(line):
                if char == 'o':
                    # Alive cell
                    self.grid[y + pad, x + pad] = self.aliveValue








"""
References
ChatGPT. (2024). In Respond to "what does convolve2d do in python". 
Retrieved from OpenAI: https://chat.openai.com/share/c19d31fa-1823-4835-9f1f-e65eca96f751

Matchew. (2011, Jun 24). Basic python file-io variables with enumerate [duplicate]. 
Retrieved from Stackoverflow: https://stackoverflow.com/questions/6473283/basic-python-file-io-variables-with-enumerate

SciPy. (2024). scipy.signal.convolve. 
Retrieved from SciPy documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve.html

SciPy. (2024). scipy.signal.convolve2d. 
Retrieved from SciPy documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html

"""
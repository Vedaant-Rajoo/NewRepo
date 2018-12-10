#made by memory leak for HACK 2.0
#vedaant rajoo IIITU17148
#game 2048 using pygame module
#

import pygame, sys, time
from pygame.locals import *
from colours import *
from random import *

t_points = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4

pygame.init()

SURFACE = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption("Lets play 2048!!!")

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]    #the intial matrix
undoMat = []                   #the undo matrix is empty
''' the main
	function for the game'''

def main(fromLoaded = False):

	if not fromLoaded:
		placeRandomTile()
		placeRandomTile()

	printMatrix()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if checkIfCanGo() == True:
				if event.type == KEYDOWN:        #when a key is pressed
					if isArrow(event.key):   #when arrow key is pressed
						rotations = getRotations(event.key)

						addToUndo()

						for i in range(0, rotations):
							rotateMatrixClockwise()   #rotate the board clockwise

						if canMove():           #if available to move
							moveTiles()
							mergeTiles()
							placeRandomTile()

						for j in range(0, (4 - rotations) % 4):
							rotateMatrixClockwise()

						printMatrix()
			else:
				printGameOver()         #game over.....................................................................................................................................

			if event.type == KEYDOWN:
				global BOARD_SIZE

				if event.key == pygame.K_r:    #reset on r
					reset()

				if 50 < event.key and 56 > event.key:
					BOARD_SIZE = event.key - 48
					reset()

				if event.key == pygame.K_s:    #save the state on s
					saveGameState()
				elif event.key == pygame.K_l:  #load the state of the matrix on l
					loadGameState()
				elif event.key == pygame.K_u:  #undo on u
					undo()

		pygame.display.update()
'''returning the matrix after the chance is played'''
'''changing the colors to different boxes'''

def printMatrix():

	SURFACE.fill(BLACK)      #filling the background with 'black'

	global BOARD_SIZE
	global t_points

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			pygame.draw.rect(SURFACE, getColour(tileMatrix[i][j]), (i*(400/BOARD_SIZE), j*(400/BOARD_SIZE) + 100, 400/BOARD_SIZE, 400/BOARD_SIZE))  #drawing a rectangle   #importing colors.py function
			
			label = myfont.render(str(tileMatrix[i][j]), 1, (255,255,255))                #render(text, antialias, color, background=None)
			label2 = scorefont.render("Score:" + str(t_points), 1, (255, 255, 255))

			SURFACE.blit(label, (i*(400/BOARD_SIZE) + 30, j*(400/BOARD_SIZE) + 130))      #blit(source, dest, area=None, special_flags = 0) -> Rect
			SURFACE.blit(label2, (10, 20))
'''the final noover gameover function'''

def printGameOver():
	global t_points

	SURFACE.fill(BLACK)

	label = scorefont.render("Game Over!", 1, (255,255,255))
	label2 = scorefont.render("Score:" + str(t_points), 1, (255,255,255))
	label3 = myfont.render("Press r to restart!", 1, (255,255,255))

	SURFACE.blit(label, (50, 100))
	SURFACE.blit(label2, (50, 200))
	SURFACE.blit(label3, (50, 300))
'''placing a random tile after a step is played'''
def placeRandomTile():
	count = 0         #initiating a counter
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if tileMatrix[i][j] == 0:   #if the tile is zero...then the random tile can be placed
				count += 1   #so if count is nonzero

	k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:
		k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2
'''returning the same value'''
def floor(n):
	return int(n - (n % 1))

def moveTiles():
	                                                                                    # We want to work column by column shifting up each element in turn.
	for i in range(0, BOARD_SIZE):                                                      # Work through our 4 columns.
		for j in range(0, BOARD_SIZE - 1):                                          # Now consider shifting up each element by checking top 3 elements if 0.
			while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:         # If any element is 0 and there is a number to shift we want to shift up elements below.
				for k in range(j, BOARD_SIZE - 1):                          # Move up elements below.
					tileMatrix[i][k] = tileMatrix[i][k + 1]             # Move up each element one.
				tileMatrix[i][BOARD_SIZE - 1] = 0

def mergeTiles():
	global t_points

	for i in range(0, BOARD_SIZE):
		for k in range(0, BOARD_SIZE - 1):
				if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
					tileMatrix[i][k] = tileMatrix[i][k] * 2
					tileMatrix[i][k + 1] = 0
					t_points += tileMatrix[i][k]
					moveTiles()

def checkIfCanGo():
	for i in range(0, BOARD_SIZE ** 2):
		if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
			return True

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE - 1):
			if tileMatrix[i][j] == tileMatrix[i][j + 1]:
				return True
			elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
				return True
	return False

def reset():
	global t_points
	global tileMatrix

	t_points = 0
	SURFACE.fill(BLACK)

	tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

	main()

def canMove():
	for i in range(0, BOARD_SIZE):
		for j in range(1, BOARD_SIZE):
			if tileMatrix[i][j-1] == 0 and tileMatrix[i][j] > 0:
				return True
			elif (tileMatrix[i][j-1] == tileMatrix[i][j]) and tileMatrix[i][j-1] != 0:
				return True

	return False

def saveGameState():
	f = open("savedata", "w")

	line1 = " ".join([str(tileMatrix[floor(x / BOARD_SIZE)][x % BOARD_SIZE]) for x in range(0, BOARD_SIZE**2)])
	
	f.write(line1 + "\n")
	f.write(str(BOARD_SIZE)  + "\n")
	f.write(str(t_points))
	f.close()

def loadGameState():
	global t_points    #declaring all te variables global makes them immutable
	global BOARD_SIZE
	global tileMatrix

	f = open("savedata", "r")   #opening the file for reading

	mat = (f.readline()).split(' ', BOARD_SIZE ** 2)
	BOARD_SIZE = int(f.readline())
	t_points = int(f.readline())

	for i in range(0, BOARD_SIZE ** 2):
		tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = int(mat[i])

	f.close()

	main(True)
''' function to just rotate the board clockwise'''

def rotateMatrixClockwise():
	for i in range(0, int(BOARD_SIZE/2)):
		for k in range(i, BOARD_SIZE- i - 1):
			temp1 = tileMatrix[i][k]
			temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
			temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
			temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

			tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
			tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
			tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
			tileMatrix[i][k] = temp4
'''to check if an arrow key is pressed'''

def isArrow(k):
	return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)   # returning the arrow key pressed   # to return true or false
#the variable rotations
def getRotations(k):
	if k == pygame.K_UP:     #to confirm that each arrow key can rotate the board similarly
		return 0
	elif k == pygame.K_DOWN:
		return 2
	elif k == pygame.K_LEFT:
		return 1
	elif k == pygame.K_RIGHT:
		return 3
'''conver to linear matrixfor file appending'''		
def convertToLinearMatrix():
	mat = []

	for i in range(0, BOARD_SIZE ** 2):
		mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

	mat.append(t_points)

	return mat
'''adding to the undo matrix for saving and loafing function'''
def addToUndo():
	undoMat.append(convertToLinearMatrix())

def undo():
	if len(undoMat) > 0:     #if the undo matrix is non empty..
		mat = undoMat.pop()   #remove the entry

		for i in range(0, BOARD_SIZE ** 2):
			tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]

		global t_points
		t_points = mat[BOARD_SIZE ** 2]

		printMatrix()

main()

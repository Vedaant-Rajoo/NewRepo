#Made by Memory Leak for Hack 2.0
#Vedaant Rajoo - IIITU17148
#2048 game using pygame module
'''import functions'''

import pygame,sys,time
from pygame.locals import *
from colours import *
from random import *
'''variables to be used'''

TOTAL_POINTS = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4
'''initiating the pygame module and setting the screen'''

pygame.init()
SURFACE = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption("Lets Play 2048!!!")

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []
'''yeh main hai'''
def main(fromLoaded = False):

	if not fromLoaded:
		placeRandomTile()
		placeRandomTile()

	printMatrix()
'''yeh likhna zarrori hai'''
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if checkIfCanGo() == True:
				if event.type == KEYDOWN:
					if isArrow(event.key):
						rotations = getRotations(event.key)

						addToUndo()

						for i in range(0, rotations):
							rotateMatrixClockwise()

						if canMove():
							moveTiles()
							mergeTiles()
							placeRandomTile()

						for j in range(0, (4 - rotations) % 4):
							rotateMatrixClockwise()

						printMatrix()
			else:
				printGameOver()

			if event.type == KEYDOWN:
				global BOARD_SIZE

				if event.key == pygame.K_r:    #r to be pressed for resetting the game
					reset()

				if 50 < event.key and 56 > event.key:
					BOARD_SIZE = event.key - 48
					reset()

				if event.key == pygame.K_s:     #if s is pressed
					saveGameState()
				elif event.key == pygame.K_l:   #if l is pressed
					loadGameState()
				elif event.key == pygame.K_u:   #if u is pressed
					undo()

		pygame.display.update()
''' isse matrix print hogi ar game chaalu hoga'''

def printMatrix():

	SURFACE.fill(BLACK)    # isse background black hoga

	global BOARD_SIZE     #both the variables to be declared global
	global TOTAL_POINTS

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):   #nesting of two for range loops
			pygame.draw.rect(SURFACE, getColour(tileMatrix[i][j]), (i*(400/BOARD_SIZE), j*(400/BOARD_SIZE) + 100, 400/BOARD_SIZE, 400/BOARD_SIZE)) # setting the size of the square(rect)

			label = myfont.render(str(tileMatrix[i][j]), 1, (255,255,255))                 #render(text, antialias, color, background=None) -> Surface
			label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))    #displaying the t_score onto the screen

			SURFACE.blit(label, (i*(400/BOARD_SIZE) + 30, j*(400/BOARD_SIZE) + 130))       #pygame.surface.blit-->used to draw one image onto other
			SURFACE.blit(label2, (10, 20))                                                 #blit(source, destination, area=None, special_flags = 0) -> Rect
''' function-->rendering game over on the screen'''

def printGameOver():
	global TOTAL_POINTS

	SURFACE.fill(BLACK)

	label = scorefont.render("Game Over!", 1, (255,255,255))
	label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255,255,255))
	label3 = myfont.render("Press r to restart!", 1, (255,255,255))              #calling pygame.K_r for reset

	SURFACE.blit(label, (50, 100))
	SURFACE.blit(label2, (50, 200))
	SURFACE.blit(label3, (50, 300))

'''function for placing the random tile anywhere free on the matrix'''

def placeRandomTile():
	count = 0                                   #initialising counter variable
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):      #nesting two for loops
			if tileMatrix[i][j] == 0:   #if the tile is zero..add 1 to the counter
				count += 1

	k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:     #while the tile is not empty
		k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2

def floor(n):
	return int(n - (n % 1)) # returns the same number
'''function-->for moving the tiles around'''

def moveTiles():
	                                                                         # We want to work column by column shifting up each element in turn.
	for i in range(0, BOARD_SIZE):                                               # Work through our 4 columns.
		for j in range(0, BOARD_SIZE - 1):                                   # Now consider shifting up each element by checking top 3 elements if 0.
			while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:  # If any element is 0 and there is a number to shift we want to shift up elements below.
				for k in range(j, BOARD_SIZE - 1):                   # Move up elements below.
					tileMatrix[i][k] = tileMatrix[i][k + 1]      # Move up each element one.
				tileMatrix[i][BOARD_SIZE - 1] = 0
'''the function for now merging two same tiles'''
def mergeTiles():
	global TOTAL_POINTS

	for i in range(0, BOARD_SIZE):
		for k in range(0, BOARD_SIZE - 1):
				if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0: #if the numbered tiles are same merge em
					tileMatrix[i][k] = tileMatrix[i][k] * 2
					tileMatrix[i][k + 1] = 0
					TOTAL_POINTS += tileMatrix[i][k]
					moveTiles()
'''function to check if space available'''
def checkIfCanGo():
	for i in range(0, BOARD_SIZE ** 2):
		if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
			return True

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE - 1):
			if tileMatrix[i][j] == tileMatrix[i][j + 1]:   #checking if adjacent tile empty or not
				return True
			elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
				return True
	return False
'''function calling reset if pressed _r'''
def reset():
	global TOTAL_POINTS
	global tileMatrix

	TOTAL_POINTS = 0
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
'''saving the game matrix'''
def saveGameState():
	f = open("savedata", "w")

	line1 = " ".join([str(tileMatrix[floor(x / BOARD_SIZE)][x % BOARD_SIZE]) for x in range(0, BOARD_SIZE**2)])

	f.write(line1 + "\n")
	f.write(str(BOARD_SIZE)  + "\n")
	f.write(str(TOTAL_POINTS))
	f.close()
'''loading the matrix onto a file'''
def loadGameState():
	global TOTAL_POINTS
	global BOARD_SIZE
	global tileMatrix

	f = open("savedata", "r")

	mat = (f.readline()).split(' ', BOARD_SIZE ** 2)
	BOARD_SIZE = int(f.readline())
	TOTAL_POINTS = int(f.readline())

	for i in range(0, BOARD_SIZE ** 2):
		tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = int(mat[i])

	f.close()

	main(True)

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
'''function for checking which key is pressed'''
def isArrow(k):
	return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)
'''the no. of rotations per key pressed'''
def getRotations(k):
	if k == pygame.K_UP:
		return 0
	elif k == pygame.K_DOWN:
		return 2
	elif k == pygame.K_LEFT:
		return 1
	elif k == pygame.K_RIGHT:
		return 3
'''to be converted into a linear matrix'''
def convertToLinearMatrix():
	mat = []

	for i in range(0, BOARD_SIZE ** 2):
		mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

	mat.append(TOTAL_POINTS)

	return mat
'''adding to the undomatrix the last played step'''
def addToUndo():
	undoMat.append(convertToLinearMatrix())
'''function to conductundo ont the last played step'''
def undo():
	if len(undoMat) > 0:    #if undomat is non empty
		mat = undoMat.pop()

		for i in range(0, BOARD_SIZE ** 2):
			tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]    #saving the last matrix

		global TOTAL_POINTS
		TOTAL_POINTS = mat[BOARD_SIZE ** 2]

		printMatrix()

main()

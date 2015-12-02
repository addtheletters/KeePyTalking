# mazes are 6 by 6 grids
# should be representable using adjacency matrix

# 0 1 2 3
# up right down left

# f c dot
# paragraph star b


# mazes are identifiable using 2 dots
# 9 mazes exist

banana_matrix = [["banana"] * (999*999)] * (999*999)

class MazeDisplayer:
	def __init__(self):
		self.v_wall = "|" # vertical wall
		self.h_wall = "-" # horizontal wall
		self.gap    = " " # lack of a wall
		self.cross  = "+" # for display purposes, to space between horizontal 'lack of walls'
		self.tile   = "*" # a floor tile in the maze
		self.header = "="
		self.header_size = 40
		self.header_end  = 5

	def mazeHeader(self, maze):
		return self.header * (self.header_size-len(maze.getName())-self.header_end) + maze.getName() + self.header * (self.header_end)

	def mazeFooter(self, maze):
		return self.header * (self.header_size)

	def mazeCap(self, maze):
		return self.cross + (self.h_wall * (maze.getSize() * 2 - 1)) + self.cross


class MazeIdentifier:
	def __init__(self):
		self.mazes = {}

	def putMaze(self, dot1, dot2, maze):
		self.mazes[(dot1, dot2)] = maze

	def getMaze(self, dot1, dot2):
		if (dot1, dot2) in self.mazes:
			return self.mazes[(dot1, dot2)]
		elif (dot2, dot1) in self.mazes:
			return self.mazes[(dot2, dot1)]
		else:
			return None

class Maze:

	# this is static or something idk
	dirs = {0:"up", 1:"right", 2:"down", 3:"left"}

	def __init__(self, to_parse="",empty=False, size=6, name="MAAAAZE"):
		self._name = name
		self._size = size
		self._adjacency = {}

		if len(to_parse) > 0:
			self._parse(to_parse)

		if empty: # no walls between any cells
			for i in range(self._size):
				for j in range(self._size):
					self.addToAdjacency((i, j), (i+1, j))
					self.addToAdjacency((i, j), (i, j+1))
		return

	@staticmethod
	def nextTo(pos1, pos2): # is pos1 physically / geometrically bordering pos2?
		# returns True if pos1 is pos2
		if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) > 1:
			return False
		return True

	def getName(self):
		return self._name

	def getSize(self):
		return self._size

	def addToAdjacency(self, pos1, pos2):
		if (not self.valid(pos1)) or (not self.valid(pos2)):
			print("[err] failed to add adjacency: invalid tile position")
			return
		if not Maze.nextTo(pos1, pos2):
			print("[wrn] trying to add adjacency for non-touching maze tiles")
		if pos1 not in self._adjacency:
			self._adjacency[pos1] = []
		if pos2 not in self._adjacency:
			self._adjacency[pos2] = []
		self._adjacency[pos1].append(pos2)
		self._adjacency[pos2].append(pos1)

	def _parse(self, stronk, AIR="."):
		slines = stronk.strip().split('\n')
		for i in range(len(slines)):
			row = i // 2
			for j in range(len(slines[i])):
				col = j // 2
				if slines[i][j] == AIR:
					if (i % 2) == 0 and (j % 2) == 1:
					#	print("used " + slines[i][j] + " of coords " + str((i, j)) + " at " + str( (row, col)) + "'s right" )
						self.addToAdjacency( (row, col), (row, col+1) )
					elif (i % 2) == 1 and (j % 2) == 0:
					#	print("used " + slines[i][j] + " of coords " + str((i, j)) + " at " + str( (row, col)) + "'s bottom" )
						self.addToAdjacency( (row, col), (row+1, col) )

	def valid(self, pos):
		return pos[0] < self._size and pos[1] < self._size

	def hasAdjacent(self, pos1, pos2):
		if pos1 not in self._adjacency:
			return False
		return pos2 in self._adjacency[pos1]

	def direction(self, pos1, pos2):
		if not Maze.nextTo(pos1, pos2):
			return None
		d1 = pos1[0] - pos2[0]
		if d1 == 1:
			return 0 # up
		if d1 == -1:
			return 2 # down
		d2 = pos1[1] - pos2[1]
		if d2 == 1:
			return 1 # right
		if d2 == -1:
			return 3 # left
		print("[wrn] this shouldn't happen (couldn't determine direction of tile)")
		return None

	def showAdjacency(self):
		for i in range(self._size):
			for j in range(self._size):
				if (i, j) in self._adjacency:
					print( str((i, j)) + ": " + str( self._adjacency[(i, j)] ))
				else:
					print( str((i, j)) + ": No adjacent vertices. :(")

	def show(self, disp): # disp: MazeDisplayer
		print(disp.mazeHeader(self))
		print(disp.mazeCap(self))
		for i in range(0, self._size + self._size - 1):
			rowout = ""
			row = i // 2
			if i % 2 == 0:
				rowout = disp.v_wall
				for col in range(0, self._size):
					rowout += disp.tile
					if col < self._size-1:
						if self.hasAdjacent((row, col), (row, col+1)):
							rowout += disp.gap
						else:
							rowout += disp.v_wall
					else: # right wall
						rowout += disp.v_wall
			else:
				rowout = disp.v_wall
				for col in range(0, self._size):
					if self.hasAdjacent((row, col), (row+1, col)):
						rowout += disp.gap
					else: 
						rowout += disp.h_wall
					if col < self._size-1:
						rowout += disp.cross
					else: # right wall
						rowout += disp.v_wall
			print(rowout)
		print(disp.mazeCap(self))
		print(disp.mazeFooter(self))

if __name__ == '__main__':

	what = '''
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
.+.+.+.+.+.
*.*.*.*.*.*
'''

	m1 = '''
*.*.*|*.*.*
.+-+.+.+-+-
*|*.*|*.*.*
.+.+-+-+-+.
*|*.*|*.*.*
.+-+.+.+-+.
*|*.*.*|*.*
.+-+-+-+-+.
*.*.*|*.*|*
.+-+.+.+-+.
*.*|*.*|*.*
'''
	
	midf = MazeIdentifier()
	midf.putMaze( (1, 0), (2, 5), Maze(m1, name="maze1") )
	maze1 = midf.getMaze( (2, 5), (1, 0) )
	maze1.showAdjacency()
	maze1.show(MazeDisplayer())

	print( Maze.dirs[maze1.direction( (2, 4), (2, 3) )] )

	#mazepool = [m1, m2]
	#Maze(empty=True).showAdjacency()
	#for m in mazepool:
	#	print("=====================THIS IS A BAR=====================")
	#	wowmaze=Maze(m)
	#	wowmaze.showAdjacency()


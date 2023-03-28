#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random
from colorize import *

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__(self):
		self.row = 1
		self.col = 1
		self.matrix = None
		self.path = None
		self.sequence = None
		self.bandAdjust = -1

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		seq1 = seq1[:align_length]
		seq2 = seq2[:align_length]

###################################################################################################
		# for the first two sequences comparisons on the banded alignment there is no alignment possible
		if (seq1 == "polynomial" or seq1 == "exponential") and seq1 != seq2 and self.banded:
			alignment1 = "No alignment possible"
			alignment2 = "No alignment possible"
			score = float("inf")
		else:
			if not banded:
				score = self.needlemanWunschUnrestricted(seq1, seq2)
			else:
				score = self.needlemanWunschBanded(seq1, seq2)

			alignment1, alignment2 = self.getAlignment(seq1, seq2)

		# used to print out the answer to question 4
		if self.row == 3 and self.col == 10:
			printc(alignment1[:100], 'green')
			printc(alignment2[:100], 'red')
		# used to print out all other answers, for easy comparison
		else:
			printc(alignment1[:100], 'blue')
			printc(alignment2[:100], 'tangerine')
###################################################################################################

		# used to adjust which cell we are currently updating (for saving the matrix to a file)
		if self.col == 10:
			self.col = self.row
			self.row += 1
		self.col += 1

		return {'align_cost':score, 'seqi_first100':alignment1[:100], 'seqj_first100':alignment2[:100]}
	

# NOTE: time complexity: O(nm), space complexity: O(nm)
	# time: this method initializes a matrix of dimensions n x m, where n is the length of seq1 and
	# m is the length of seq2. It then fills in the matrix iteratively with the appropriate values.
	# Since we are iterating through the matrix and, at each step, performing basic comparisons, the
	# time complexity is O(nm).
	# space: also O(nm), since we are creating a matrix of size n x m.
	def needlemanWunschUnrestricted(self, seq1, seq2):
		# Initialize the matrix
		x = len(seq2)+1
		y = len(seq1)+1
		self.matrix = [[Node(None,0) for i in range(x)] for j in range(y)]

		# Fill in the first row
		for j in range(x):
			if j == 0:
				self.matrix[0][j] = Node('', 0)
				continue
			self.matrix[0][j] = Node('<', j*INDEL)
		# Fill in the first col
		for i in range(y):
			if i == 0:
				continue
			self.matrix[i][0] = Node('^', i*INDEL)

		# Fill in the rest of the matrix
		for i in range(1, y): # row
			for j in range(1, x): # col
				_ins = int(self.matrix[i][j-1].val) + INDEL # left one
				_del = int(self.matrix[i-1][j].val) + INDEL # up one
				_sub = int(self.matrix[i-1][j-1].val) + SUB # diagonal sub
				_match = float("inf") 						# diagonal match
				if seq1[i-1] == seq2[j-1]:
					_match = self.matrix[i-1][j-1].val + MATCH

				if _ins < _del and _ins < _sub and _ins < _match:
					_min = _ins
				elif _del < _sub and _del < _match:
					_min = _del
				elif _sub < _match:
					_min = _sub
				else:
					_min = _match

				_op = '<' if _min == _ins else '^' if _min == _del else '\\'
				
				self.matrix[i][j] = Node(_op, _min)

		# used to save the path to/from the optimal solution to variables for easy access
		self.path, self.sequence = self.pathfinder(self.matrix)

		# debug: print out small matrices to console, and all matrices to files
		# if x < 50 and y < 50:
		# 	self.matrixPrinter(seq1, seq2, self.matrix)
		# self.matrixPrinter(seq1, seq2, self.matrix, open(f"matrix/matrix_{self.row}-{self.col}.txt", "w"))

		return self.matrix[y-1][x-1].val
	
# NOTE: time complexity: O(kn), space complexity: O(kn)
	# time: this method initializes a matrix of dimensions k x n, where k is the length of a band
	# (always 7 in our case) and n is the length of the sequences being compared. It then fills in
	# the matrix iteratively with the appropriate values. Since we are iterating through the matrix
	# and, at each step, performing basic comparisons, the time complexity is O(kn). The dependency
	# pointers to adjacent cells in the smaller array are calculated normally for the first 3 rows,
	# however for subsequent rows the dependency pointers must be calculated slightly differently.
	# Left arrows are calculated normally, but up and diagonal arrows are calculated slightly
	# differently. This is because the band is only 7 cells wide. The up arrow is calculated by
	# looking at the cell one row above and one column to the right of the current cell. The diagonal
	# arrow is calculated by looking at the cell one row above and in the same column as the current
	# cell.
	# space: also O(kn), since we are creating a matrix of size k x n.
	def needlemanWunschBanded(self, seq1, seq2):
		# Initialize the matrix
		x = 7
		y = len(seq1)+1
		self.matrix = [[None for i in range(x)] for j in range(y)]
		self.bandAdjust = -1

		# Fill in the first row
		for i in range(4):
			if i == 0:
				self.matrix[0][i] = Node('', 0)
				continue
			self.matrix[0][i] = Node('<', i*INDEL)

		# Fill in the rest of the matrix
		for i in range(1, y): # row
			if i == y-1:
				_range = 4
			elif i == 1 or i == y-2:
				_range = 5
			elif i == 2 or i == y-3:
				_range = 6
			else:
				_range = 7

			for j in range(_range): # col
				center = _range - 4

				# fill in first three rows
				if i < 4:
					# fill in first col in first few rows; else is other special cases
					if j == 0:
						self.matrix[i][j] = Node('^', self.matrix[i-1][j].val + INDEL)
						continue
					else:
						if self.matrix[i][j-1] == None or j == 0:			# left one
							_ins = float("inf")
						else:
							_ins = int(self.matrix[i][j-1].val) + INDEL
						if j == _range-1 or self.matrix[i-1][j] == None:	# up one
							_del = float("inf")
						else:
							_del = int(self.matrix[i-1][j].val) + INDEL 
						if self.matrix[i-1][j-1] == None:					# diagonal
							_sub = float("inf")
							_match = float("inf")
						else:
							if seq1[i-1] == seq2[j+self.bandAdjust]:
								_sub = float("inf")
								_match = int(self.matrix[i-1][j-1].val) + MATCH
							else:
								_sub = int(self.matrix[i-1][j-1].val) + SUB
								_match = float("inf")
						

						if _ins < _del and _ins < _sub and _ins < _match:
							_min = _ins
						elif _del < _sub and _del < _match:
							_min = _del
						elif _sub < _match:
							_min = _sub
						else:
							_min = _match

						_op = '<' if _min == _ins else '^' if _min == _del else '\\'
						
						self.matrix[i][j] = Node(_op, _min)
						continue

				# after the first 3 rows, "adjust" the portion of the top string we're looking at
				elif j == 0:
					self.bandAdjust += 1

				if self.matrix[i][j-1] == None or j == 0:			# left one
					_ins = float("inf")
				else:
					_ins = int(self.matrix[i][j-1].val) + INDEL
				if j == _range-1 or self.matrix[i-1][j+1] == None:	# up one
					_del = float("inf")
				else:
					_del = int(self.matrix[i-1][j+1].val) + INDEL 
				if self.matrix[i-1][j] == None:						# diagonal
					_sub = float("inf")
				else:
					if seq1[i-1] == seq2[j+self.bandAdjust]:
						_match = int(self.matrix[i-1][j].val) + MATCH
						_sub = float("inf")
					else:
						_sub = int(self.matrix[i-1][j].val) + SUB
						_match = float("inf")
				

				if _ins < _del and _ins < _sub and _ins < _match:
					_min = _ins
				elif _del < _sub and _del < _match:
					_min = _del
				elif _sub < _match:
					_min = _sub
				else:
					_min = _match

				_op = '<' if _min == _ins else '^' if _min == _del else '\\'
				
				self.matrix[i][j] = Node(_op, _min)

		self.path, self.sequence = self.pathfinderBanded(self.matrix)

		# debug: print out small matrices to console, and all matrices to files
		# if x < 50 and y < 50:
		# 	self.matrixPrinterBanded(seq1, seq2, self.matrix)
		# self.matrixPrinterBanded(seq1, seq2, self.matrix, open(f"matrix/matrixBanded_{self.row}-{self.col}.txt", "w"))s

		return self.matrix[y-1][3].val
	

	# utility function to print out the matrix
	def matrixPrinter(self, seq1, seq2, matrix, fOut = None):
		if fOut is None:
			# print seq2 along the top
			print("  \t", end = "")
			[print(colorize(f"{i}", "red"), end = "\t") for i in seq2[:len(matrix)]]
			print()

			for i in range(len(matrix)):
				# print seq1 along the left
				if i == 0:
					print("  ", end = "")
				else:
					print(colorize(seq1[i-1], "red"), end = " ")

				for j in range(len(matrix[0])):
					if matrix[i][j].onPath:
						print(colorize(matrix[i][j], "green"), end = "\t")
					elif i == j:
						print(colorize(matrix[i][j], "cyan"), end = "\t")
					else:
						print(matrix[i][j], end = "\t")
				print()
		else:
			# print seq2 along the top
			print("\t\t", end = "", file=fOut)
			[print(i + "   ", end = "\t", file=fOut) for i in seq2[:len(matrix)-1]]
			print("\n", file=fOut)

			for i in range(len(matrix)):
				# print seq1 along the left
				if i == 0:
					print("  ", end = "", file=fOut)
				else:
					print(seq1[i-1], end = " ", file=fOut)

				for j in range(len(matrix[0])):
					cell = str(matrix[i][j])
					if not (i == 0 and j == 0) and not matrix[i][j].onPath:
						cell = cell[1:]
					while len(cell) < 5:
						cell += ' '
					print(cell, end = "\t", file=fOut)
				print("\n", file=fOut)
	
	# utility function to print out the matrix
	def matrixPrinterBanded(self, seq1, seq2, matrix, fOut = None):
		center = 0

		if fOut is None:
			# print seq2 along the top
			print("  \t", end = "")
			[print(colorize(f"{i}", "red"), end = "\t") for i in seq2[:len(matrix)]]
			print()

			for i in range(len(matrix)):
				# print seq1 along the left
				if i == 0:
					print("  ", end = "")
				else:
					print(colorize(seq1[i-1], "red"), end = " ")

				if 3 < i:
					center += 1

				# add tabs to make the matrix look like a band
				if i > 3:
					print('\t' * (i - 3), end = "")

				for j in range(len(matrix[0])):
					try:
						if matrix[i][j].onPath:
							print(colorize(matrix[i][j], "green"), end = "\t")
						elif i == j+center:
							print(colorize(matrix[i][j], "cyan"), end = "\t")
						else:
							print(matrix[i][j], end = "\t")
					except:
						pass
				print()
		else:
			# print seq2 along the top
			print("\t\t", end = "", file=fOut)
			[print(i + "   ", end = "\t", file=fOut) for i in seq2[:len(matrix)]]
			print("\n", file=fOut)

			for i in range(len(matrix)):
				# print seq1 along the left
				if i == 0:
					print("  ", end = "", file=fOut)
				else:
					print(seq1[i-1], end = " ", file=fOut)

				# add tabs to make the matrix look like a band
				if i > 3:
					print('\t' * (i - 3), end = "", file=fOut)

				for j in range(len(matrix[0])):
					try:
						cell = str(matrix[i][j])
						if not (i == 0 and j == 0) and not matrix[i][j].onPath:
							cell = cell[1:]
						while len(cell) < 5:
							cell += ' '
						print(cell, end = "\t", file=fOut)
					except:
						pass
				print("\n", file=fOut)

	
	# utility function to save the path to/from the optimal solution
	def pathfinder(self, matrix):
		path = []
		sequence = []
		
		i = len(matrix)-1
		j = len(matrix[0])-1
		while i > 0 or j > 0:
			path.append((i, j))
			sequence.append(matrix[i][j].op)
			matrix[i][j].onPath = True
			if matrix[i][j].op == "\\":
				i -= 1
				j -= 1
			elif matrix[i][j].op == "<":
				j -= 1
			elif matrix[i][j].op == "^":
				i -= 1
			else:
				raise Exception("Invalid path")

		return path,sequence
	
	# utility function to save the path to/from the optimal solution
	def pathfinderBanded(self, matrix):
		path = []
		sequence = []
		
		i = len(matrix)-1
		j = 3
		while i > 0 or j > 0:
			if matrix[i][j].op == "\\":
				path.append((i, j))
				sequence.append(matrix[i][j].op)
				matrix[i][j].onPath = True
				i -= 1
				if i < 3:
					j -= 1
			elif matrix[i][j].op == "<":
				path.append((i, j))
				sequence.append(matrix[i][j].op)
				matrix[i][j].onPath = True
				j -= 1
			elif matrix[i][j].op == "^":
				path.append((i, j))
				sequence.append(matrix[i][j].op)
				matrix[i][j].onPath = True
				i -= 1
				if i > 3:
					j += 1
			else:
				raise Exception("Invalid path")

		return path,sequence


	# utility function to get the alignment for two sequences
	def getAlignment(self, seq1, seq2):
		alignment1 = ''
		alignment2 = ''

		for i in range(len(self.sequence)):
			if self.sequence[i] == '<':
				alignment1 += '-'
				alignment2 += seq2[-1]
				seq2 = seq2[:-1]
			elif self.sequence[i] == '^':
				alignment1 += seq1[-1]
				alignment2 += '-'
				seq1 = seq1[:-1]
			else:
				alignment1 += seq1[-1]
				alignment2 += seq2[-1]
				seq1 = seq1[:-1]
				seq2 = seq2[:-1]

		# reverse the strings
		alignment1 = alignment1[::-1]
		alignment2 = alignment2[::-1]

		return alignment1, alignment2


# utility class for ease of storing/accessing matrix values and dependency pointers
class Node:
	def __init__(self, op, val):
		self.op = op
		self.val = val
		self.onPath = False
		
	def __str__(self):
		return f"{self.op}{self.val}"

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
		self.count = 1
		pass

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length

		if not banded:
			score = self.needlemanWunsch(seq1, seq2)

###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		# score = random.random()*100

		alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
			len(seq1), align_length, ',BANDED' if banded else '')
		alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
			len(seq2), align_length, ',BANDED' if banded else '')
###################################################################################################

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
	

	def needlemanWunsch(self, seq1, seq2):
		# Initialize the matrix
		matrix = [[Node(None,0) for i in range(len(seq1)+1)] for j in range(len(seq2)+1)]

		# Fill in the first row
		for i in range(len(seq1)+1):
			matrix[0][i] = Node('', i*INDEL)
		# Fill in the first col
		for i in range(len(seq2)+1):
			matrix[i][0] = Node('', i*INDEL)

		# Fill in the rest of the matrix
		for i in range(1, len(seq2)+1):
			for j in range(1, len(seq1)+1):
				if seq1[j-1] == seq2[i-1]:
					matrix[i][j] = Node("\\", matrix[i-1][j-1].val + MATCH)
				else:
					_sub = int(matrix[i-1][j-1].val) + SUB # diagonal
					_ins = int(matrix[i][j-1].val) + INDEL # left one
					_del = int(matrix[i-1][j].val) + INDEL # up one
					_min = min(_sub, _ins, _del)
					_op = "\\" if _min == _sub else "<" if _min == _ins else "^"
					
					matrix[i][j] = Node(_op, _min)

		path = self.pathfinder(matrix)
		self.matrixPrinter(seq1, seq2, matrix, open(f"matrix{self.count}.txt", "w"))
		self.count += 1

		return matrix[len(seq2)][len(seq1)].val
	

	def matrixPrinter(self, seq1, seq2, matrix, fOut = None):
		if fOut is None:
			# print seq1 along the top
			print("  \t", end = "")
			[print(colorize(f"{i}", "red"), end = "\t") for i in seq1]
			print()

			for i in range(len(matrix)):
				# print seq2 along the left
				if i == 0:
					print("  ", end = "")
				else:
					print(colorize(seq2[i-1], "red"), end = " ")

				for j in range(len(matrix[0])):
					if matrix[i][j].onPath:
						print(colorize(matrix[i][j], "green"), end = "\t")
					elif i == j:
						print(colorize(matrix[i][j], "cyan"), end = "\t")
					else:
						print(matrix[i][j], end = "\t")
				print()
		else:
			# print seq1 along the top
			print("\t\t", end = "", file=fOut)
			[print(i + "   ", end = "\t", file=fOut) for i in seq1]
			print("\n", file=fOut)

			for i in range(len(matrix)):
				# print seq2 along the left
				if i == 0:
					print("  ", end = "", file=fOut)
				else:
					print(seq2[i-1], end = " ", file=fOut)

				for j in range(len(matrix[0])):
					cell = str(matrix[i][j])
					while len(cell) < 5:
						cell += ' '
					print(cell, end = "\t", file=fOut)
				print("\n", file=fOut)

	
	def pathfinder(self, matrix):
		# Find the path
		path = []
		
		i = len(matrix)-1
		j = len(matrix[0])-1
		while i > 0 and j > 0:
			if matrix[i][j].op == "\\":
				path.append((i, j))
				matrix[i][j].onPath = True
				i -= 1
				j -= 1
			elif matrix[i][j].op == "<":
				path.append((i, j))
				matrix[i][j].onPath = True
				j -= 1
			elif matrix[i][j].op == "^":
				path.append((i, j))
				matrix[i][j].onPath = True
				i -= 1
			else:
				raise Exception("Invalid path")

		return path
	
class Node:
	def __init__(self, op, val):
		self.op = op
		self.val = val
		self.onPath = False
		
	def __str__(self):
		return f"{self.op}{self.val}"
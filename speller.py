#!/usr/bin/env python

import sys

class Node:
	val = left = right = None

	def __init__(self, val=None, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

	def safe_left(self):
		if not self.left: self.left = Node()
		return self.left

	def safe_right(self):
		if not self.right: self.right = Node()
		return self.right

	def __str__(self):
		return '(%s %s %s)' % (self.val, self.left, self.right)

class WordTree:
	MAX_ERRORS = 2

	root = Node()

	def __str__(self): return str(self.root)

	def add_word(self, word, node=root):
		if not word: return

		if not node.val:
			node.val = word[0]
			self.add_word(word[1:], node.safe_left())
		else:
			if node.val == word[0]:
				if node.safe_left().val is None:
					self.add_word(word[1:], node.left.safe_right())
				else:
					self.add_word(word[1:], node.left)
			else:
				self.add_word(word, node.safe_right())

	def correct(self, word, node=root, path=[], revised=[], output=None):
		is_top = output is None
		if is_top: output = []

		if not node or len(path) > WordTree.MAX_ERRORS: return

		if not word and not node.val:
			output.append([''.join(revised), path[:]])
			return

		if word and word[0] == node.val:
			revised.append(word[0])
			self.correct(word[1:], node.left, path, revised, output)
			revised.pop()
		else:
			if word and node.val:
				path.append(['s', node.val, word[0]])
				revised.append(node.val)
				self.correct(word[1:], node.left, path, revised, output)
				revised.pop()
				path.pop()

			if node.val:
				path.append(['d', node.val])
				revised.append(node.val)
				self.correct(word, node.left, path, revised, output)
				revised.pop()
				path.pop()

			if word:
				path.append(['i', word[0]])
				self.correct(word[1:], node, path, revised, output)
				path.pop()

		self.correct(word, node.right, path, revised, output)

		if len(word) > 1 and word[1] == node.val:
			cur_node = node.left
			while cur_node:
				if cur_node.val == word[0]: break
				cur_node = cur_node.right

			if cur_node:
				path.append(['t', word[1], word[0]])
				revised.append(word[1])
				revised.append(word[0])
				self.correct(word[2:], cur_node.safe_left(), path, revised, output)
				revised.pop()
				revised.pop()
				path.pop()

		if is_top:
			tmp = {}
			for x in output: tmp[repr(x[1])] = x
			output = tmp.values()
			output.sort(key=lambda x: len(x[1]))
			return output

def readable_path(path):
	output = []

	for row in path:
		if row[0] == 's': output.append('substitution error %s -> %s' % (row[1], row[2]))
		elif row[0] == 'd': output.append('deletion error %s' % row[1])
		elif row[0] == 'i': output.append('insertion error %s' % row[1])
		elif row[0] == 't': output.append('transposition error %s <-> %s' % (row[1], row[2]))
		else: output.append(repr(row))

	return '%d error(s): %s' % (len(path), ', '.join(output))

def check_word(word, word_tree):
	print '%s ->' % word
	output = word_tree.correct(word)
	for row in output:
		print '%s: %s' % (row[0], readable_path(row[1]))
	print '-'*4

if __name__ == '__main__':
	word_tree = WordTree()

	if len(sys.argv) > 1 and sys.argv[1] == '-a':
		for word in ['ant', 'cat', 'colt', 'cow', 'pet', 'pig', 'pigs', 'pony']:
			word_tree.add_word(word)

		print word_tree
		print '-'*4

		for word in ['amt', 'caat', 'pigss', 'dow', 'pnoy', 'clt']:
			check_word(word, word_tree)

	else:
		for line in open('words.txt'):
			word_tree.add_word(line[:-1])

		print '* Word tree created.'

		while True:
			check_word(raw_input(), word_tree)

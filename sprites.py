import pygame as pg
from ajustes import *

class Tablero():
	board = [[0 for i in range(0,8)] for j in range(0,8)]
	board[3][3] = 1
	board[4][4] = 1
	board[3][4] = 2
	board[4][3] = 2
	size = 0
	height = 0
	width = 0
	offset_x = 0
	offset_y = 0
	game = None
	f_blanca = None
	f_negra = None


	def __init__(self,game,width,height,offset_x,offset_y):
		self.size = 8
		self.width = width
		self.height = height
		self.offset_x = offset_x
		self.offset_y = offset_y
		self.game = game
		self.f_blanca = pg.transform.scale(game.f_blanca,(int(width/8 * 0.8),int(height/8 * 0.8)))
		self.f_negra = pg.transform.scale(game.f_negra,(int(width/8 * 0.8),int(height/8 * 0.8)))

	def ubicacion_click(self,click_pos):
		segment_size = self.width / self.size

		x = (click_pos[1] - self.offset_y)//segment_size
		y = (click_pos[0] - self.offset_x)//segment_size

		return int(x),int(y)

	def hay_jugadas(self):
		result = False
		for x in range(0,self.size):
			for y in range(0,self.size):
				result = result or self.board[x][y] == 0

		return result

	def jugada_en_tablero(self,x,y):
		return (x >= 0 and y >= 0 and x < 8 and y < 8 and self.board[x][y] == 0)

	def jugada_valida(self,x,y):
		if x>0 and y>0:
			if x<(self.size-1) and y<(self.size-1):
				alrededor = [
					self.board[y][x+1],
					self.board[y+1][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
			elif x==(self.size-1) and y<(self.size-1):
				alrededor = [
					self.board[y-1][x],
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
			elif x<(self.size-1) and y==(self.size-1):
				alrededor = [
					self.board[y][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
			elif x==(self.size-1) and y==(self.size-1):
				alrededor = [
					self.board[y-1][x],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
		elif x==0 and y>0:
			if y<(self.size-1):
				alrededor = [
					self.board[y][x+1],
					self.board[y+1][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
					self.board[y+1][x],
				]
			elif y==(self.size-1):
				alrededor = [
					self.board[y][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
				]
		elif x>0 and y==0:
			if x<(self.size-1):
				alrededor = [
					self.board[y][x+1],
					self.board[y+1][x+1],
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
				]
			elif x==(self.size-1):
				alrededor = [
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
				]

		elif x==0 and y==0:
			alrededor = [
				self.board[y][x+1],
				self.board[y+1][x+1],
				self.board[y+1][x],
				]

		return self.jugada_en_tablero(x,y) and any(i!=0 for i in alrededor)

	def render_board(self):
		segment_size = self.width / self.size

		# dibujando las lineas
		for x in range(0,self.size+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x + segment_size * x,self.offset_y),
			(self.offset_x + segment_size * x,self.offset_y + self.height),5)
		for y in range(0,self.size+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x,self.offset_y + segment_size * y),
			(self.offset_x + self.width,self.offset_y + segment_size * y),5)

		# dibujando las fichas
		for x in range(0,self.size):
			for y in range(0,self.size):
				if self.board[x][y] == 1:
					self.game.screen.blit(self.game.f_blanca,
							(
								self.offset_x + segment_size * y + int(self.width/self.size * 0.1),
								self.offset_y + segment_size * x + int(self.height/self.size * 0.1)
							)
						)
				if self.board[x][y] == 2:
					self.game.screen.blit(self.game.f_negra,
							(
								self.offset_x + segment_size * y + int((self.width/self.size) * 0.1),
								self.offset_y + segment_size * x + int(self.height/self.size * 0.1)
							)
						)

	def jugada(self,x_pos,y_pos,jugador):
		if self.board[x_pos][y_pos] == 0:
			self.board[x_pos][y_pos] = jugador.index

class Jugador():
	puntos = 2
	index = 0

	def __init__(self,game,index):
		self.index = index
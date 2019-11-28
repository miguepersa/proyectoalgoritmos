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
	fichas_restantes = 60

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
		segment_size = self.width / 8

		x = (click_pos[1] - self.offset_y)//segment_size
		y = (click_pos[0] - self.offset_x)//segment_size

		return int(x),int(y)

	def hay_jugadas(self):
		result = False
		for x in range(0,8):
			for y in range(0,8):
				result = result or self.board[x][y] == 0

		return result

	def jugada_en_tablero(self,x,y):
		return (x >= 0 and y >= 0 and x < 8 and y < 8 and self.board[x][y] == 0)

	def jugada_valida(self,x,y,turno):
		if x>0 and y>0:
			if x<7 and y<7:
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
			elif x==7 and y<7:
				alrededor = [
					self.board[y-1][x],
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
			elif x<7 and y==7:
				alrededor = [
					self.board[y][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
			elif x==7 and y==7:
				alrededor = [
					self.board[y-1][x],
					self.board[y][x-1],
					self.board[y-1][x-1]
				]
		elif x==0 and y>0:
			if y<7:
				alrededor = [
					self.board[y][x+1],
					self.board[y+1][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
					self.board[y+1][x],
				]
			elif y==7:
				alrededor = [
					self.board[y][x+1],
					self.board[y-1][x+1],
					self.board[y-1][x],
				]
		elif x>0 and y==0:
			if x<7:
				alrededor = [
					self.board[y][x+1],
					self.board[y+1][x+1],
					self.board[y+1][x],
					self.board[y+1][x-1],
					self.board[y][x-1],
				]
			elif x==7:
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
		if turno == 1:
			otroturno=2
		if turno == 2:
			otroturno = 1
		return self.jugada_en_tablero(x,y) and any(i!=0 for i in alrededor) and any(i==otroturno for i in alrededor)

	def render_board(self):
		segment_size = self.width / 8

		# dibujando las lineas
		for x in range(0,8+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x + segment_size * x,self.offset_y),
			(self.offset_x + segment_size * x,self.offset_y + self.height),5)
		for y in range(0,8+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x,self.offset_y + segment_size * y),
			(self.offset_x + self.width,self.offset_y + segment_size * y),5)

		# dibujando las fichas
		for x in range(0,8):
			for y in range(0,8):
				if self.board[x][y] == 1:
					self.game.screen.blit(self.game.f_blanca,
							(
								self.offset_x + segment_size * y + int(self.width/8 * 0.1),
								self.offset_y + segment_size * x + int(self.height/8 * 0.1)
							)
						)
				if self.board[x][y] == 2:
					self.game.screen.blit(self.game.f_negra,
							(
								self.offset_x + segment_size * y + int((self.width/8) * 0.1),
								self.offset_y + segment_size * x + int(self.height/8 * 0.1)
							)
						)

	def jugada(self,x_pos,y_pos,jugador):
		if self.board[x_pos][y_pos] == 0:
			self.board[x_pos][y_pos] = jugador.index


	# metodo que chequea lineas verticales
	def check_horizon(self,ficha,xinicio,yinicio):
		otraficha = 0
		ycambio = 1
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif ficha == 2:
			otraficha = 1
		if self.board[xinicio][yinicio+1] == otraficha:
			while ycambio+yinicio<7 and self.board[xinicio][ycambio+yinicio] == otraficha:
				fichasCambio.append([xinicio,ycambio+yinicio])
				ycambio += 1
			if self.board[xinicio][yinicio+ycambio] == ficha:
				for i,j in fichasCambio:
					self.board[i][j] = ficha
		if self.board[xinicio][yinicio-1] == otraficha:
			ycambio = -1
			while ycambio+yinicio>0 and self.board[xinicio][ycambio+yinicio] == otraficha:
				fichasCambio.append([xinicio,ycambio+yinicio])
				ycambio -= 1
			if self.board[xinicio][yinicio+ycambio] == ficha:
				for i,j in fichasCambio:
					self.board[i][j] = ficha


	# metodo que chequea lineas horizontales
	def check_vertical(self,ficha,xinicio,yinicio):
		otraficha = 0
		xcambio = 1
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif ficha == 2:
			otraficha = 1
		if self.board[xinicio+1][yinicio] == otraficha:
			while xcambio+xinicio<7 and self.board[xinicio+xcambio][yinicio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio])
				xcambio += 1
			if self.board[xinicio+xcambio][yinicio] == ficha:
				for i,j in fichasCambio:
					self.board[i][j] = ficha		
		if self.board[xinicio-1][yinicio] == otraficha:
			xcambio = -1
			while xcambio+xinicio>0 and self.board[xinicio+xcambio][yinicio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio])
				xcambio -= 1
			if self.board[xinicio+xcambio][yinicio] == ficha:
				for i,j in fichasCambio:
					self.board[i][j] = ficha

	# metodo que chequea lineas diagonales
	def check_diagonal(self,ficha,xinicio,yinicio):
		otraficha = 0
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif otraficha == 2:
			otraficha = 1
		ycambio = 1
		xcambio = 1
		if self.board[xinicio+1][yinicio+1] == otraficha:
			while xcambio+xinicio<7 and ycambio+yinicio<7 and self.board[xinicio+xcambio][yinicio+ycambio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio+ycambio])
				xcambio += 1
				ycambio += 1
			if self.board[xinicio+xcambio][yinicio+ycambio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha
		if self.board[xinicio-1][yinicio-1] == otraficha:
			xcambio = -1
			ycambio = -1
			while xcambio+xinicio>0 and ycambio+yinicio>0 and self.board[xinicio+xcambio][yinicio+ycambio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio+ycambio])
				xcambio -= 1
				ycambio -= 1
			if self.board[xinicio+xcambio][yinicio+ycambio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha

		if self.board[xinicio+1][yinicio-1] == otraficha:
			xcambio = 1
			ycambio = -1
			while xcambio+xinicio<7 and ycambio+yinicio>0 and self.board[xinicio+xcambio][yinicio+ycambio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio+ycambio])
				xcambio += 1
				ycambio -= 1
			if self.board[xinicio+xcambio][yinicio+ycambio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha

		if self.board[xinicio-1][yinicio+1] == otraficha:
			xcambio = -1
			ycambio = 1
			while xcambio+xinicio>0 and ycambio+yinicio<7 and self.board[xinicio+xcambio][yinicio+ycambio] == otraficha:
				fichasCambio.append([xinicio+xcambio,yinicio+ycambio])
				xcambio -= 1
				ycambio += 1
			if self.board[xinicio+xcambio][yinicio+ycambio] == ficha:
				for i,j in fichasCambio:
					self.board[i][j] = ficha


	def voltearFichas(self,xinicio,yinicio,ficha):
		self.check_vertical(ficha,xinicio,yinicio)
		self.check_horizon(ficha,xinicio,yinicio)
		self.check_diagonal(ficha,xinicio,yinicio)



	# def voltearFichas(self,xinicio,yinicio,ficha):
	# 	direcciones = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
	# 	fichasAVoltear = []
	# 	direccionesCambio = []
	# 	xcambio = 0
	# 	ycambio = 0
	# 	if ficha == 1:
	# 		otraficha = 2
	# 	if ficha == 2:
	# 		otraficha = 1
	# 	for x,y in direcciones:
	# 		indexx = xinicio + x
	# 		indexy = yinicio + y
	# 		if self.jugada_en_tablero(indexx,indexy):
	# 			if self.board[indexx][indexy] == otraficha:
	# 				print(str(indexx) + " " + str(indexy))
	# 				direccionesCambio.append([x,y])
	# 				print(direccionesCambio)
	# 	print(direccionesCambio)
	# 	for i,j in direccionesCambio:
	# 		xcambio = xinicio+i
	# 		ycambio = yinicio+j
	# 		while self.jugada_en_tablero(xcambio,ycambio) and self.board[xcambio][ycambio] == otraficha:
	# 			fichasAVoltear.append([xcambio,ycambio])
	# 			xcambio += i
	# 			ycambio += j
	# 	print(fichasAVoltear)
	# 	# print(str(xcambio) + " " + str(ycambio))
	# 	if self.board[xcambio][ycambio] == ficha:
	# 		for i,j in fichasAVoltear:
	# 			self.board[i][j] = ficha
	# 	else:
	# 		pass


class Jugador():
	puntos = 2
	index = 0
	nombre = ""

	def __init__(self,index):
		self.index = index
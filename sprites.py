import pygame as pg
from ajustes import *

class Tablero():
	# Inicialización de variables
	board = [] # Arreglo que representa el tablero del juego
	height = 0
	width = 0
	offset_x = 0
	offset_y = 0
	game = None
	f_blanca = None
	f_negra = None
	fichas_restantes = 60

	def __init__(self,game,width,height,offset_x,offset_y):
		'''
		Función constructora de la clase del tablero.
		'''
		self.size = 8
		self.width = width
		self.height = height
		self.offset_x = offset_x
		self.offset_y = offset_y
		self.game = game
		self.f_blanca = pg.transform.scale(game.f_blanca,(int(width/8 * 0.8),int(height/8 * 0.8)))
		self.f_negra = pg.transform.scale(game.f_negra,(int(width/8 * 0.8),int(height/8 * 0.8)))
		self.board = [[0 for i in range(0,8)] for j in range(0,8)] # Arreglo que representa el tablero del juego
		self.board[3][3] = 1		#
		self.board[4][4] = 1		# Fichas iniciales del juego
		self.board[3][4] = 2		#
		self.board[4][3] = 2		#


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
		'''
		Verifica que la jugada que se hizo,
		esté dentro del tablero
		'''
		return (x >= 0 and y >= 0 and x < 8 and y < 8 and self.board[x][y] == 0)

	def jugada_valida(self,x,y,turno):
		'''
		Funcion que revisa que hayan fichas del otro 
		jugador en los alrededores de la jugada hecha.
		El arreglo 'alrededor' contiene la información
		de las casillas que estan en los alrededores
		de la ultima jugada.
		'''
		if y>0 and x>0:
			if y<7 and x<7:
				alrededor = [
					self.board[x][y+1],
					self.board[x+1][y+1],
					self.board[x-1][y+1],
					self.board[x-1][y],
					self.board[x+1][y],
					self.board[x+1][y-1],
					self.board[x][y-1],
					self.board[x-1][y-1]
				]
			elif y==7 and x<7:
				alrededor = [
					self.board[x-1][y],
					self.board[x+1][y],
					self.board[x+1][y-1],
					self.board[x][y-1],
					self.board[x-1][y-1]
				]
			elif y<7 and x==7:
				alrededor = [
					self.board[x][y+1],
					self.board[x-1][y+1],
					self.board[x-1][y],
					self.board[x][y-1],
					self.board[x-1][y-1]
				]
			elif y==7 and x==7:
				alrededor = [
					self.board[x-1][y],
					self.board[x][y-1],
					self.board[x-1][y-1]
				]
		elif y==0 and x>0:
			if x<7:
				alrededor = [
					self.board[x][y+1],
					self.board[x+1][y+1],
					self.board[x-1][y+1],
					self.board[x-1][y],
					self.board[x+1][y],
				]
			elif x==7:
				alrededor = [
					self.board[x][y+1],
					self.board[x-1][y+1],
					self.board[x-1][y],
				]
		elif y>0 and x==0:
			if y<7:
				alrededor = [
					self.board[x][y+1],
					self.board[x+1][y+1],
					self.board[x+1][y],
					self.board[x+1][y-1],
					self.board[x][y-1],
				]
			elif y==7:
				alrededor = [
					self.board[x+1][y],
					self.board[x+1][y-1],
					self.board[x][y-1],
				]

		elif y==0 and x==0:
			alrededor = [
				self.board[x][y+1],
				self.board[x+1][y+1],
				self.board[x+1][y],
				]
		if turno == 1:
			otroturno=2
		if turno == 2:
			otroturno = 1
		return self.jugada_en_tablero(x,y) and any(i!=0 for i in alrededor) and any(i==otroturno for i in alrededor)

	def render_board(self):
		segment_size = self.width / 8

		# Dibujo de las lineas del tablero
		for x in range(0,8+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x + segment_size * x,self.offset_y),
			(self.offset_x + segment_size * x,self.offset_y + self.height),5)
		for y in range(0,8+1):
			pg.draw.line(self.game.screen,BLACK,(self.offset_x,self.offset_y + segment_size * y),
			(self.offset_x + self.width,self.offset_y + segment_size * y),5)

		# Dibujo de las fichas en el tablero
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
	def consumoHorizontal(self,ficha,xinicio,yinicio):
		'''
		Funcion que revisa las lineas horizontales desde la posicion
		de la jugada hecha para voltear las fichas del
		otro jugador si es necesario.
		'''
		# Inicializacion de variables:
		otraficha = 0
		ycambio = 1
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif ficha == 2:
			otraficha = 1
		if yinicio+1<=7:	
			if self.board[xinicio][yinicio+1] == otraficha:
				while ycambio+yinicio<7 and self.board[xinicio][ycambio+yinicio] == otraficha:
					fichasCambio.append([xinicio,ycambio+yinicio])
					ycambio += 1
				if self.board[xinicio][yinicio+ycambio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha
		if yinicio-1>=0:				
			if self.board[xinicio][yinicio-1] == otraficha:
				ycambio = -1
				while ycambio+yinicio>0 and self.board[xinicio][ycambio+yinicio] == otraficha:
					fichasCambio.append([xinicio,ycambio+yinicio])
					ycambio -= 1
				if self.board[xinicio][yinicio+ycambio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha


	# metodo que chequea lineas horizontales
	def consumoVertical(self,ficha,xinicio,yinicio):
		'''
		Funcion que revisa las lineas verticales desde la posicion
		de la jugada hecha para voltear las fichas del
		otro jugador si es necesario.
		'''
		# Inicializacion de variables:
		otraficha = 0
		xcambio = 1
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif ficha == 2:
			otraficha = 1
		if xinicio+1<=7:	
			if self.board[xinicio+1][yinicio] == otraficha:
				while xcambio+xinicio<7 and self.board[xinicio+xcambio][yinicio] == otraficha:
					fichasCambio.append([xinicio+xcambio,yinicio])
					xcambio += 1
				if self.board[xinicio+xcambio][yinicio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha		
		if xinicio-1>=0:
			if self.board[xinicio-1][yinicio] == otraficha:
				xcambio = -1
				while xcambio+xinicio>0 and self.board[xinicio+xcambio][yinicio] == otraficha:
					fichasCambio.append([xinicio+xcambio,yinicio])
					xcambio -= 1
				if self.board[xinicio+xcambio][yinicio] == ficha:
					for i,j in fichasCambio:
						self.board[i][j] = ficha

	# metodo que chequea lineas diagonales
	def consumoDiagonal(self,ficha,xinicio,yinicio):
		'''
		Funcion que revisa las diagonales desde la posicion
		de la jugada hecha para voltear las fichas del
		otro jugador si es necesario.
		'''
		# Inicializacion de variables:
		otraficha = 0
		fichasCambio = []
		if ficha == 1:
			otraficha = 2
		elif ficha == 2:
			otraficha = 1
		ycambio = 1 # Variable para desplazar la revision por el tablero
		xcambio = 1	# Variable para desplazar la revision por el tablero
		if xinicio+1<=7 and yinicio+1<=7:
			if self.board[xinicio+1][yinicio+1] == otraficha:
				while xcambio+xinicio<7 and ycambio+yinicio<7 and self.board[xinicio+xcambio][yinicio+ycambio] == otraficha:
					fichasCambio.append([xinicio+xcambio,yinicio+ycambio])
					xcambio += 1
					ycambio += 1
				if self.board[xinicio+xcambio][yinicio+ycambio] == ficha:
						for i,j in fichasCambio:
							self.board[i][j] = ficha
		if xinicio-1>=0 and yinicio-1>=0:
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
		if xinicio+1<=7 and yinicio-1>=0:
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
		if xinicio-1>=0 and yinicio+1<=7:
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


	def consumo(self,xinicio,yinicio,ficha):
		self.consumoVertical(ficha,xinicio,yinicio)
		self.consumoHorizontal(ficha,xinicio,yinicio)
		self.consumoDiagonal(ficha,xinicio,yinicio)

	def cambiarTurno(self,game,x,y):
		if game.turno == 1:
			ficha = 1
			game.board.board[x][y]=1
			game.turno = 2
		elif game.turno == 2:
			ficha = 2
			game.board.board[x][y]=2
			game.turno = 1
		return ficha



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
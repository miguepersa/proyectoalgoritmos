from ajustes import *
from os import path
from sprites import *

import pygame as pg
import random


class Game():
	def __init__(self):
		pg.init()
		pg.mixer.init()
		pg.display.set_caption(TITULO)
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		self.running = True
		self.turno = 2
		self.jugada_invalida = False
		self.f_blanca = pg.transform.scale(pg.image.load(path.join(DIR_IMAGENES,'blanca.png')).convert_alpha(),(40,40))
		self.f_negra = pg.transform.scale(pg.image.load(path.join(DIR_IMAGENES,'negra.png')).convert_alpha(),(40,40))



	def new(self):
		# Iniciar un juego nuevo
		self.all_sprites = pg.sprite.Group()
		self.board = Tablero(self,WIDTH/2,WIDTH/2,WIDTH/2-200, 150)
		self.blancas = Jugador(self,1)
		self.negras = Jugador(self,2)
		self.run()

	def run(self):
		# Ciclo del juego
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		# Actualizacion del Ciclo de juego
		self.all_sprites.update()

	def puntos(self):
		self.blancas.puntos = 0
		self.negras.puntos = 0
		for i in range(0,self.board.size):
			for j in range(0,self.board.size):
				if self.board.board[i][j] == 1:
					self.blancas.puntos += 1
				elif self.board.board[i][j] == 2:
					self.negras.puntos += 1


	def events(self):
		# Eventos en el juego
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing == True:
					self.playing = False
				self.running = False

			if event.type == pg.MOUSEBUTTONDOWN:
				click_pos = pg.mouse.get_pos()

				x,y = self.board.ubicacion_click(click_pos)

				if self.board.jugada_valida(x,y):
					self.jugada_invalida = False
					if self.turno == 1:
						self.board.board[x][y]=1
						self.turno = 2
					elif self.turno == 2:
						self.board.board[x][y]=2
						self.turno = 1
					self.puntos()

				else:
					self.jugada_invalida = True


	def escribir_texto(self,surf,text,size,x,y):
		font = pg.font.Font('binchrt.ttf',size)
		text_surface = font.render(text, True, BLACK)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x,y)
		surf.blit(text_surface,text_rect)

	def draw(self):
		# Graficos del juego
		self.screen.fill(GREY)
		self.all_sprites.draw(self.screen)
		self.board.render_board()
		self.escribir_texto(self.screen,"Reversi",40,WIDTH/2,20)
		self.escribir_texto(self.screen,"A B C D E F G H",45,WIDTH/2,100)
		y_numeros = 150
		for i in NUMEROS_TABLERO:
			self.escribir_texto(self.screen,str(i),45,self.board.offset_x-25,y_numeros)
			y_numeros += 50
		self.escribir_texto(self.screen,"BLANCAS",30,WIDTH-100,200)
		self.escribir_texto(self.screen,str(self.blancas.puntos),30,WIDTH-100,250)
		self.escribir_texto(self.screen,"NEGRAS",30,WIDTH-100,350)
		self.escribir_texto(self.screen,str(self.negras.puntos),30,WIDTH-100,400)


		if self.turno == 1:
			self.escribir_texto(self.screen,"Turno de las Blancas",30,WIDTH/2,60)
		else:
			self.escribir_texto(self.screen,"Turno de las Negras",30,WIDTH/2,60)
		if self.jugada_invalida:
			self.escribir_texto(self.screen,"Jugada inválida",20,WIDTH/2,10)		
		# Dibujo de los gráficos
		pg.display.flip()

	def inicio_juego(self):
		# Pantalla de inicio del juego
		pass

	def fin_juego(self):
		# Pantalla de fin de juego
		pass

g = Game()
g.inicio_juego()
while g.running:
	g.new()
	g.fin_juego()

pg.quit()
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
		self.blancas = Jugador(1)
		self.negras = Jugador(2)


	def new(self):
		# Iniciar un juego nuevo
		self.all_sprites = pg.sprite.Group()
		self.board = Tablero(self,WIDTH/2,WIDTH/2,WIDTH/2-200, 150)
		self.run()

	def run(self):
		# Ciclo del juego
		self.playing = True
		self.puntos
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			# self.update()
			self.draw()
		if self.board.fichas_restantes == 0:
			self.playing = False
		if self.blancas.puntos == 0 or self.negras.puntos == 0:
			self.playing = False

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
				turno = self.turno
				if self.board.jugada_valida(x,y,turno):
					self.jugada_invalida = False
					ficha = self.board.cambiarTurno(self,x,y)
					self.board.consumo(x,y,ficha)
					self.puntos()
					self.board.fichas_restantes -= 1

				else:
					self.jugada_invalida = True
			if self.board.fichas_restantes == 0:
				self.playing = False
			elif self.blancas.puntos == 0 or self.negras.puntos == 0:
				self.playing = False


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
		self.escribir_texto(self.screen,self.blancas.nombre,30,WIDTH-100,200)
		self.escribir_texto(self.screen,str(self.blancas.puntos),30,WIDTH-100,250)
		self.escribir_texto(self.screen,self.negras.nombre,30,WIDTH-100,350)
		self.escribir_texto(self.screen,str(self.negras.puntos),30,WIDTH-100,400)


		if self.turno == 1:
			self.escribir_texto(self.screen,"Turno de las Blancas",30,WIDTH/2,60)
		else:
			self.escribir_texto(self.screen,"Turno de las Negras",30,WIDTH/2,60)
		if self.jugada_invalida:
			self.escribir_texto(self.screen,"Jugada inválida",20,WIDTH/2,10)		
		# Dibujo de los gráficos
		pg.display.flip()

	def esperar_tecla(self):
		pg.event.wait()
		waiting = True
		key = None
		while waiting and self.running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.playing = False
					self.running = False
					waiting = False
				if event.type == pg.KEYUP:
					waiting = False
					key = event.key

		return key

	# metodo que espera que se dispare un KEYDOWN event (tambien retorna el evento)
	def esperar_evento(self):
		pg.event.wait()
		waiting = True
		_event = None
		while waiting and self.running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.playing = False
					self.running = False
					waiting = False
					_event = None

				if event.type == pg.KEYDOWN:
					waiting = False
					_event = event

		return _event

	def pantalla_inicio(self):

		# dibujamos la interfaz
		self.screen.fill(GREY)
		self.escribir_texto(self.screen,self.blancas.nombre,50,WIDTH / 6, 20)
		self.escribir_texto(self.screen,self.negras.nombre,50,(WIDTH * 5) / 6, 20)

		self.escribir_texto(self.screen,'Bienvenidos al Reversi',60, WIDTH / 2, 250)
		self.escribir_texto(self.screen,'Presionen cualquier tecla para jugar',30, WIDTH / 2, 500)

		pg.display.flip()

		# esperamos a que el usuario presione la tecla
		key = self.esperar_tecla()


	def entrada_nombres(self):

		# inicializamos las variables a recibir
		nombre1 = ''
		nombre2 = ''

		entrada1lista = False
		entrada2lista = False

		# dibujamos la interfaz
		self.screen.fill(GREY)
		self.escribir_texto(self.screen,'Jugador 1 ingresa tu nombre',50,WIDTH / 2, 60)
		self.escribir_texto(self.screen,'usa backspace para borrar',30,WIDTH / 2, 100)


		self.escribir_texto(self.screen,'',80, WIDTH / 2, 250)
		self.escribir_texto(self.screen,'presiona espacio cuando estes listo',40,WIDTH / 2, 500)
		pg.display.flip()

		# obtenemos el nombre del jugador 1
		while (not entrada1lista) and self.running:
			alert = ''

			# esperamos a que se presione una tecla
			event = self.esperar_evento()

			if event != None:

				# si el usuario presiona espacio
				if event.key == pg.K_SPACE:
					# y ya introdujo su nombre
					if len(nombre1) > 0:
						# entonces ya tenemos el nombre
						entrada1lista = True
					else:
						alert = 'Debes ingresar tu nombre'

				# si el usuario presiono backspace
				elif event.key == pg.K_BACKSPACE:
					# borramos el ultimo caracter del nombre
					if len(nombre1) > 0:
						nombre1 = nombre1[:-1]

				# si presiona otra tecla, le agregamos el caracter al nombre
				else:
					nombre1 += event.unicode

			# dibujamos la interfaz
			self.screen.fill(GREY)
			self.escribir_texto(self.screen,'Jugador 1 ingresa tu nombre',50,WIDTH / 2, 60)
			self.escribir_texto(self.screen,'usa backspace para borrar',30,WIDTH / 2, 100)


			self.escribir_texto(self.screen,nombre1,80, WIDTH / 2, 250)
			self.escribir_texto(self.screen,alert,30, WIDTH / 2, 400)
			self.escribir_texto(self.screen,'presiona espacio cuando estes listo',40,WIDTH / 2, 500)
			pg.display.flip()

		# dibujamos la interfaz
		self.screen.fill(GREY)
		self.escribir_texto(self.screen,'Jugador 2 ingresa tu nombre',50,WIDTH / 2, 60)
		self.escribir_texto(self.screen,'usa backspace para borrar',30,WIDTH / 2, 100)


		self.escribir_texto(self.screen,'',80, WIDTH / 2, 250)
		self.escribir_texto(self.screen,'presiona espacio cuando estes listo',40,WIDTH / 2, 500)
		pg.display.flip()

		# obtenemos el nombre del jugador 2
		while (not entrada2lista) and self.running:

			alert = ''

			# esperamos a que se presione una tecla
			event = self.esperar_evento()

			if event != None:

				# si el usuario presiona espacio
				if event.key == pg.K_SPACE:
					# y ya introdujo su nombre
					if len(nombre2) > 0:
						# entonces ya tenemos el nombre
						entrada2lista = True
					else:
						alert = 'debes ingresar tu nombre'

				# si el usuario presiono backspace
				elif event.key == pg.K_BACKSPACE:
					# borramos el ultimo caracter del nombre
					if len(nombre2) > 0:
						nombre2 = nombre2[:-1]

				# si presiona otra tecla, le agregamos el caracter al nombre
				else:
					nombre2 += event.unicode

			# dibujamos la interfaz
			self.screen.fill(GREY)
			self.escribir_texto(self.screen,'Jugador 2 ingresa tu nombre',50,WIDTH / 2, 60)
			self.escribir_texto(self.screen,'usa backspace para borrar',30,WIDTH / 2, 100)


			self.escribir_texto(self.screen,nombre2,80, WIDTH / 2, 250)
			self.escribir_texto(self.screen,alert,30, WIDTH / 2, 400)
			self.escribir_texto(self.screen,'presiona espacio cuando estes listo',40,WIDTH / 2, 500)
			pg.display.flip()

		# guardamos los datos
		if self.running:
			self.blancas.nombre = nombre1
			self.negras.nombre = nombre2


	def fin_juego(self):

		# dibujamos la interfaz
		self.screen.fill(GREY)
		self.escribir_texto(self.screen,self.blancas.nombre,50,WIDTH / 6, 20)
		self.escribir_texto(self.screen,self.negras.nombre,50,(WIDTH * 5) / 6, 20)
		self.escribir_texto(self.screen,str(self.blancas.puntos),50, WIDTH / 6, 60)
		self.escribir_texto(self.screen,str(self.negras.puntos),50,(WIDTH * 5) / 6, 60)

		# dibujamos en la pantalla el resultado de la partida
		main_string = ''

		if self.blancas.puntos > self.negras.puntos :
			main_string = 'El ganador es ' + self.blancas.nombre
		elif self.blancas.puntos < self.negras.puntos :
			main_string = 'El ganador es ' + self.negras.nombre
		else:
			main_string = 'Es un empate'

		self.escribir_texto(self.screen,main_string,40, WIDTH / 2, 250)
		self.escribir_texto(self.screen,'presionen \'Y\' para jugar otra vez.',30, WIDTH / 2, 350)

		pg.display.flip()

		# esperamos a que el usuario presione la tecla
		key = self.esperar_tecla()

		# si el usuario decidio seguir jugando entonces seguimos, de lo contrario cerramos el programa
		if key != pg.K_y:
			self.running = False
			
		self.blancas.puntos = 2
		self.negras.puntos = 2

g = Game()
g.pantalla_inicio()
g.entrada_nombres()
while g.running:
	g.new()
	if g.running:
		g.fin_juego()

pg.quit()
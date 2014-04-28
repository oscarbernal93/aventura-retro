#! /usr/bin/python

import random
import pygame
from pygame.locals import *

##	CONSTANTES	##
ANCHO=800
ALTO=640
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0) 
VERDE = (0,255,0)
AZUL = (0,0,255)

## 	CLASES	##

class Block(pygame.sprite.Sprite):
	#Constructor
    def __init__(self, color, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.width = width
       self.height = height
       #crea una imagen de las dimenciones espefificadas
       self.image = pygame.Surface([self.width, self.height])
       #la rellena con el color correspondiente
       self.image.fill(color)
       #define el rectangulo de coliciones
       self.rect = self.image.get_rect()
       self.vely = 1
       self.velx = 0
       self.aire = True   # atributo para saber si esta en el aire
       self.bloqueo = False  # atributo para saber si bloquea el paso 
       self.frenar = False

##	FUNCIONES	##

# funcion de carga de imagenes
def cargar_imagen(archivo,transpartente = False):
	try: imagen = pygame.image.load(archivo)
	except pygame.error, mensaje:
		raise SystemExit, mensaje
	imagen = imagen.convert()
	if transpartente:
		imagen.convert_alpha()
	return imagen

def gravedad(bloque):
	bloque.rect.y += bloque.vely
	bloque.rect.x += bloque.velx
	if bloque.aire and bloque.vely < 10:
		bloque.vely += 1

# funcion principal del juego
def juego():
	pygame.init()
	pantalla = pygame.display.set_mode((ANCHO, ALTO))
	pygame.display.set_caption("Gravedad")
	fondo = cargar_imagen("espacio.jpg")

	# posicion del cubo (x,y)
	sprites = pygame.sprite.Group()
	#definicion del cubo
	cubo = Block(ROJO,20,20)
	#definicion del piso
	piso = Block(NEGRO,800,100)
	piso.rect.x=0
	piso.rect.y=540
	sprites.add(piso)
	# definicion de otro objeto
	cosa = Block(NEGRO,250,50)
	cosa.rect.x=0
	cosa.rect.y=300
	sprites.add(cosa)
	# definicion aleatoria de objetos
	for i in range(20):
		b = Block(NEGRO, 100, 20)
		b.rect.y = random.randrange(ALTO)
		b.rect.x = random.randrange(ANCHO)
		sprites.add(b)
	

	# configuraciones de pygame,reloj y teclado
	reloj = pygame.time.Clock()
	pygame.key.set_repeat(60,0)
	# ciclo prinicipal
	while True:
		#se dibuja el fondo
		pantalla.blit(fondo,(0,0))
		gravedad(cubo)

		sprites.draw(pantalla)
		pantalla.blit(cubo.image,cubo.rect)
		pygame.display.flip()

		alone = True;
		for x in sprites:
			if pygame.sprite.collide_rect(cubo, x):
				if cubo.vely > 0 and cubo.rect.y < x.rect.y:  ## si esta cayendo
					cubo.aire = False
					cubo.vely = 0
					cubo.rect.y=x.rect.y-cubo.height+1
				elif cubo.vely < 0 and cubo.rect.y > x.rect.y:  ## si esta saltando
					cubo.aire = True
					cubo.vely = 0
					cubo.rect.y=x.rect.y+cubo.height-1
				elif cubo.velx > 0 and cubo.frenar: ## si se mueve a la derecha y va a frenar, frena
					cubo.velx += -1 
				elif cubo.velx < 0 and cubo.frenar: ## si se mueve a la izquierda y va a frenar, frena
					cubo.velx += 1 
				alone = False
		if alone:
			cubo.aire=True
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_LEFT :
					cubo.frenar=False
					cubo.velx += -1
				elif event.key == pygame.K_RIGHT:
					cubo.frenar=False
					cubo.velx += 1
				elif event.key == pygame.K_UP:
					if not cubo.aire:
						cubo.vely += -10
					cubo.aire=True
				elif event.key == pygame.K_DOWN:
					cubo.vely+= 1
				#if event.key == pygame.K_a:
				
				if event.key == pygame.K_ESCAPE:
					raise SystemExit
			if event.type == pygame.QUIT:
				raise SystemExit
			if event.type == pygame.KEYUP :
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
					cubo.frenar = True
		reloj.tick(60)
juego()
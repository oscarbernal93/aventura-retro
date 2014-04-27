#! /usr/bin/python

import random
import pygame
from pygame.locals import *

##	CONSTANTES	##
ANCHO=800
ALTO=600
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
       #crea una imagen de las dimenciones espefificadas
       self.image = pygame.Surface([width, height])
       #la rellena con el color correspondiente
       self.image.fill(color)
       #define el rectangulo de coliciones
       self.rect = self.image.get_rect()

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
	bloque.rect.y += 1

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
	sprites.add(cubo)
	#definicion del piso
	piso = Block(NEGRO,800,100)
	piso.rect.x=0
	piso.rect.y=500
	sprites.add(piso)
	

	# configuraciones de pygame,reloj y teclado
	reloj = pygame.time.Clock()
	pygame.key.set_repeat(1,50)
	# ciclo prinicipal
	while True:
		#se dibuja el fondo
		pantalla.blit(fondo,(0,0))
		gravedad(cubo)
		sprites.draw(pantalla)
		pygame.display.flip()
		tecla = pygame.key.get_pressed()

		for event in pygame.event.get():
			if tecla[K_LEFT]:
				cubo.rect.x += -1
			if tecla[K_RIGHT]:
				cubo.rect.x += 1
			if tecla[K_UP]:
				cubo.rect.y += -1
			if tecla[K_DOWN]:
				cubo.rect.y += 1
			if tecla[K_a]:
				print "teclaA"
			if tecla[K_ESCAPE] or event.type == pygame.QUIT:
				raise SystemExit
		reloj.tick(60)
juego()
#! /usr/bin/python

import random
import pygame
import sys
from pygame.locals import *
import ConfigParser

#####------------------------------------------
#####-----------constantes

SX = 32
SY = 32

###----------------------------------------------
###-------------funciones
#crear ventana
def crear_ventana(ancho, alto, fondo,titulo):
	pygame.init()

	#creacion de la ventana
	ventana = pygame.display.set_mode((ancho,alto))
	#titulo de la ventana
	pygame.display.set_caption(titulo)

	#cargar fondo
	fondo_ventana = pygame.image.load(fondo).convert()
	#se anade fondo a la ventana
	ventana.blit(fondo_ventana,(0,0))

	return ventana

	
	


# funcion de carga de imagenes
def cargar_imagen(archivo,transpartente = False):
	try: imagen = pygame.image.load(archivo)
	except pygame.error, mensaje:
		raise SystemExit, mensaje
	imagen = imagen.convert()
	if transpartente:
		imagen.convert_alpha()
	return imagen

#funcion para la carga de mapas, retorna el sprite correspondiente en la
#matriz del atributo mapa, de la etiqueta [nivel]
def cargar_mapa(archivo):
	externo = ConfigParser.ConfigParser()
	externo.read(archivo)
	mapa = externo.get("nivel", "mapa").split("\n")
	sprites = cargar_sprites("terrain.png",SX, SY)
	print mapa
	mapa_con_sprites = []
	for cad in mapa:
		listasprites = []
		for c in cad:
			sprite_x = externo.get(c,"x")
			sprite_y = externo.get(c, "y") 
			listasprites.append(sprites[int(sprite_x)][int(sprite_y)])
		mapa_con_sprites.append(listasprites)
	return mapa_con_sprites

	
	
	


##retorna la tabla de sprites
def cargar_sprites(archivo,ancho,alto):
	imagen = pygame.image.load(archivo).convert_alpha()
	imagen_ancho, imagen_alto = imagen.get_size()
	#print imagen_ancho
	#print imagen_alto
	tabla_fondos = []
	for fondo_x in range(0, imagen_ancho/ancho):
		linea = []
		tabla_fondos.append(linea)
		for fondo_y in range(0,imagen_alto/alto):
			cuadro = (fondo_x * ancho, fondo_y * alto,ancho,alto)
			linea.append(imagen.subsurface(cuadro))
	return tabla_fondos


#####-----------------------------------------
#####--------------MAIN

def main():
	##25x20 en la matriz del ini
	ventana = crear_ventana(800,640,"fondo.jpg","mapa1")
	mapa = cargar_mapa("mapa1.ini")
	while True:
		for x, fila in enumerate (mapa):
			for y, cuadro in enumerate (fila):
				ventana.blit (cuadro, (y*(SY),x*(SX)))
		#se muestra la ventana
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


###---ejecucion del main
if __name__ == "__main__":
    main()



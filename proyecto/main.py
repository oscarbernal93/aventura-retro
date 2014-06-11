#! /usr/bin/python

import random
import pygame
import sys
from pygame.locals import *
import ConfigParser

#####------------------------------------------
#####-----------constantes
#tamano sprites
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
def cargar_mapa(archivo,nivel):
	externo = ConfigParser.ConfigParser()
	externo.read(archivo)
	mapa = externo.get(nivel, "mapa").split("\n")
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


########----------------------------------------------------------------------------
########---------------Menu de Inicio-----------------------------------------------

class Menu:
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    kolor_tla = (51,51,51)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection
        
    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.pozycja_zaznaczenia
    
    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()        
        
    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun 
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in xrange(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2            
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my) 

########---------------Fin menu inicio----------------------------------------------

######------control menu

def control_menu():
	#creacion del menu
    menu= Menu()

    menu.init(['Start','Options','Quit'], ventana)
    menu.draw()


    pygame.key.set_repeat(199,69)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:
                    if menu.get_position() == 2:#here is the Menu class function
                        pygame.display.quit()
                        sys.exit()
                    if menu.get_position() == 0:
                        print "hola"
                        main()                    
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)
	


#####-----------------------------------------
#####--------------MAIN

def main():
	##25x20 en la matriz del ini
	corrimientox=0
	corrimientoy=0
	#ventana = crear_ventana(800,640,"fondo.jpg","mapa1")
	mapa = cargar_mapa("mapa1.ini","nivel")

	#sonido de saltp
	sound_jump = pygame.mixer.Sound("sounds/jump.wav")
	while True:
		#antes de dibujar los sprite se dibuja el fondo
		ventana.fill((0,0,0))

		fondo_ventana = pygame.image.load("fondo.jpg").convert()
		#se anade fondo a la ventana
		ventana.blit(fondo_ventana,(0,0))
		for x, fila in enumerate (mapa):
			for y, cuadro in enumerate (fila):
				ventana.blit (cuadro, (y*(SY)+corrimientoy,x*(SX)+corrimientox))
		#se muestra la ventana
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_LEFT :
					corrimientoy += 15
				elif event.key == pygame.K_RIGHT:
					corrimientoy -= 15
					#carga el nivel 2
					mapa = cargar_mapa("mapa1.ini","nivel2")
					#mapa = cargar_mapa("mapa1.ini","nivel")
				if event.key == K_UP:
					sound_jump.play()


###---ejecucion del main
if __name__ == "__main__":
    #main()
    ventana = crear_ventana(800,640,"fondo_menu.png","mapa1")
    control_menu()




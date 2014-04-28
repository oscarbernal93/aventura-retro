#! /usr/bin/python

import ConfigParser


archivo="iniciar_mapa.ini"
externo = ConfigParser.ConfigParser()

print "antes de leer el archivo"
print externo.sections()

externo.read(archivo)
print "despues de leer el archivo"
print externo.sections()

#-----------------------

#obteniendo elementos
s1 = externo.get("@", "tipo")
print s1

#------------------------------
#mirando las lineas (filas)
mapa = externo.get("nivel", "mapa").split("\n")
for nf, filas in enumerate(mapa):
	print nf,filas
	
#--------------------------
indice={}
for seccion in externo.sections():
	print "longitud: ", len(seccion)
	if len(seccion)== 1:
		desc = dict(externo.items(seccion))
		indice[seccion]= desc
		
print "llaves: ", indice.keys()
ancho = len(mapa[0])
alto = len(mapa)
print "ancho: ", ancho, "alto: ", alto

print "posicion (2,2): ", mapa[2][2], "posicion (0,2): ", mapa[0][2]

#---------------------
info={}
try:
	char = mapa[2][10]
	print char
except IndexError:
	print "error"
	
try:
	info = indice[char]
	print info
except KeyError:
	print "error"

t="tipo"

print info[t]


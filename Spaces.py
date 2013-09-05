import pygame
from pygame.locals import *
import sys

#Libreria opcional
import os

dir_sonido = "Sonidos"
from random import randint

#Variables Globales
width = 900
height = 480
ListaEnemigos= []


def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    try:
        sonido = pygame.mixer.Sound(ruta)
    except pygame.error, message:
        print "No se pudo cargar el sonido:", ruta
        sonido = None
    return sonido
 


class NaveEspacial(pygame.sprite.Sprite):
	"Estamos Creaando una nueva Nave Espacial para nuestro juego"

	def __init__(self,SonidoExplosion, SonidoDisparo):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load("Imagenes/nave.jpg")
		self.ImagenNaveExposion = pygame.image.load("Imagenes/explosion.jpg")

		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = width/2
		self.rect.centery = height-30

		self.listaDisparo = []
		self.Vida= True
		self.SonidoDisparo=SonidoDisparo
		self.SonidoExplosion=SonidoExplosion

	def Movimiento(self):
		if self.Vida==True:
			if self.rect.left <=0:
				self.rect.left=0
			elif self.rect.right>870:
				self.rect.right=640

	def Dibujar(self,Superficie):
		Superficie.blit(self.ImagenNave,self.rect)

		#Debe
	def Disparo(self,x,y):
		arma = Proyectil(0)
		x=x-5
		arma.coordenadas(x,y)
		self.SonidoDisparo.play()
		self.listaDisparo.append(arma)

	def DeteccionColision(self,objetivo):
		if self.rect.colliderect(objetivo.rect):
			self.SonidoDisparo.stop()
			self.AutoDestruccion()
			return True
		else:
			return False

	def AutoDestruccion(self):
		self.SonidoExplosion.play()
		print "\n"
		self.ImagenNave = self.ImagenNaveExposion
		self.Vida=False 

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,posicion):
		pygame.sprite.Sprite.__init__(self)
		self.imagenProyectilNave = pygame.image.load("imagenes/disparoa.jpg")
		self.imagenProyectilEnemigo = pygame.image.load("Imagenes/disparob.jpg")

		self.listaImagenesProyectil = [self.imagenProyectilNave,self.imagenProyectilEnemigo]
		
		self.imagenProyectil = self.listaImagenesProyectil[posicion]
		self.posicion = posicion 
		self.rect = self.imagenProyectil.get_rect()
		self.posy= 0
		self.posx= 0
		self.velocidadDisparo = 10

	def Update(self, superficie):
		"""if self.posicion ==0:
			self.posy = self.posy - self.velocidadDisparo
			self.Dibujar(superficie)
		else:
			self.posy= self.posy + self.velocidadDisparo
			self.Dibujar(superficie)"""
		if self.posicion==0:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo
		self.Dibujar(superficie)


	def Dibujar(self,superficie):
		#superficie.blit(self.imagenProyectil, (self.posx, self.posy))
		superficie.blit(self.imagenProyectil,self.rect)
	def coordenadas(self, px, py):
		self.posy ,self.posx= py,px
		self.rect.top= self.posy
		self.rect.left= self.posx

	def DeteccionColision(self,objetivo):
		if self.rect.colliderect(objetivo.rect):
			return True

class Invasores(pygame.sprite.Sprite):
	def __init__(self,x,y,distancia,ImagenUno,ImagenDos):
		pygame.sprite.Sprite.__init__(self)
		#self.imagenInvasorA = pygame.image.load("Imagenes/MarcianoA.jpg")
		#self.imagenInvasorB = pygame.image.load("Imagenes/MarcianoB.jpg")

		self.imagenInvasorA = pygame.image.load(ImagenUno)
		self.imagenInvasorB = pygame.image.load(ImagenDos)
								#0 							1
		self.listaImagenes= [self.imagenInvasorA, self.imagenInvasorB]
		self.ImagenActual = 0

		self.SonidoDisparo=pygame.mixer.Sound("Sonidos/laserAlien.wav")

		self.listaDisparo= []
		self.ImagenInvasor= self.listaImagenes[self.ImagenActual]
		self.rect = self.ImagenInvasor.get_rect()
		
		self.rect.centerx = x
		self.rect.centery = y

		self.Arriba = False
		self.Derecha = True
		self.velocidad= 20

		self.limiteDerecha = x +distancia
		self.limiteIzquierda = x-distancia
		self.ContadorDecenso= 0
		self.descenso = 0
		self.ContadorImagen = 0

		self.Tiempo=1
		self.conquista= False
		self.RangoDisparo =1

	def Dibujar(self,Superficie):
		self.ImagenInvasor= self.listaImagenes[self.ImagenActual]
		Superficie.blit(self.ImagenInvasor,self.rect)

	def Comportamiento(self,Tiempo):
		if self.conquista==False:
			if self.ContadorDecenso < 1:
				self.MovimientoDerecha()
			else:
				if self.Abajo==False:
					self.descenso = self.rect.top +30
					self.Abajo=True
				if self.rect.top == self.descenso:
					self.ContadorDecenso=0
				else:
					self.MovimientoAbajo()

			self.Disparo()
			self.SiguienteImagen(Tiempo)

	def SiguienteImagen(self,Tiempo):
		if self.Tiempo == Tiempo: 
			self.ImagenActual +=1
			self.Tiempo = self.Tiempo + 1
			if self.ImagenActual > len(self.listaImagenes)-1:
				self.ImagenActual = 0
		else:
			if self.Tiempo < Tiempo:
				self.Tiempo = Tiempo+ 1
			
	
	def MovimientoAbajo(self):
		self.rect.top += 1 

	def MovimientoDerecha(self):
		if self.rect.left>=self.limiteIzquierda and self.rect.left <self.limiteDerecha and self.Derecha==True:
			
			if self.rect.left ==self.limiteIzquierda:
				self.ContadorDecenso= self.ContadorDecenso + 1
				self.Abajo= False
			self.rect.left +=self.velocidad
		else:
			self.Derecha=False
			if self.rect.left>self.limiteIzquierda:
				self.rect.left -=self.velocidad
			else:
				self.Derecha=True
				self.rect.left=self.limiteIzquierda

	def Disparo(self):
		if (randint(0,100))<self.RangoDisparo:
			arma = Proyectil(1)
			x,y = self.rect.center
			x=x-5
			arma.coordenadas(x,y)
			self.listaDisparo.append(arma)
			self.SonidoDisparo.play()

	def DeteccionColision(self,objetivo):
		if self.rect.colliderect(objetivo.rect):
			return True

def CreadorEnemigos(Tiempo):
	ListaImagenesEnemigos = ["Imagenes/MarcianoA.jpg", "Imagenes/MarcianoB.jpg", 
							"Imagenes/Marciano2A.jpg", "Imagenes/Marciano2B.jpg",
							"Imagenes/Marciano3A.jpg", "Imagenes/Marciano3B.jpg"
							]
	if len(ListaEnemigos)>0:
		for x in ListaEnemigos:
			ListaEnemigos.remove(x)
			print "Eliminando"
	Distancia = 140

	for PosXEnemigo in range(1,5):
		if PosXEnemigo == 1:
			Enemigo = Invasores((5*Distancia), 30,Distancia,ListaImagenesEnemigos[0],ListaImagenesEnemigos[1])
		else:
			Enemigo = Invasores((PosXEnemigo*Distancia), 30,Distancia,ListaImagenesEnemigos[0],ListaImagenesEnemigos[1])
			Enemigo.Tiempo= Tiempo
		ListaEnemigos.append(Enemigo)
	
	for PosXEnemigo in range(1,5):
		Enemigo = Invasores((PosXEnemigo*Distancia),-60,Distancia,ListaImagenesEnemigos[2],ListaImagenesEnemigos[3])
		ListaEnemigos.append(Enemigo)
	
	for PosXEnemigo in range(1,5):
		Enemigo = Invasores((PosXEnemigo*Distancia),-150,Distancia,ListaImagenesEnemigos[4],ListaImagenesEnemigos[5])
		ListaEnemigos.append(Enemigo)
		


#Metodo principal 
def SpaceInvader():
	pygame.init()
	Pantalla = pygame.display.set_mode((width,height,))
	pygame.display.set_caption("Demo de nuestros Space Inavders")
	
	#Variables
	ImagenFondo = pygame.image.load("Imagenes/Fondo.jpg")
	
	SonidoFondo = os.path.join("Sonidos", "Intro.mp3")

	SonidoE = load_sound("deadSpaceShip.wav",dir_sonido)
	SonidoD = load_sound("laserSpace.wav",dir_sonido)

	pygame.mixer.music.load(SonidoFondo)
	pygame.mixer.music.play(3)
	sonido = pygame.mixer.Sound("sonido.wav")

	Juego = True
	velocidad = 40
	Tiempo= 0
	ListaProyectiles = []

	#Debemos de crear una Fuente
	MiFuente = pygame.font.Font(None,48)
	Texto= MiFuente.render("Fin del juego",0,(200,200,200))
	TextoGanador = MiFuente.render("Ganaste  ",0,(200,0,200))
	#Objetos
	Jugador = NaveEspacial(SonidoE,SonidoD)
	reloj = pygame.time.Clock()
	
	cantidadEnemigos = len(ListaEnemigos)
	CreadorEnemigos(1)
	A= True
	while A:
		reloj.tick(50)
		
	
		Jugador.Movimiento()
		
		Tiempo = pygame.time.get_ticks()/1000
		
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sys.exit(0)

			#Colocar esta condicion desdel el comienzo
			if Juego==True: 
				if evento.type == pygame.KEYDOWN:
					if evento.key == K_LEFT:
						Jugador.rect.left -=velocidad
						
					elif evento.key == K_RIGHT:
						Jugador.rect.right +=velocidad

				elif evento.type == pygame.KEYUP:
					if evento.key == K_LEFT:
						Jugador.rect.centery +=0

					elif evento.key == K_RIGHT:
						Jugador.rect.centery +=0
					elif evento.key == K_s:
						x,y= Jugador.rect.center
						Jugador.Disparo(x,y)
						sonido.play()
			"""
			else:
				if evento.type == pygame.KEYUP:
					if evento.key == K_r:
						SpaceInvader()
						CreadorEnemigos(Tiempo+3)
						pygame.display.update()
						A=False"""

					
		Pantalla.blit(ImagenFondo,(0,0))
		Jugador.Dibujar(Pantalla)
		
		#Todo lo que Tiene que ver con los Enemigos
		if len(ListaEnemigos)>0:
			for Invasor in ListaEnemigos:
				Invasor.Comportamiento(Tiempo)
				Invasor.Dibujar(Pantalla)

				if Juego== True:
					if Jugador.DeteccionColision(Invasor):
						Juego = False

					if Invasor.rect.top > 600:
						Jugador.AutoDestruccion()
						Juego = False


				#Si el enemigo disparo
				if len(Invasor.listaDisparo)>0:
					for x in Invasor.listaDisparo :
						x.Update(Pantalla)
						if x.posy > 800:
							Invasor.listaDisparo.remove(x)
						else:	
							if Jugador.DeteccionColision(x):
								Juego = False
						if len(Jugador.listaDisparo)>0:
							for A in Jugador.listaDisparo:
								if A.rect.colliderect(x.rect):
									Jugador.listaDisparo.remove(A)
									Invasor.listaDisparo.remove(x)

		else:
			Pantalla.blit(TextoGanador,(200,200))

		#Enemigo.Dibujar(Pantalla)
		#Tenemos que colocar las balas despues de que el fondo 
		#se encuentre actualizado
	
		if len(Jugador.listaDisparo)>0:
			for bala in Jugador.listaDisparo:
				bala.Update(Pantalla)
				if bala.posy < 10:
					Jugador.listaDisparo.remove(bala)
				else:
					for x in ListaEnemigos:
						if bala.DeteccionColision(x):
							Jugador.listaDisparo.remove(bala)
							ListaEnemigos.remove(x)

		if Juego==False:
			for enemigoVivo in ListaEnemigos:
				enemigoVivo.conquista=True

				if len(enemigoVivo.listaDisparo)>0:
					for disparosEnemigos in enemigoVivo.listaDisparo:
						enemigoVivo.listaDisparo.remove(disparosEnemigos)


			if len(Jugador.listaDisparo)>0:
				for balas in Jugador.listaDisparo:
					bala.velocidadDisparo=0
			pygame.mixer.music.fadeout(3000)#Detiene la cansion Gradualmente
			Pantalla.blit(Texto,(200,200))
		pygame.display.update()

#LLamamos al metodo principal
SpaceInvader()

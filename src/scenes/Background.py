
# -------------------------------------------------
# Clase Cielo

class Background(object):
	def __init__(self):
		#self.map = ResourceManager.load_image('background.png', -1)
		#self.map = pygame.transform.scale(self.map, (300, 200))
		self.backgroundColour = (100, 200, 255)
		#self.rect = self.map.get_rect()
		#self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
		self.update(0)

	def update(self, time):
		#self.posicionx += VELOCIDAD_SOL * tiempo
		# if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
		# 	self.posicionx = 0
		# self.rect.right = self.posicionx
		# # Calculamos el color del cielo
		# if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
		# 	ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
		# else:
		# 	ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
		#self.backgroundColour = (100*ratio, 200*ratio, 255)
		return

	def draw(self, screen):
		# Dibujamos el color del cielo
		screen.fill(self.backgroundColour)
		# Y ponemos el sol
		#screen.blit(self.map, self.rect)

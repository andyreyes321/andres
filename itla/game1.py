#pygame, una biblioteca q nos facilita el crear games
import pygame

pygame.init()

#esta parte crea el tamaño del personaje y del enemigo
scale_personaje = 1.0
scale_enemigo = 1.7

#aqui cargue la imagen del fondo
paisaje = pygame.image.load("assets/image/paisaje/paisaje1.png")
#pygame.transform.scale sirve para darle un tamaño a nuestra imagen
paisaje = pygame.transform.scale(paisaje, (1000, 600))

#aqui cargamos la imagen del ataque, similar al del paisaje
img_ataque = pygame.image.load("assets/image/weapons/energy_ball.0.png")
img_ataque = pygame.transform.scale(img_ataque, (100, 50))  

#aqui defini el "escalar" refiriendome a el tamaño q le queria dar a cada cosa
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

#aqui cree las animaciones usando un bucle que corra desde la imagen 0 hasta la imagen 7, 
animacion = []
for i in range(7):
    img = pygame.image.load(f"assets/image/character/player/player_{i}.PNG")
    img = escalar_img(img, scale_personaje)
    animacion.append(img)
#aqui hize algo similar pero con la animacion del enemigo   
animacion_enemigo = []
for i in range(8):
    img_enemigo = pygame.image.load(f"assets/image/character/enemigo/enemigo.{i}.PNG")
    img_enemigo = escalar_img(img_enemigo, scale_enemigo)
    animacion_enemigo.append(img_enemigo)

#en esta parte cree variables utiles que use en el juego, como altura o fps , velocidad etc...
width = 1000
height = 600
height_1= 100
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("rosendo") #me permite darle un nombre a la pestaña
FPS = 80
velocidad = 5

#colores q se usan en el juego (uso mas como recordatorio)
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris = (200, 200, 200)
verde = (0, 255, 0)
rojo = (255, 0, 0)

#primera parte para definir los controles, mover a la izquierda y derecha con "a" y "d", lo iniciamos en false
mover_izquierda = False
mover_derecha = False

#aqui nombramos las variables que usamos para saltar, la gravedad y la velocidad de salto
gravedad = 0.5
velocidad_salto = -15

#definimos clase jugador, aqui le daremos sus caracteristicas
class Player:
    def __init__(self, x, y, animacion): #x and y es donde el jugador se ubica, y le damos lo ya antes creado animacion
        self.flip = False # esto me dice si la imagen está volteada o no
        self.animacion = animacion #aqui le otorgo las imagenes ya antes cargadas
        self.frame_index = 0 #el frame index vendria siendo la imagen ya antes cargada, osea con cual comienza
        self.update_time = pygame.time.get_ticks()# Obtiene el tiempo actual en milisegundos desde que comenzó el juego.
        self.image = animacion[self.frame_index]#aqui le otorgo la imagen, donde tiene tanto la animacion como el index
        self.rect = self.image.get_rect() #esto crea una hitbox al personaje, usando el rect
        self.shape = pygame.Rect(0, 0, 20, 20) #self shape en como la ubicacion mas o menos
        self.shape.center = (x, y) #aqui centramos al jugador en el centro usando la x and y
        self.en_suelo = True #aqui indicamos q inicie én el suelo 
        self.saltar = False #le damos la opcion de saltar pero empienza en false
        self.velocidad_y = 0

#definimos el movimiento
    def movimiento(self, delta_x): #usamos condicionales, nos permite voltear al jugador
        if delta_x < 0: 
            self.flip = True 
        if delta_x > 0:
            self.flip = False    
        self.shape.x += delta_x 

#aqui definimos la actualizacion (muy necesario)
    def update(self):
        cooldown_animacion = 100 #es como el tiempo de avance del personaje
        self.image = self.animacion[self.frame_index]  
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animacion):
                self.frame_index = 0
        #aqui definimos el saltar, si cumple ambas condiciones pues las propiedades antes dadas se ponen en false
        if self.saltar and self.en_suelo:
            self.velocidad_y = velocidad_salto
            self.en_suelo = False
            self.saltar = False
        #esta parte suma la velocidad con la gravedad para permitir un salto
        self.velocidad_y += gravedad
        self.shape.y += self.velocidad_y
        #esta parte nos permite q el jugador tenga una altura sin q se salga de la pantalla
        if self.shape.bottom >= height - 100:
            self.shape.bottom = height - 100
            self.en_suelo = True
            self.velocidad_y = 0
    #aqui dibujamos lo antes ya creado, en el interfaz que seria como la ventana del game
    def draw(self, interfaz):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.shape)
 #aqui la clase enemigo, tiene similares propiedades a las del jugador
class Enemigos():
    def __init__(self, x, y, animacion_enemigo, player):# inicio , le damos propiedades
        self.animacion = animacion_enemigo #la animacion 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = pygame.transform.flip(animacion_enemigo[self.frame_index], True, False)

        self.rect = self.image.get_rect()

        self.rect.x = player.shape.x + 100
        self.rect.y = player.shape.y -120

        self.velocidad_x = -3

    def update(self):
        self.rect.x += self.velocidad_x

        if self.rect.right < 0:
            self.rect.x = width

        cooldown_animacion = 100
        self.image = self.animacion[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animacion):
                self.frame_index = 0

        self.image = pygame.transform.flip(self.animacion[self.frame_index], True, False)

    def draw(self, interfaz):
        interfaz.blit(self.image, self.rect) #en Pygame es una forma de dibujar una superficie sobre otra.
    
   

#aqui creamos la clase de ataque, tambien similar a la clase player
class Ataque():  
    def __init__(self, x, y):
        self.image = img_ataque
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 10 

    def update(self):
        self.rect.x += self.velocidad_x  
        if self.rect.x > width:  
            return True
        return False

    def draw(self, interfaz):
        interfaz.blit(self.image, self.rect)

#aqui abajo llamos a nuestras clases 
player = Player(0, height - 100, animacion)

enemigo = Enemigos(1000, 100, animacion_enemigo, player)

ataques = []  

sprite = pygame.sprite.Group() #Los sprites son imágenes o animaciones que representan objetos, personajes
sprite.add_internal(player)
sprite.add_internal(enemigo)

reloj = pygame.time.Clock()

x = 0
#aqui esta el bucle principal del juego
run = True
while run:
    reloj.tick(FPS)

    delta_x = 0

    if mover_derecha:
        delta_x = velocidad
    if mover_izquierda:
        delta_x = -velocidad


    player.movimiento(delta_x)
    player.update()
#sirve para cerrar el juego
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
        #aqui creamos ya los controles del juego
        if event.type == pygame.KEYDOWN: #keydown es si la tecla esta presionada o no
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_SPACE and player.en_suelo:
                player.saltar = True
            if event.key == pygame.K_f: 
                ataques.append(Ataque(player.shape.x + 30, player.shape.y)) 
        #aqui el keyup es por si soltamos la tecla  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_SPACE:
                player.saltar = False

    #esta parte ya es pra q cuando el ataque toque al enemigo el muera
    for ataque in ataques[:]:  
        if ataque.update():  
            ataques.remove(ataque)   
        
         #creamos una condicion usando el colliderect, q dice q si ambas hitbox chocan el enemigo vuelve a su posicion inicial   
        if ataque.rect.colliderect(enemigo.rect):
            ataques.remove(ataque) 
            enemigo.rect.x = width   
            enemigo.rect.y = player.shape.y -120
            
    
      #
    x_relativa = x % screen.get_rect().width
    screen.blit(paisaje, [x_relativa - screen.get_rect().width, 0])
    if x_relativa < width:
        screen.blit(paisaje, (x_relativa, 0))
    x -= 1

    #aqui dibujamos nuestros jugadores en pantalla
    player.draw(screen)
    enemigo.update()
    enemigo.draw(screen)

   
    for ataque in ataques:
        ataque.draw(screen)

    pygame.display.flip()

pygame.quit()


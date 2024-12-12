import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dino Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Configuración del jugador
player_width = 50
player_height = 50
player_x = 50
player_y = height - player_height - 10
player_velocity = 10
is_jumping = True
jump_count = 10

# Configuración de los obstáculos
obstacle_width = 20
obstacle_height = 50
obstacle_velocity = 5
obstacle_gap = 100

# Fuente para el texto
font = pygame.font.SysFont('Arial', 30)

# Función para dibujar el jugador
def draw_player(y):
    pygame.draw.rect(screen, BLACK, (player_x, y, player_width, player_height))

# Función para dibujar los obstáculos
def draw_obstacle(x):
    pygame.draw.rect(screen, GREEN, (x, height - obstacle_height - 10, obstacle_width, obstacle_height))

# Función para mostrar el puntaje
def show_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Juego principal
def game():
    global player_y, is_jumping, jump_count
    obstacle_x = width
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador (salto)
        if is_jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = True
                jump_count = 10
        else:
            if player_y < height - player_height - 10:
                player_y += 5

        # Movimiento del obstáculo
        obstacle_x -= obstacle_velocity
        if obstacle_x < 0:
            obstacle_x = width
            score += 1

        # Colisiones con obstáculos
        if player_x + player_width > obstacle_x and player_x < obstacle_x + obstacle_width:
            if player_y + player_height > height - obstacle_height - 10:
                running = False

        # Dibuja el jugador y el obstáculo
        draw_player(player_y)
        draw_obstacle(obstacle_x)

        # Mostrar puntaje
        show_score(score)

        # Actualizar la pantalla
        pygame.display.update()

        # Controlar la velocidad del juego
        clock.tick(30)

    pygame.quit()

# Control de salto
def handle_input():
    global is_jumping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True

# Función principal
def main():
    while True:
        handle_input()
        game()

if __name__ == "__main__":
    main()

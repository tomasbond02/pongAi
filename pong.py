import pygame

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Dimensiones de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Clase para las paletas
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Clase para la pelota
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = 5
        self.y_speed = 5

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # Rebote en los bordes superior e inferior
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.y_speed *= -1

# Crear paletas
paddle_width = 15
paddle_height = 100
paddle_speed = 5  # Velocidad de movimiento de las paletas
left_paddle = Paddle(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)
right_paddle = Paddle(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)

# Crear pelota
ball_radius = 10
ball = Ball(screen_width // 2, screen_height // 2, ball_radius, WHITE)

# Puntuación
left_score = 0
right_score = 0
font = pygame.font.Font(None, 36)

# Función para mostrar la puntuación en pantalla
def show_score(screen):
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (screen_width // 4, 10))
    screen.blit(right_score_text, (3 * screen_width // 4, 10))

# Bucle principal del juego
running = True
while running:
    # Manejar eventos (movimiento de paletas)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.y > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.y < screen_height - left_paddle.height:
        left_paddle.y += paddle_speed
    if keys[pygame.K_UP] and right_paddle.y > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.y < screen_height - right_paddle.height:
        right_paddle.y += paddle_speed

    # Lógica del juego
    ball.move()

    # Rebote en las paletas
    if ball.x - ball.radius <= left_paddle.x + left_paddle.width and \
       ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
        ball.x_speed *= -1
    elif ball.x + ball.radius >= right_paddle.x and \
         ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
        ball.x_speed *= -1

    # Puntuación y fin del juego
    if ball.x - ball.radius <= 0:
        right_score += 1
        ball.x = screen_width // 2
        ball.y = screen_height // 2
    elif ball.x + ball.radius >= screen_width:
        left_score += 1
        ball.x = screen_width // 2
        ball.y = screen_height // 2

    # Verificar si alguien ganó (puedes establecer un puntaje máximo)
    if left_score >= 10 or right_score >= 10:
        running = False

    # Dibujar elementos en la pantalla
    screen.fill(BLACK)
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)
    show_score(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar la velocidad de fotogramas
    clock.tick(60)

# Salir de Pygame
pygame.quit()

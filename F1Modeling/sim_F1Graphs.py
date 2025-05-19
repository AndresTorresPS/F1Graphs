import pygame
import math

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_RADIUS = 10
TRACK_RADIUS = 200
CENTER = (WIDTH // 2, HEIGHT // 2)
LAPS_TOTAL = 3
PIT_STOP_LAP = 2

# Colores
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Carrera 2D")
clock = pygame.time.Clock()

# Estado del coche
angle = 0
speed = 0.02
lap = 1
pit_done = False
tire_type = "Soft"

# Fuente
font = pygame.font.SysFont("Arial", 24)

def draw_track():
    pygame.draw.circle(screen, GRAY, CENTER, TRACK_RADIUS, 5)
    pygame.draw.rect(screen, GREEN, (CENTER[0] + TRACK_RADIUS + 20, CENTER[1] - 40, 60, 80), 2)
    pit_text = font.render("PIT", True, GREEN)
    screen.blit(pit_text, (CENTER[0] + TRACK_RADIUS + 30, CENTER[1] - 30))

def draw_car(x, y):
    color = RED if tire_type == "Soft" else BLUE
    pygame.draw.circle(screen, color, (int(x), int(y)), CAR_RADIUS)

def draw_status():
    text = f"Lap: {lap}/{LAPS_TOTAL} | Tire: {tire_type} | Pit: {'Yes' if pit_done else 'No'}"
    screen.blit(font.render(text, True, WHITE), (10, 10))

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    draw_track()

    # Movimiento del coche
    x = CENTER[0] + TRACK_RADIUS * math.cos(angle)
    y = CENTER[1] + TRACK_RADIUS * math.sin(angle)
    draw_car(x, y)

    # Paso por línea de meta
    if angle >= 2 * math.pi:
        angle = 0
        lap += 1
        if lap > LAPS_TOTAL:
            running = False

    # Parada en pits (una vez)
    if lap == PIT_STOP_LAP and not pit_done and 0.45 < angle < 0.55:
        tire_type = "Medium"
        pit_done = True

    draw_status()
    angle += speed
    pygame.display.flip()
    clock.tick(FPS)

# Pantalla final
screen.fill(BLACK)
final_text = font.render("¡Carrera terminada!", True, WHITE)
screen.blit(final_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()

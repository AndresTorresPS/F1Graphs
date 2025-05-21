import pandas as pd
import math
import pygame

# Inicializa los recursos de pygame una sola vez
pygame.init()

class Constants:
    # Configuraciones de la pantalla
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    CENTER = (WIDTH // 2, HEIGHT // 2)

    # Dimensiones
    CAR_RADIUS = 10
    TRACK_RADIUS = 200
    
    # Colores
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    GREEN = (0, 200, 0)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    YELLOW = (255, 255, 0)
    COMPOUND_COLORS = {
        "Soft": RED,
        "Medium": YELLOW,
        "Hard": WHITE,
    }

    # Textos
    FONT = "Cambria"
    H1 = pygame.font.SysFont(FONT, 22, bold=1) 
    H2 = pygame.font.SysFont(FONT, 16, bold=1)
    BODY = pygame.font.SysFont(FONT, 14)
    PIT_STR = "PIT"
    END_STR = "End of F1 2D-Simulation"
    SUB_END_STR = "Results were saved in F1Results/"

class Car:
    def __init__(self, tire_order, pit_lap, car_id):
        self.tire_order = tire_order
        self.pit_lap = pit_lap
        self.car_id = car_id
        
        lap_times = {
            "lap_time": {
                "Soft": 6,
                "Medium": 6.5,
                "Hard": 7
            }
        }

        self.lap_times_pd = pd.DataFrame(lap_times)
        self.pit_stop_time = 2
        self.tire_idx = 0
        self.tire_type = self.tire_order[self.tire_idx]
        self.angle = 0.1
        self.lap = 1
        self.pit_done = 0
        self.speed = self.get_speed_for_tire(self.tire_type)
        self.in_pit_stop = False
        self.pit_stop_timer = 0

    def get_speed_for_tire(self, tire):
        lap_time = self.lap_times_pd.loc[tire, "lap_time"]
        return (2 * math.pi) / (lap_time * Constants.FPS)

    def update_tire(self):
        self.tire_idx = min(self.tire_idx + 1, len(self.tire_order) - 1)
        self.tire_type = self.tire_order[self.tire_idx]
        self.speed = self.get_speed_for_tire(self.tire_type)

    def draw_car(self, screen):
        angle = self.angle + math.pi / 2
        size = Constants.CAR_RADIUS * 2
        x = Constants.CENTER[0] + Constants.TRACK_RADIUS * math.cos(self.angle)
        y = Constants.CENTER[1] + Constants.TRACK_RADIUS * math.sin(self.angle)
        tip = (
            int(x + size * math.cos(angle)),
            int(y + size * math.sin(angle))
        )
        back_left = (
            int(x + Constants.CAR_RADIUS * math.cos(angle + 2.5)),
            int(y + Constants.CAR_RADIUS * math.sin(angle + 2.5))
        )
        back_right = (
            int(x + Constants.CAR_RADIUS * math.cos(angle - 2.5)),
            int(y + Constants.CAR_RADIUS * math.sin(angle - 2.5))
        )
        pygame.draw.polygon(screen, Constants.COMPOUND_COLORS[self.tire_type], [tip, back_left, back_right])
        # Draw car id above the car
        id_text = Constants.BODY.render(str(self.car_id), True, (255, 255, 0))
        screen.blit(id_text, (int(x) - 10, int(y) - 30))

    def update_lap(self, laps_total):
        if self.angle >= 2 * math.pi:
            self.angle = 0
            self.lap += 1
            if self.lap > laps_total:
                self.lap = laps_total + 1  # Mark as finished

    def start_pit_stop(self):
        self.in_pit_stop = True
        self.pit_stop_timer = int(self.pit_stop_time * Constants.FPS)

    def finish_pit_stop(self):
        self.in_pit_stop = False
        self.pit_done += 1
        self.update_tire()

    def handle_pit_stop_logic(self, laps_total, pit_stops_required):
        if self.lap > laps_total:
            return  # Finished
        if self.in_pit_stop:
            self.pit_stop_timer -= 1
            if self.pit_stop_timer <= 0:
                self.finish_pit_stop()
        else:
            self.update_lap(laps_total)
            # Pit stop logic
            if (self.pit_done < pit_stops_required and
                self.lap == self.pit_lap and
                math.pi * 1.95 < self.angle < math.pi * 1.99):
                self.start_pit_stop()
            else:
                self.angle += self.speed

class Track:
    def __init__(self, name, pit_font):
        self.name = name
        self.pit_font = pit_font

    def draw_track(self, screen):
        if self.name == "Circle":
            pygame.draw.circle(screen, Constants.GRAY, Constants.CENTER, Constants.TRACK_RADIUS, 5)
            pygame.draw.rect(
                screen, Constants.GREEN,
                (Constants.CENTER[0] + Constants.TRACK_RADIUS + 20, Constants.CENTER[1] - 40, 60, 80), 2
            )
            pit_text = self.pit_font.render(Constants.PIT_STR, True, Constants.GREEN)
            screen.blit(pit_text, (Constants.CENTER[0] + Constants.TRACK_RADIUS + 30, Constants.CENTER[1] - 30))

class Renderer:
    pass
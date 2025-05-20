import math
import pygame

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
    END_STR = "End of F1 2D-Simulation"
    SUB_END_STR = "Results where saved in F1Results/"

class Car:
    def __init__(self, tire_order, pit_lap, car_id, lap_times_pd, fps, car_radius, color_map, pit_stop_time):
        self.tire_order = tire_order
        self.pit_lap = pit_lap
        self.car_id = car_id
        self.lap_times_pd = lap_times_pd
        self.fps = fps
        self.car_radius = car_radius
        self.color_map = color_map
        self.pit_stop_time = pit_stop_time

        self.tire_idx = 0
        self.tire_type = self.tire_order[self.tire_idx]
        self.angle = 0
        self.lap = 1
        self.pit_done = 0
        self.speed = self.get_speed_for_tire(self.tire_type)
        self.in_pit_stop = False
        self.pit_stop_timer = 0

    def get_speed_for_tire(self, tire):
        lap_time = self.lap_times_pd.loc[tire, "lap_time"]
        return (2 * math.pi) / (lap_time * self.fps)

    def update_tire(self):
        self.tire_idx = min(self.tire_idx + 1, len(self.tire_order) - 1)
        self.tire_type = self.tire_order[self.tire_idx]
        self.speed = self.get_speed_for_tire(self.tire_type)

    def draw(self, screen, center, track_radius, font):
        angle = self.angle + math.pi / 2
        size = self.car_radius * 2
        x = center[0] + track_radius * math.cos(self.angle)
        y = center[1] + track_radius * math.sin(self.angle)
        tip = (
            int(x + size * math.cos(angle)),
            int(y + size * math.sin(angle))
        )
        back_left = (
            int(x + self.car_radius * math.cos(angle + 2.5)),
            int(y + self.car_radius * math.sin(angle + 2.5))
        )
        back_right = (
            int(x + self.car_radius * math.cos(angle - 2.5)),
            int(y + self.car_radius * math.sin(angle - 2.5))
        )
        pygame.draw.polygon(screen, self.color_map[self.tire_type], [tip, back_left, back_right])
        # Draw car id above the car
        id_text = font.render(str(self.car_id), True, (255, 255, 0))
        screen.blit(id_text, (int(x) - 10, int(y) - 30))


import pygame
import math
import pandas as pd

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

class F1RaceSim:
    def __init__(self, laps_total, pit_stops_required, lap_times_pd, pit_stop_time, cars_params):
        pygame.init()
        # Global parameters
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.CAR_RADIUS = 10
        self.TRACK_RADIUS = 200
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.COLORS = {
            "Soft": (200, 0, 0),
            "Medium": (0, 0, 255),
            "Hard": (255, 255, 255)
        }
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.GREEN = (0, 200, 0)
        self.BLACK = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("F1Graphs")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.laps_total = laps_total
        self.pit_stops_required = pit_stops_required
        self.pit_stop_time = pit_stop_time
        self.lap_times_pd = lap_times_pd
        self.running = True

        # Create cars
        self.cars = []
        for idx, car_param in enumerate(cars_params):
            # Distribute initial angles so cars don't overlap
            car = Car(
                tire_order=car_param["tire_order"],
                pit_lap=car_param["pit_lap"],
                car_id=car_param["id"],
                lap_times_pd=self.lap_times_pd,
                fps=self.FPS,
                car_radius=self.CAR_RADIUS,
                color_map=self.COLORS,
                pit_stop_time=self.pit_stop_time
            )
            self.cars.append(car)

    def draw_track(self):
        pygame.draw.circle(self.screen, self.GRAY, self.CENTER, self.TRACK_RADIUS, 5)
        pygame.draw.rect(
            self.screen, self.GREEN,
            (self.CENTER[0] + self.TRACK_RADIUS + 20, self.CENTER[1] - 40, 60, 80), 2
        )
        pit_text = self.font.render("PIT", True, self.GREEN)
        self.screen.blit(pit_text, (self.CENTER[0] + self.TRACK_RADIUS + 30, self.CENTER[1] - 30))

    def draw_status(self):
        y = 10
        for car in self.cars:
            text = f"Car {car.car_id} | Lap: {car.lap}/{self.laps_total} | Tire: {car.tire_type} | Pit: {car.pit_done}/{self.pit_stops_required}"
            self.screen.blit(self.font.render(text, True, self.WHITE), (10, y))
            if car.in_pit_stop:
                pit_text = self.font.render(f"En PIT: {car.pit_stop_timer // self.FPS + 1}s", True, self.GREEN)
                self.screen.blit(pit_text, (400, y))
            y += 30

    def pit_stop(self, car):
        car.in_pit_stop = True
        car.pit_stop_timer = int(self.pit_stop_time * self.FPS)

    def finish_pit_stop(self, car):
        car.in_pit_stop = False
        car.pit_done += 1
        car.update_tire()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_lap(self, car):
        if car.angle >= 2 * math.pi:
            car.angle = 0
            car.lap += 1
            if car.lap > self.laps_total:
                car.lap = self.laps_total + 1  # Mark as finished

    def handle_pit_stop_logic(self, car):
        if car.lap > self.laps_total:
            return  # Finished
        if car.in_pit_stop:
            car.pit_stop_timer -= 1
            if car.pit_stop_timer <= 0:
                self.finish_pit_stop(car)
        else:
            self.update_lap(car)
            # Pit stop logic
            if (car.pit_done < self.pit_stops_required and
                car.lap == car.pit_lap and
                math.pi * 1.95 < car.angle < math.pi * 1.99):
                self.pit_stop(car)
            else:
                car.angle += car.speed

    def show_final_screen(self):
        self.screen.fill(self.BLACK)
        final_text = self.font.render("¡Carrera terminada!", True, self.WHITE)
        self.screen.blit(final_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(self.BLACK)
            self.draw_track()
            for car in self.cars:
                car.draw(self.screen, self.CENTER, self.TRACK_RADIUS, self.font)
                self.handle_pit_stop_logic(car)
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            # End simulation when all cars finished
            if all(car.lap > self.laps_total for car in self.cars):
                self.running = False
        self.show_final_screen()

if __name__ == "__main__":
    data = {
        "lap_time": {
            "Soft": 6,
            "Medium": 6.5,
            "Hard": 7
        }
    }

    lap_times_pd = pd.DataFrame(data)
    laps_total = 3
    pit_stops_required = 1
    pit_stop_time = 2

    # User provides car parameters
    cars_params = [
        {"tire_order": ["Soft", "Medium"], "pit_lap": 1, "id": 1},
        {"tire_order": ["Medium", "Soft"], "pit_lap": 1, "id": 2}, # Gana
        {"tire_order": ["Soft", "Medium"], "pit_lap": 2, "id": 3}, # Gana
        {"tire_order": ["Medium", "Soft"], "pit_lap": 2, "id": 4},
    ]

    sim = F1RaceSim(
        laps_total=laps_total,
        pit_stops_required=pit_stops_required,
        lap_times_pd=lap_times_pd,
        pit_stop_time=pit_stop_time,
        cars_params=cars_params
    )
    sim.run()

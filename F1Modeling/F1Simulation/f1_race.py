import pygame
import math
import pandas as pd
from F1Utils.race_utils import Constants, Car

# Incicialza los recursos de pygame una sola vez
pygame.init()

class F1Race():

    # Variables de clase
    H1 = pygame.font.SysFont(Constants.FONT, 22, bold=1) 
    H2 = pygame.font.SysFont(Constants.FONT, 16, bold=1)
    BODY = pygame.font.SysFont(Constants.FONT, 14)
    pygame.display.set_caption("F1 2D-Simulator")

    def __init__(self, laps_total, pit_stops_required, lap_times_pd, pit_stop_time, cars_params):
        
        # Configuraciones de la instancia
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.clock = pygame.time.Clock()

        self.laps_total = laps_total                    # Total de vueltas
        self.pit_stops_required = pit_stops_required    # Total de paradas en boxes requeridas
        self.pit_stop_time = pit_stop_time              # Tiempo de parada en boxes (debe ser de Car)
        self.lap_times_pd = lap_times_pd                # DataFrame con tiempos de vuelta por compuesto (debe ser de Car)
        self.running = True                             # Variable para controlar el bucle principal    

        # Create cars
        self.cars = []
        for idx, car_param in enumerate(cars_params):
            # Distribute initial angles so cars don't overlap
            car = Car(
                tire_order=car_param["tire_order"],
                pit_lap=car_param["pit_lap"],
                car_id=car_param["id"],
                lap_times_pd=self.lap_times_pd,
                fps=Constants.FPS,
                car_radius=Constants.CAR_RADIUS,
                color_map=Constants.COMPOUND_COLORS,
                pit_stop_time=self.pit_stop_time
            )
            self.cars.append(car)

    def draw_track(self):
        pygame.draw.circle(self.screen, Constants.GRAY, Constants.CENTER, Constants.TRACK_RADIUS, 5)
        pygame.draw.rect(
            self.screen, Constants.GREEN,
            (Constants.CENTER[0] + Constants.TRACK_RADIUS + 20, Constants.CENTER[1] - 40, 60, 80), 2
        )
        pit_text = F1Race.H2.render("PIT", True, Constants.GREEN)
        self.screen.blit(pit_text, (Constants.CENTER[0] + Constants.TRACK_RADIUS + 30, Constants.CENTER[1] - 30))

    def draw_status(self):
        y = 10
        for car in self.cars:
            text = f"Car {car.car_id} | Lap: {car.lap}/{self.laps_total} | Tire: {car.tire_type} | Pit: {car.pit_done}/{self.pit_stops_required}"
            self.screen.blit(F1Race.BODY.render(text, True, Constants.WHITE), (10, y))
            if car.in_pit_stop:
                pit_text = F1Race.BODY.render(f"En PIT: {car.pit_stop_timer // Constants.FPS + 1}s", True, Constants.GREEN)
                self.screen.blit(pit_text, (300, y))
            y += 30

    def pit_stop(self, car):
        car.in_pit_stop = True
        car.pit_stop_timer = int(self.pit_stop_time * Constants.FPS)

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
        self.screen.fill(Constants.BLACK)
        end_text = F1Race.H1.render(Constants.END_STR, True, Constants.WHITE)
        self.screen.blit(end_text, (Constants.WIDTH // 2 - 300, Constants.HEIGHT // 2 - 20))
        sub_end_text = F1Race.BODY.render(Constants.SUB_END_STR, True, Constants.WHITE)
        self.screen.blit(sub_end_text, (Constants.WIDTH // 2 - 300, Constants.HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(Constants.BLACK)
            self.draw_track()
            for car in self.cars:
                car.draw(self.screen, Constants.CENTER, Constants.TRACK_RADIUS, F1Race.BODY)
                self.handle_pit_stop_logic(car)
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(Constants.FPS)
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

    sim = F1Race(
        laps_total=laps_total,
        pit_stops_required=pit_stops_required,
        lap_times_pd=lap_times_pd,
        pit_stop_time=pit_stop_time,
        cars_params=cars_params
    )
    sim.run()

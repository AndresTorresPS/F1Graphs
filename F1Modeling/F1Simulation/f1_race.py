import pygame
import math
import pandas as pd
from F1Utils.race_utils import Constants, Car, Track

class F1Race():

    def __init__(self, laps_total, pit_stops_required, cars_params):
        
        # Configuraciones de la simulación
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        pygame.display.set_caption("F1 2D-Simulator")
        self.clock = pygame.time.Clock()
        self.track = Track("Circle", Constants.H2)
        
        # Configuraciones de la carrera
        self.laps_total = laps_total                    # Total de vueltas
        self.pit_stops_required = pit_stops_required    # Total de paradas en boxes requeridas
        self.running = True                             # Variable para controlar el bucle principal    

        # Create cars
        self.cars = []
        for idx, car_param in enumerate(cars_params):
            # Distribute initial angles so cars don't overlap
            car = Car(
                tire_order=car_param["tire_order"],
                pit_lap=car_param["pit_lap"],
                car_id=car_param["id"]
            )
            self.cars.append(car)

    def draw_status(self):
        y = 10
        for car in self.cars:
            text = f"Car {car.car_id} | Lap: {car.lap}/{self.laps_total} | Tire: {car.tire_type} | Pit: {car.pit_done}/{self.pit_stops_required}"
            self.screen.blit(Constants.BODY.render(text, True, Constants.WHITE), (10, y))
            if car.in_pit_stop:
                pit_text = Constants.BODY.render(f"En PIT: {car.pit_stop_timer // Constants.FPS + 1}s", True, Constants.GREEN)
                self.screen.blit(pit_text, (300, y))
            y += 30

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def show_final_screen(self):
        self.screen.fill(Constants.BLACK)
        end_text = Constants.H1.render(Constants.END_STR, True, Constants.WHITE)
        self.screen.blit(end_text, (Constants.WIDTH // 2 - 300, Constants.HEIGHT // 2 - 20))
        sub_end_text = Constants.BODY.render(Constants.SUB_END_STR, True, Constants.WHITE)
        self.screen.blit(sub_end_text, (Constants.WIDTH // 2 - 300, Constants.HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(Constants.BLACK)
            self.track.draw_track(self.screen)
            for car in self.cars:
                car.draw_car(self.screen)
                car.handle_pit_stop_logic(self.laps_total, self.pit_stops_required)
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(Constants.FPS)
            # End simulation when all cars finished
            if all(car.lap > self.laps_total for car in self.cars):
                self.running = False
        self.show_final_screen()

if __name__ == "__main__":
    
    laps_total = 3
    pit_stops_required = 1

    # User provides car parameters
    cars_params = [
        {"tire_order": ["Soft", "Medium"], "pit_lap": 1, "id": 1}, 
        {"tire_order": ["Medium", "Soft"], "pit_lap": 1, "id": 2}, # Gana
        {"tire_order": ["Soft", "Medium"], "pit_lap": 2, "id": 3}, # Gana
        {"tire_order": ["Medium", "Soft"], "pit_lap": 2, "id": 4}
    ]

    sim = F1Race(
        laps_total=laps_total,
        pit_stops_required=pit_stops_required,
        cars_params=cars_params
    )
    sim.run()

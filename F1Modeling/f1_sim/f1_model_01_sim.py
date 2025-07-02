import os
import time
import pandas as pd
import pygame
from f1_sim.f1_sim_utils.sim_utils import Constants, Car, Track

class F1Race():
    """
    Clase principal para la simulación de una carrera de F1 en 2D.
    """

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
        self.start_time = time.time()
        
        # Asignar el start_time a cada carro y crear variables auxiliares
        for car in self.cars:
            car.start_time = self.start_time
            car.lap_times = {}
            car.last_lap_logged = 0

        while self.running:
            self.handle_events()
            self.screen.fill(Constants.BLACK)
            self.track.draw_track(self.screen)

            for car in self.cars:
                car.draw_car(self.screen)
                car.handle_pit_stop_logic(self.laps_total, self.pit_stops_required)

                # ✅ Verifica si el carro ha cambiado de vuelta
                if car.lap > car.last_lap_logged:
                    lap_time = round(time.time() - self.start_time, 2)
                    lap_number = car.lap - 1
                    car.lap_times[lap_number] = lap_time
                    car.last_lap_logged = car.lap
                    print(f"🏁 Car {car.car_id} completó la vuelta {lap_number} en t={lap_time}s desde inicio")

            self.draw_status()
            pygame.display.flip()
            self.clock.tick(Constants.FPS)

            if all(car.lap > self.laps_total for car in self.cars):
                self.running = False

        total_time = round(time.time() - self.start_time, 2)

        # Determinar el carro que terminó primero (menor tiempo de última vuelta)
        finished_cars = [(car.car_id, car.lap_times.get(self.laps_total)) for car in self.cars]
        finished_cars = [(cid, t) for cid, t in finished_cars if t is not None]
        winner_id = min(finished_cars, key=lambda x: x[1])[0] if finished_cars else "Desconocido"

        # Crear carpeta si no existe
        output_dir = "f1_output/sim_models"
        os.makedirs(output_dir, exist_ok=True)

        # Guardar resumen de resultados
        summary_path = os.path.join(output_dir, "f1_model_01_sim_optimal_solution.csv")
        summary_df = pd.DataFrame([{
            "Optimal Solution (Car ID)": winner_id,
            "Total Simulation Time (s)": total_time
        }])
        summary_df.to_csv(summary_path, index=False)
        print(f"✅ Resultados guardados en {summary_path}")

        # Guardar tiempos por vuelta
        lap_data = []
        for car in self.cars:
            for lap_number, time_s in car.lap_times.items():
                lap_data.append({
                    "car_id": car.car_id,
                    "lap": lap_number,
                    "time_s": time_s
                })

        lap_df = pd.DataFrame(lap_data)
        lap_times_path = os.path.join(output_dir, "f1_model_01_sim_lap_times.csv")
        lap_df.to_csv(lap_times_path, index=False)
        print(f"✅ Tiempos por vuelta guardados en {lap_times_path}")

        self.show_final_screen()

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

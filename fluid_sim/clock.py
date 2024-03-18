import datetime

from fluid_sim import SIM_DT


class Clock:

    def __init__(self):
        self.elapsed_time: float = 0.0
        self.elapsed_fixed_time: float = 0.0

        self.elapsed_ticks: int = 0
        self.elapsed_fixed_ticks: int = 0

        self.delta_time: float = 0.0

        self._creation_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    def tick(self, dt: float):
        self.elapsed_ticks += 1
        self.elapsed_time += dt
        self.delta_time = dt

    def fixed_tick(self):
        self.elapsed_fixed_ticks += 1
        self.elapsed_fixed_time += SIM_DT

    @property
    def comp_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    @property
    def create_time(self):
        return self._creation_time

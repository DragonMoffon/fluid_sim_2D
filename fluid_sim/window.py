from arcade import Window

from fluid_sim import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SIM_WIDTH, SIM_HEIGHT, SIM_DT, SIM_NAME
from fluid_sim.clock import Clock
from fluid_sim.lib import SimBase


class SimWindow(Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, f"2D CFD [{SIM_WIDTH}, {SIM_HEIGHT}] {SIM_NAME}", fullscreen=FULLSCREEN,
                         gl_version=(4, 3))
        self.register_event_type('on_fixed_update')

        self._clock: Clock = Clock()
        self._accumulated_time: float = 0.0
        self._excess_fraction: float = 0.0

        self._sim: SimBase = SimBase.create_sim(SIM_NAME)

    @property
    def clock(self):
        return self._clock

    def _dispatch_updates(self, delta_time: float):
        self._accumulated_time += delta_time
        while self._accumulated_time >= SIM_DT:
            self._clock.fixed_tick()
            self.dispatch_event('on_fixed_update', SIM_DT)
            self._accumulated_time -= SIM_DT
        self._excess_fraction = self._accumulated_time / SIM_DT

        self._clock.tick(delta_time)
        self.dispatch_event('on_update', delta_time)

    def on_update(self, delta_time: float):
        self._sim.render()

    def on_fixed_update(self, delta_time: float):
        self._sim.update()

    def on_draw(self):
        self.clear()
        self._sim.draw()
        self.draw_ui()

    def draw_ui(self):
        pass

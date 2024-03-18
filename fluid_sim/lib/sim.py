"""
Base simulation class. Is inherited by every type of unique simulation
"""
from arcade import get_window

from fluid_sim.lib.sim_shader import SimShaderBase
from fluid_sim.lib.sim_renderer import SimRendererBase


class SimBase:

    def __init__(self, shader: SimShaderBase, renderer: SimRendererBase):
        self._win = get_window()
        self._clk = self._win.clock

        self._shader: SimShaderBase = shader
        self._renderer: SimRendererBase = renderer

    @staticmethod
    def name():
        raise NotImplementedError()

    @staticmethod
    def create_sim(name: str):
        print({child.name(): child for child in SimBase.__subclasses__()})
        cls = {child.name(): child for child in SimBase.__subclasses__()}[name]
        return cls()

    @staticmethod
    def children_set():
        return set(child.name() for child in SimBase.__subclasses__())

    def draw(self):
        self._renderer.draw()

    def render(self):
        self._renderer.render()

    def update(self):
        self._shader.update()

    def save_screenshot(self):
        self._renderer.screen_shot()

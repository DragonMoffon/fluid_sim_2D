"""
Base renderer class for the simulation
"""

from PIL import Image

import arcade.gl as gl
from arcade import get_window, ArcadeContext
from arcade.resources import get_resource_handle_paths

from fluid_sim import SIM_WIDTH, SIM_HEIGHT, SMOOTH
from fluid_sim.clock import Clock


class SimRendererBase:

    def __init__(self):
        win = get_window()
        self._clk: Clock = win.clock
        self._ctx: ArcadeContext = win.ctx

        self._texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, SIM_HEIGHT),
            filter=(
                gl.LINEAR if SMOOTH else gl.NEAREST,
                gl.LINEAR if SMOOTH else gl.NEAREST
            )
        )
        self._framebuffer: gl.Framebuffer = self._ctx.framebuffer(
            color_attachments=[
                self._texture
            ]
        )

        self._draw_geo = gl.geometry.quad_2d_fs()
        self._draw_prog = self._ctx.load_program(
            vertex_shader=":s:sim_draw_vs.glsl",
            fragment_shader=":s:sim_draw_fs.glsl"
        )

    def __str__(self):
        raise NotImplementedError()

    def render(self):
        with self._framebuffer.activate() as fbo:
            fbo.clear()
            self._on_render()

    def _on_render(self):
        raise NotImplementedError()

    def draw(self):
        self._texture.use(0)
        self._draw_geo.render(self._draw_prog)

    def screen_shot(self):
        img = Image.frombuffer("RGBA", (SIM_WIDTH, SIM_HEIGHT), self._texture.read())
        pth = get_resource_handle_paths("l")[0]
        img.save(
            f"{str(pth)}/screenshot"
            f"_{str(self)}"
            f"_{self._clk.elapsed_fixed_time}"
            f"_{self._clk.elapsed_fixed_time}"
            f"_{self._clk.comp_time}"
            f".png"
        )

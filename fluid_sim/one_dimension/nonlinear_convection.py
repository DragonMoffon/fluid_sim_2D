"""
Non-Linear Convection equation is a very simple equation which describes the propagation of a wave over time with
a non-linear dependence on the speed u.

To run this simulation call "python -m fluid_sim --nonlinear-convection" in the terminal.
"""
import struct
from array import array

import arcade.gl as gl
from arcade import get_window, ArcadeContext

from fluid_sim import SIM_WIDTH, SIM_DT, SIM_DP
from fluid_sim.lib.sim import SimBase, SimRendererBase, SimShaderBase


class SimShaderLinearConvection(SimShaderBase):

    def __init__(self):
        win = get_window()
        self._ctx: ArcadeContext = win.ctx

        self._comp_shader: gl.ComputeShader = self._ctx.load_compute_shader(
            ":s:one_dimension/nonlinear_convection_cs.glsl"
        )

        self._sim_data: gl.Buffer = self._ctx.buffer(
            data=struct.pack("fff", SIM_DT, SIM_DP, SIM_DT/SIM_DP)
        )

        self._write_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="f4",
            data=array("f", (2.0 if 200 <= i <= 350 else 1.0 for i in range(SIM_WIDTH)))
        )
        self._read_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="f4",
            data=array("f", (2.0 if 200 <= i <= 350 else 1.0 for i in range(SIM_WIDTH)))
            )

    @property
    def active_texture(self):
        return self._write_u_texture

    def _flip(self):
        self._write_u_texture, self._read_u_texture = self._read_u_texture, self._write_u_texture

    def _calculate(self):
        self._read_u_texture.bind_to_image(0, read=True, write=False)
        self._write_u_texture.bind_to_image(1, read=False, write=True)
        self._sim_data.bind_to_storage_buffer(binding=0)
        self._comp_shader.run(group_x=SIM_WIDTH)


class SimRendererLinearConvection(SimRendererBase):

    def __init__(self, shader: SimShaderLinearConvection):
        super().__init__()

        self._shader: SimShaderLinearConvection = shader

        self._render_prog: gl.Program = self._ctx.load_program(
            vertex_shader=":s:sim_draw_vs.glsl",
            fragment_shader=":s:one_dimension/convection_render_fs.glsl"
        )

    def __str__(self):
        return "non-linear-convection-1d"

    def _on_render(self):
        self._shader.active_texture.use(0)
        self._draw_geo.render(self._render_prog)


class SimLinearConvection(SimBase):

    def __init__(self):
        shader: SimShaderLinearConvection = SimShaderLinearConvection()
        renderer: SimRendererLinearConvection = SimRendererLinearConvection(shader)

        super().__init__(shader, renderer)

    @staticmethod
    def name():
        return "nonlinear-convection"

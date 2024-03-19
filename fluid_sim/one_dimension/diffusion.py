"""
Diffusion is the second part of the navier stokes equation along with convection. It is a double order derivative
which makes the integration more complicated. To do the integration a taylor series has been used. Due to the
small size of the components at x^4 and above they have been ignored to simplify the final equation.

To run this simulation call "python -m fluid_sim --diffusion-1d" in the terminal.
"""
import struct
from array import array
from PIL import Image

import arcade.gl as gl
from arcade import get_window, ArcadeContext
from arcade.resources import resolve

from fluid_sim import SIM_WIDTH, SIM_DT, SIM_DP, SIM_MU, RENDER_MODE_1D, RENDER_MODES_1D
from fluid_sim.lib.sim import SimBase, SimRendererBase, SimShaderBase


class SimShaderDiffusion_1d(SimShaderBase):

    def __init__(self):
        win = get_window()
        self._ctx: ArcadeContext = win.ctx

        self._comp_shader: gl.ComputeShader = self._ctx.load_compute_shader(
            ":s:one_dimension/diffusion_cs.glsl"
        )

        DT = 0.2 * SIM_DP**2 / SIM_MU
        self._sim_data: gl.Buffer = self._ctx.buffer(
            data=struct.pack("ffff", DT, SIM_DP, SIM_MU, (DT / SIM_DP**2.0))
        )

        p_start = max(1, int(0.2 * SIM_WIDTH))
        p_end = max(1, int(0.35 * SIM_WIDTH))

        self._write_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="f4",
            data=array("f", (2.0 if p_start <= i <= p_end else 1.0 for i in range(SIM_WIDTH)))
        )

        self._read_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="f4",
            data=array("f", (2.0 if p_start <= i <= p_end else 1.0 for i in range(SIM_WIDTH)))
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


class SimRendererDiffusion_1d_gradient(SimRendererBase):

    def __init__(self, shader: SimShaderDiffusion_1d):
        super().__init__()

        self._shader: SimShaderDiffusion_1d = shader

        img = Image.open(resolve(":r:blue_red_ramp.png"))
        self._gradient_map_texture: gl.Texture2D = self._ctx.texture(
            size=img.size,
            filter=(gl.NEAREST, gl.NEAREST),
            wrap_x=gl.CLAMP_TO_EDGE,
            wrap_y=gl.REPEAT,
            data=img.tobytes()
        )

        self._render_prog: gl.Program = self._ctx.load_program(
            vertex_shader=":s:sim_draw_vs.glsl",
            fragment_shader=":s:one_dimension/1d_gradient_map_render_fs.glsl"
        )
        self._render_prog["texture_0"] = 0
        self._render_prog["colour_ramp_0"] = 1
        self._render_prog["max_value"] = 2.0

    def __str__(self):
        return "diffusion-1d_gradient"

    def _on_render(self):
        self._shader.active_texture.use(0)
        self._gradient_map_texture.use(1)
        self._draw_geo.render(self._render_prog)


class SimRendererDiffusion_1d_graph(SimRendererBase):

    def __init__(self, shader: SimShaderDiffusion_1d):
        super().__init__()

        self._shader: SimShaderDiffusion_1d = shader

        self._render_prog: gl.Program = self._ctx.load_program(
            vertex_shader=":s:sim_draw_vs.glsl",
            fragment_shader=":s:one_dimension/1d_graph_render_fs.glsl"
        )
        self._render_prog["texture_0"] = 0
        self._render_prog["max_value"] = 2.0

    def __str__(self):
        return "diffusion-1d_graph"

    def _on_render(self):
        self._shader.active_texture.use(0)
        self._draw_geo.render(self._render_prog)


class SimDiffusion_1d(SimBase):

    def __init__(self):
        shader: SimShaderDiffusion_1d = SimShaderDiffusion_1d()
        match RENDER_MODE_1D:
            case RENDER_MODES_1D.gradient_1d:
                renderer: SimRendererDiffusion_1d_gradient = SimRendererDiffusion_1d_gradient(shader)
            case RENDER_MODES_1D.graph_1d:
                renderer: SimRendererDiffusion_1d_graph = SimRendererDiffusion_1d_graph(shader)
            case _:
                renderer: SimRendererDiffusion_1d_gradient = SimRendererDiffusion_1d_gradient(shader)
        super().__init__(shader, renderer)

    @staticmethod
    def name():
        return "diffusion-1d"

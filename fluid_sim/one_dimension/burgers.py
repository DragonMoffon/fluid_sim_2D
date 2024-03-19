"""
burgers is the combination of the non-linear convection and the diffusion equations.

To run this simulation call "python -m fluid_sim --burgers-1d" in the terminal.
"""
import struct
from array import array
from PIL import Image
from math import exp, pi

import arcade.gl as gl
from arcade import get_window, ArcadeContext
from arcade.resources import resolve

from fluid_sim import SIM_WIDTH, SIM_DT, SIM_DP, SIM_MU, RENDER_MODE_1D, RENDER_MODES_1D
from fluid_sim.lib.sim import SimBase, SimRendererBase, SimShaderBase


class SimShaderBurgers_1d(SimShaderBase):

    def __init__(self):
        win = get_window()
        self._ctx: ArcadeContext = win.ctx

        self._comp_shader: gl.ComputeShader = self._ctx.load_compute_shader(
            ":s:one_dimension/burgers_cs.glsl"
        )

        self._sim_data: gl.Buffer = self._ctx.buffer(
            data=struct.pack(
                "lllll",
                int(100_000*SIM_DT),
                int(100_000*SIM_DP),
                int(100_000*SIM_MU),
                int(100_000*(SIM_DT / SIM_DP)),
                int(100_000*(SIM_DT / SIM_DP**2.0)))
        )

        def phi(x, t):
            return exp(-(x - 4.0 * t)**2 / (4 * SIM_MU * (t + 1.0))) + exp(-(x - 4.0 * t - 2.0 * pi)**2 / (4.0 * SIM_MU * (t + 1)))

        def phi_prime(x, t):
            return -(-8*t + 2*x)*exp(-(-4*t + x)**2/(4*SIM_MU*(t + 1)))/(4*SIM_MU*(t + 1)) - (-8*t + 2*x - 4*pi)*exp(-(-4*t + x - 2*pi)**2/(4*SIM_MU*(t + 1)))/(4*SIM_MU*(t + 1))

        def u(x, t):
            return int((-2.0 * SIM_MU * (phi_prime(x, t) / phi(x, t)) + 4.0)*100_000)

        def u_array():
            _i_frac = 2.0 * pi / SIM_WIDTH
            for i in range(SIM_WIDTH):
                _x = i * _i_frac
                yield u(_x, 0)

        data = array("l", u_array())

        self._write_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="i4",
            data=data
        )

        self._read_u_texture: gl.Texture2D = self._ctx.texture(
            size=(SIM_WIDTH, 1),
            components=1,
            dtype="i4",
            data=data
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


class SimRendererBurgers_1d_gradient(SimRendererBase):

    def __init__(self, shader: SimShaderBurgers_1d):
        super().__init__()

        self._shader: SimShaderBurgers_1d = shader

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
            fragment_shader=":s:one_dimension/1d_int_gradient_map_render_fs.glsl"
        )
        self._render_prog["texture_0"] = 0
        self._render_prog["colour_ramp_0"] = 1
        self._render_prog["max_value"] = 10.0

    def __str__(self):
        return "burgers-1d_gradient"

    def _on_render(self):
        self._shader.active_texture.use(0)
        self._gradient_map_texture.use(1)
        self._draw_geo.render(self._render_prog)


class SimRendererBurgers_1d_graph(SimRendererBase):

    def __init__(self, shader: SimShaderBurgers_1d):
        super().__init__()

        self._shader: SimShaderBurgers_1d = shader

        self._render_prog: gl.Program = self._ctx.load_program(
            vertex_shader=":s:sim_draw_vs.glsl",
            fragment_shader=":s:one_dimension/1d_int_graph_render_fs.glsl"
        )
        self._render_prog["texture_0"] = 0
        self._render_prog["max_value"] = 10.0

    def __str__(self):
        return "burgers-1d_graph"

    def _on_render(self):
        self._shader.active_texture.use(0)
        self._draw_geo.render(self._render_prog)


class SimBurgers_1d(SimBase):

    def __init__(self):
        shader: SimShaderBurgers_1d = SimShaderBurgers_1d()
        match RENDER_MODE_1D:
            case RENDER_MODES_1D.gradient_1d:
                renderer: SimRendererBurgers_1d_gradient = SimRendererBurgers_1d_gradient(shader)
            case RENDER_MODES_1D.graph_1d:
                renderer: SimRendererBurgers_1d_graph = SimRendererBurgers_1d_graph(shader)
            case _:
                renderer: SimRendererBurgers_1d_gradient = SimRendererBurgers_1d_gradient(shader)
        super().__init__(shader, renderer)

    @staticmethod
    def name():
        return "burgers-1d"

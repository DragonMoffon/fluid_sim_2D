"""
The base class for the simulation shader. This holds the compute shader, and the data necessary for it to work.
"""


class SimShaderBase:

    def _flip(self):
        raise NotImplementedError()

    def _calculate(self):
        raise NotImplementedError()

    def update(self):
        self._flip()
        self._calculate()

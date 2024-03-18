from sys import argv
import warnings
from pathlib import Path

from arcade.resources import add_resource_handle, get_resource_handle_paths

__all__ = (
    "REACTIVE",
    "FULLSCREEN",
    "SMOOTH",
    "CONSOLE_OFF",
    "VERBOSE",
    "THROW_ERRORS",
    "SCREEN_WIDTH",
    "SCREEN_HEIGHT",
    "SIM_WIDTH",
    "SIM_HEIGHT",
    "SIM_SCALING",
    "SIM_DT",
    "LOG_DIST",
    "SAVE_RATE",
    "ROLL_BACK_CAP",
    "STACK_DEPTH"
)

add_resource_handle("s", Path("./shaders").resolve())
add_resource_handle("r", Path("./resources").resolve())
add_resource_handle("l", Path("./logs").resolve())

root = argv[0]
arguments = set(arg.lower() for arg in argv[1:])

SIM_NAME = "" if len(argv) <= 1 else argv[1][2:]

# Set all boolean values.
REACTIVE = "--reactive" in arguments
arguments.discard("--reactive")
FULLSCREEN = "--fullscreen" in arguments
arguments.discard("--fullscreen")
SMOOTH = "--smooth" in arguments
arguments.discard("--smooth")
CONSOLE_OFF = "--console-off" in arguments
arguments.discard("--console-off")
VERBOSE = "--verbose" in arguments
arguments.discard("--verbose")
THROW_ERRORS = "--throw" in arguments
arguments.discard("--throw")

# Set all Variables
argument_dict = {
    arg.split("=")[0]: arg.split("=")[-1]
    for arg in tuple(arguments) if "=" in arg
}

SCREEN_WIDTH = int(argument_dict.get("--width", 100))
arguments.discard(f"--width={SCREEN_WIDTH}")
SCREEN_HEIGHT = int(argument_dict.get("--height", 100))
arguments.discard(f"--height={SCREEN_HEIGHT}")
SIM_SCALING = int(argument_dict.get("--scale", 1))
arguments.discard(f"--scale={SIM_SCALING}")
SIM_WIDTH = SCREEN_WIDTH // SIM_SCALING
SIM_HEIGHT = SCREEN_HEIGHT // SIM_SCALING

if SCREEN_WIDTH % SIM_SCALING != 0 or SCREEN_HEIGHT % SIM_SCALING != 0:
    raise ValueError(f"scale={SIM_SCALING} is not a factor of width={SCREEN_WIDTH} and height={SCREEN_HEIGHT}")

_dt_frac = argument_dict.get("--dt", "1/60").split("/")
if len(_dt_frac) != 2:
    raise ValueError(f"provided delta time fraction is invalid please use the format x/y not {argument_dict.get('--dt', '1/60')}")

SIM_DT = float(_dt_frac[0]) / float(_dt_frac[-1])
arguments.discard(f"--dt={_dt_frac[0]}/{_dt_frac[-1]}")

_dp_frac = argument_dict.get("--dp", f"1/{SIM_WIDTH}").split("/")
if len(_dp_frac) != 2:
    raise ValueError(f"provided delta position fraction is invalid please use the format x/y not {argument_dict.get('--dt', f'1/{SIM_WIDTH}')}")

SIM_DP = float(_dp_frac[0]) / float(_dp_frac[-1])
arguments.discard(f"--dt={_dp_frac[0]}/{_dp_frac[-1]}")

_log_name = argument_dict.get("--log-dist", "log.txt")
arguments.discard(f"--log-dist={_log_name}")
LOG_DIST = get_resource_handle_paths("l")[0] / Path(_log_name)

SAVE_RATE = int(argument_dict.get("--save-rate", 1))
arguments.discard(f"--save-rate={SAVE_RATE}")
if SAVE_RATE < 1:
    raise ValueError(f"{SAVE_RATE} must be 1 or greater")

ROLL_BACK_CAP = int(argument_dict.get("--roll-back-cap", 5))
arguments.discard(f"--roll-back-cap={ROLL_BACK_CAP}")

STACK_DEPTH = int(argument_dict.get("--stack-depth", 5))
arguments.discard(f"--stack-depth={STACK_DEPTH}")

for arg in tuple(arguments):
    warnings.warn(f"unrecognised argument [{arg}]. It is being Ignored")
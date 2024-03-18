# fluid_sim_2D
 A 1D and 2D fluid sim engine built with python arcade

To run the code ensure you are within the root directory "fluid_sim_2D" and run
"python -m fluid_sim"

### Valid Args
#### | - MODE: (the mode should always be the first value)
 <span style="color:yellow">linear-convection</span> <span style="color:orange">[default]</span> The simplest 1D simulation. 
#### | - VARIABLES:
 <span style="color:yellow">--width=int</span> <span style="color:orange">[default: 100]</span> <span style="color:red">(Must be even)</span> sets window width \
 <span style="color:yellow">--height=int</span> <span style="color:orange">[default: 100]</span> <span style="color:red">(Must be even)</span> sets window height \
 <span style="color:yellow">--scale=int</span> <span style="color:orange">[default: 1]</span> <span style="color:red">(Must be a factor of width and height)</span> sets ratio between screen and sim pixels \
 <span style="color:yellow">--dt=fraction</span> <span style="color:orange">[default: 1/60]</span> <span style="color:red">(should be less than or equal to update)</span> set the dt of the fixed updates \
 <span style="color:yellow">--dp=fraction</span> <span style="color:orange">[default: 1/50]</span> <span style="color:red">(The smaller, the more accurate)</span> set the dx and dy of the simulation \
 <span style="color:yellow">--log-name=path</span> <span style="color:orange">[default log.txt]</span> sets the name of the log file. Is always saved in the logs folder <span style="color:red">UNUSED</span> \
 <span style="color:yellow">--save-rate=int</span> <span style="color:orange">[default: 1]</span> how many logs must occur before the console saves to the log destination <span style="color:red">UNUSED</span>
#### | - BOOLEANS
 <span style="color:yellow">--reactive</span> sets if the sim reacts to the movement of the mouse or the window <span style="color:red">UNUSED</span> \
 <span style="color:yellow">--fullscreen</span> sets the sim to fullscreen, if the width and height are set the sim then uses those values \
 <span style="color:yellow">--smooth</span> sets the filtering on the sim drawn texture to linear rather than nearest \
 <span style="color:yellow">--console-off</span> disables the imgui debug console <span style="color:red">UNUSED</span> \
 <span style="color:yellow">--verbose</span> adds extra details to the logs and debug console <span style="color:red">UNUSED</span> \
 <span style="color:yellow">--throw</span> causes python to throw when a fatal error occurs rather than the sim rolling back <span style="color:red">UNUSED</span>
#### | - ENUMS <span style="color:red">[NOT YET IMPLIMENTENTED]</span>


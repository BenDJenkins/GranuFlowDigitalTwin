from liggghts import liggghts
import numpy as np
import os

## Orifice Sizes

orifice_size = [2]  # mm ((TEST))
# orifice_size = [2, 4, 8, 12, 18, 22, 28]  # mm
# orifice_size = np.divide(orifice_size, 1000)  # Convert to meters

for i in range(len(orifice_size)):

    print(orifice_size[i])
    os.popen('cp Run_GF_Sim.liggghts Run_GF_Sim_{}.liggghts'.format(orifice_size[i]))

    with open(os.path.join(""))

# lmp = liggghts()

# lmp.file('Run_GF_Sim.liggghts')  # Read LIGGGHTS file

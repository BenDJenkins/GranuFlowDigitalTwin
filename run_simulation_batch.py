import os
import shutil

## Orifice Sizes

orifice_size = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]  # mm

for i in range(len(orifice_size)):

    # Create the LIGGGHTS script files for different orifice sizes using template.

    shutil.copyfile('Run_GF_Sim.liggghts', 'Run_GF_Sim_{}mm.liggghts'.format(orifice_size[i]))

    with open('Run_GF_Sim_{}mm.liggghts'.format(orifice_size[i])) as f:
        sim_input = f.readlines()

    sim_input[128] = "fix	plate	all mesh/surface file geometry/Plate" + str(orifice_size[i]) + "mm.stl	type 2  scale 0.001\n"
    sim_input[186] = '''fix output all print ${outputsteps} "$t,${massTube}" screen no file MassFlowrate''' + str(orifice_size[i]) + 'mm.csv title "Time,MassInTube"\n'

    with open('Run_GF_Sim_{}mm.liggghts'.format(orifice_size[i]), "w") as f:
        f.writelines(sim_input)

    # Create the run.sh files for BlueBear.

    with open('run_simulation.sh', "r") as f:
        lines = f.readlines()

    lines[17] = 'lmp_auto < Run_GF_Sim_' + str(orifice_size[i]) + 'mm.liggghts'
    batch_filename = f"run_simulation" + str(orifice_size[i]) + "mm"
    with open(batch_filename, "w") as f:
        f.writelines(lines)

    os.system(f"sbatch {batch_filename}")

#!/bin/bash
#SBATCH --time 10-0:0
#SBATCH --ntasks 16
#SBATCH --qos bbdefault
#SBATCH --account=windowcr-granutools-engd
#SBATCH --mail-type ALL



set -e
module purge; module load bluebear

module load bear-apps/2020a
module load LIGGGHTS/3.8.0-foss-2020a

module load Anaconda3

lmp_auto < Run_GF_Sim.liggghts

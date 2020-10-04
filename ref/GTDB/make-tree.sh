#!/bin/bash

# MSA with mafft/linsi
linsi GTDB_r89.GENUS_cons.fa > GTDB_r89.GENUS_cons.linsi_out 
linsi GTDB_r89.SPECIES_cons.fa > GTDB_r89.SPECIES_cons.linsi_out 

# Tree construction
 fasttree -nt GTDB_r89.GENUS_cons.linsi_out > GTDB_r89.GENUS_cons.linsi_fasttree
 fasttree -nt GTDB_r89.SPECIES_cons.linsi_out > GTDB_r89.SPECIES_cons.linsi_fasttree

 ete3 view --text -t  GTDB_r89.GENUS_cons.linsi_fasttree > GTDB_r89.GENUS_cons.linsi_treeview
 ete3 view --text -t  GTDB_r89.SPECIES_cons.linsi_fasttree > GTDB_r89.SPECIES_cons.linsi_treeview

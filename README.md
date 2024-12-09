# slabvacuum
A small package to create slab-vacuum-system cif files from those of bulks.

## Installation
(You need to install python.)

From your terminal, execute
```
pip install git+https://github.com/ShotaNamerikawa/slabvacuum.git
```

## How to use
A command to create a slab-vacuum cif file is automatically installed.
You can create the files by
```
get_slab_cif <bulk_cif_file> <number_of_slab_layers> [--miller_index <miller_index> |--points_on_surface <points on surface in fractional coordinates>] 
```
This command creates `layered.cif` in the current directory.

- `--miller_index` or `--points_on_surface` must be specified.
- The atomic plane position specified by these parameters corresponds to the nearest distance vector from a slab to another slab. 

- If `--points_on_surface` is given, you must pass at least 3 atomic positions the atomic plane passes in fractional coordinates. For example,
```
0 0 10 1 0 10 0 1 10
```
is interpreted as (0,0,10), (1,0,10), (0,1,10) points are on the atomic plane you want to set. If more than 3 points are given, the combination of points, for which corresponding atomic plane is the nearest is chosen.

- For other options, execute, in terminal,
```
get_slab_cif --help
```
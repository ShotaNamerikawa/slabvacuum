import numpy as np
from pilecrystal.pile_generator import get_slab_vac_cif, cli_get_slab_cif
from pymatgen.core import Structure
import pytest
from click.testing import CliRunner


def test_get_slab_vac_cif(min_slab_size, min_vacuum_size, tmp_path):
    cubic_structure = Structure(np.array([[1,0,0],[0,1,0],[0,0,1]]), ["A"], [0,0,0])
    get_slab_vac_cif(cubic_structure, min_slab_size, min_vacuum_size, in_unit_planes=True, 
                     slab_cif_prefix = tmp_path/"slab", 
                     frac_coords_on_surface_plane=[[0,0,1],[1,0,1],[0,1,1]])
    slab_structure = Structure.from_file(tmp_path/"slab.cif")
    assert slab_structure.lattice.a[2,2] == (min_vacuum_size+min_slab_size)*cubic_structure.lattice.a[2,2]
    

def test_cli_get_slab_cif():
    runner = CliRunner()
    arg_list = (structure, [0,0,1], 5, 5, slab_cif_prefix=os.path.join("tests/models","layered"))
    result = runner.invoke(cli_get_slab_cif, 
                           arg_list # List of arguments of the function decorated by click.command
                           )
    assert result.exit_code == 0 # 0 means success
    # assert result.output == output_of_command

    cif_file = "tests/models/Mn2VGa.cif"
    structure = Structure.from_file(cif_file)
    get_slab_vac_cif()

import numpy as np
from pymatgen.core import Structure
import pytest
from click.testing import CliRunner
from pathlib import Path

from pilecrystal.pile_generator import get_slab_vac_cif, cli_get_slab_cif

@pytest.mark.parametrize(["min_slab_size", "min_vacuum_size"], [(10,5)])
def test_get_slab_vac_cif(min_slab_size, min_vacuum_size, tmp_path):
    cubic_structure = Structure(np.array([[1,0,0],[0,1,0],[0,0,1]]), ["A"], [[0,0,0]]) # bulk is cubic structure.
    get_slab_vac_cif(cubic_structure, min_slab_size, min_vacuum_size, in_unit_planes=True, 
                     slab_cif_prefix = tmp_path/"slab", 
                     frac_coords_on_surface=[[0,0,1],[1,0,1],[1,0,1]])
    slab_structure = Structure.from_file(tmp_path/"slab.cif")
    assert slab_structure.lattice.matrix[2,2] == (min_vacuum_size+min_slab_size)*cubic_structure.lattice.matrix[2,2]
    # assert np.allclose(slab_structure.sites, np.array([[0,0,i/(min_slab_size + min_vacuum_size)] for i in range(min_slab_size)]))
    print(slab_structure.sites)
    
@pytest.mark.parametrize(["bulk_cif", "min_slab_size", "min_vacuum_size", "miller_index_or_frac_coords_dict"], 
                         [("tests/models/Mn2VGa.cif",10,5,dict(miller_index = (0,0,10)))])
def test_get_slab_vac_cif_from_file(bulk_cif, min_slab_size, min_vacuum_size, miller_index_or_frac_coords_dict, tmp_path):
    structure = Structure.from_file(bulk_cif)
    get_slab_vac_cif(structure, min_slab_size, min_vacuum_size, in_unit_planes=True, 
                     slab_cif_prefix = tmp_path/"slab", 
                     **miller_index_or_frac_coords_dict)
    slab_structure = Structure.from_file(tmp_path/"slab.cif")
    assert slab_structure.lattice.matrix[2,2] == (min_vacuum_size+min_slab_size)*structure.lattice.matrix[2,2]
    # assert np.allclose(slab_structure.sites, np.array([[0,0,i/(min_slab_size + min_vacuum_size)] for i in range(min_slab_size)]))
    print(slab_structure.sites)
    # print(cubic_structure.lattice.matrix)# remove
    
def test_cli_get_slab_cif():
    runner = CliRunner()
    arg_list = ["tests/models/Mn2VGa.cif", "5", "5", "--points_on_surface", "0", "0", "10", "1", "0", "10", "0", "1", "10"]
    result = runner.invoke(cli_get_slab_cif, 
                           arg_list # List of arguments of the function decorated by click.command
                           )
    # assert result.exit_code == 0 # 0 means success
    # assert result.output == output_of_command
    if result.exit_code != 0:
        print("Test failed!")
        print("=== Output ===")
        print(result.output)
        print("=== Exception ===")
        if result.exception:
            print(result.exception)
        print("=== Traceback ===")
        if result.exc_info:
            import traceback
            traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
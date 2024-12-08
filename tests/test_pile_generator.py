from pilecrystal.pile_generator import set_layers, get_layered_cif, get_slab
from pymatgen.core import Structure
from pymatgen.core.surface import SlabGenerator
from click.testing import CliRunner

def test_set_layers():
    structrue = Structure.from_file("tests/models/Mn2VGa.cif") 
    slabgen = SlabGenerator(structrue,[0,0,1],10,10)
    n_layers_slab = 2
    n_layers_vac = 2
    set_layers(slabgen, n_layers_slab, n_layers_vac)
    slabs = slabgen.get_slabs()
    anum=0
    for specie in slabs[0].species:
        if "Mn" in str(specie):
            anum += 1 
    assert anum == 16
    
def test_get_cif(tmp_path):
    cif_file = "tests/models/Mn2VGa.cif"
    structure = Structure.from_file(cif_file)
    get_layered_cif(structure, [0,0,1], 5, 5, slab_cif_name= tmp_path)
    
def test_cli(tmp_path):
    # FIXME: make a bulk file from a Structure instance in this method.
    runner = CliRunner()
    result = runner.invoke(get_slab, 
                           ["tests/models/Mn2VGa.cif", 
                            (0,0,1),
                            5,
                            5,
                            tmp_path,
                            None])
    assert result.exit_code == 0
    with open(tmp_path) as fp:
        # add test cif parameter by converting it to Structure.
        pass
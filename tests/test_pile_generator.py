import sys
sys.path.append("./")
from pilecrystal.pile_generator import set_layers, get_layered_cif
from pymatgen.core import Structure
from pymatgen.core.surface import SlabGenerator
import os
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
    
def test_get_cif():
    cif_file = "tests/models/Mn2VGa.cif"
    structure = Structure.from_file(cif_file)
    get_layered_cif(structure, [0,0,1], 5, 5, cif_prefix=os.path.join("tests/models","layered"))
    
    
if __name__ == "__main__":
    import sys
    sys.path.append("./")
    test_set_layers()
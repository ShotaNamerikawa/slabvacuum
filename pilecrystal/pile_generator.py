from pymatgen.core.surface import SlabGenerator
from pymatgen.core import Structure
def set_layers(slabgen:SlabGenerator, n_layers_slab, n_layers_vac):
    """set n_layers of slabgen to user-defined value.

    Parameters
    ----------
    slabgen : SlabGenerator
        _description_
    n_layers_slab : _type_
        layer number of slabs
    n_layers_vac : _type_
        layer number of vacuum
    """
    h = slabgen._proj_height
    p = round(h / slabgen.parent.lattice.d_hkl(slabgen.miller_index), 8)
    if slabgen.in_unit_planes == True:
        slabgen.min_slab_size = p*n_layers_slab
        slabgen.min_vac_size = p*n_layers_vac
    else:
        slabgen.min_slab_size = h*n_layers_slab
        slabgen.min_vac_size = h*n_layers_vac
        
def get_layered_cif(structure:Structure, miller_index, n_layers_slab, n_layers_vac, *slabgen_args, cif_prefix="layered", **slabgen_kwargs):
    slabgen = SlabGenerator(structure, miller_index, 10,10, *slabgen_args, **slabgen_kwargs)
    set_layers(slabgen, n_layers_slab, n_layers_vac)
    slabs = slabgen.get_slabs()
    cif_str = slabs[0].to(filename=".cif")
    with open(cif_prefix + ".cif", 'w') as fp:
        fp.write(cif_str)
        
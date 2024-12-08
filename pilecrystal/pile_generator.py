from pymatgen.core.surface import SlabGenerator
from pymatgen.core import Structure
import click

def set_layers(slabgen:SlabGenerator, n_layers_slab:int, n_layers_vac:int):
    """set n_layers of SlabGenerator to be user-defined value.
    
    set n_layers of an SlabGenerator, which cannot be directly changed in the constructor of the class.

    Parameters
    ----------
    slabgen : SlabGenerator
        a SlabGenerator instance
    n_layers_slab : int
        the layer number of slabs
    n_layers_vac : int
        the layer number of vacuum
    """
    h = slabgen._proj_height
    p = round(h / slabgen.parent.lattice.d_hkl(slabgen.miller_index), 8)
    
    # set min_slab_size and min_vac_size to be those corresponding_to n_layers_slab and n_layers_vac.
    if slabgen.in_unit_planes == True:
        slabgen.min_slab_size = p*n_layers_slab
        slabgen.min_vac_size = p*n_layers_vac
    else:
        slabgen.min_slab_size = h*n_layers_slab
        slabgen.min_vac_size = h*n_layers_vac
        
def get_layered_cif(structure:Structure, miller_index, n_layers_slab, n_layers_vac, *slabgen_args, 
                    slab_cif_name="layered.cif", 
                    max_normal_search: int|None = None, 
                    **slabgen_kwargs:dict[str,bool]):
    """get layered cif structure
    
    NOTE: If you want miller_index to correspond to a conventional cell, you should pass Structure of a conventional cell!

    Parameters
    ----------
    structure : Structure
        _description_
    miller_index : _type_
        _description_
    n_layers_slab : _type_
        _description_
    n_layers_vac : _type_
        _description_
    slab_cif_name : str, optional
        _description_, by default "layered"
    """
    min_slab_size = 10
    min_vacuum_size = 10
    slabgen = SlabGenerator(structure, miller_index, min_slab_size, min_vacuum_size, *slabgen_args, **slabgen_kwargs)
    set_layers(slabgen, n_layers_slab, n_layers_vac)
    slabs = slabgen.get_slabs()
    cif_str = slabs[0].to(filename=".cif")
    with open(slab_cif_name , 'w') as fp:
        fp.write(cif_str)
        
@click.command()
@click.option('--cif', prompt='the name of bulk cif file', help='', required = True) #argument1 of cli function.
@click.option('--miller', prompt='miller index:',
              help='For miller index, see the article of wikipedia.',
              type = int,
              nargs = 3,
              required = True
              )
@click.option('--num_slab', prompt='the number of slab layers',
              type = int,
              default = 5,
              required = True
              )
@click.option('--num_vacuum', prompt='the number of slab layers',
              type = int,
              default = 5,
              required = True
              )
@click.option('--slab_cif_name', prompt='the name of the slab cif file created from the original bulk cif file',
              default = "layered",
              )
@click.option('--max_normal_search', 
              prompt='SlabGenerator.max_normal_search',
              default = 0,
              type = int)
def get_slab(cif:str, miller:tuple[int], num_slab:int, num_vacuum:int, slab_cif_name:str, max_normal_search:int|None = None):
    bulk_strct = Structure.from_file(cif)
    get_layered_cif(bulk_strct, miller, num_slab, num_vacuum, slab_cif_name = slab_cif_name, 
                    max_normal_search=None if max_normal_search == 0 else max_normal_search)
import numpy as np
from typing import Iterable

from pymatgen.core.surface import SlabGenerator
from pymatgen.core import Structure
import click
        
def get_slab_vac_cif(structure:Structure, 
                    min_slab_size:int|float, 
                    min_vacuum_size:int|float, 
                    *slabgen_args, 
                    in_unit_planes = True, 
                    slab_cif_prefix:str="layered", 
                    miller_index:Iterable|None = None,
                    frac_coords_on_surface:None|Iterable = None,
                    **slabgen_kwargs):
    """get a cif file of slab-vacuum system from bulk Structure

    Parameters
    ----------
    structure : Structure
        pymatgen.core.Structure
    min_slab_size : int | float
        minimum size of slab layers in "the specified unit".
        "the specified unit" is specified by in_unit_planes keyword argument of this function.
    min_vacuum_size : int | float
        minimum size of vacuum layers in "the specified unit".
        "the specified unit" is specified by in_unit_planes keyword argument of this function.
    in_unit_planes : bool, optional
        set unit of min_**_size
        If True, min_**_size is interpreted as integer 
        , by default True
    cif_prefix : str, optional
        the prefix of the generated slab cif file,
        ".cif" is attached to cif_prefix in the slab-cif-file name.
        , by default "layered"
    miller_index : Iterable | None, optional
        miller index of a plane parallel to the atomic plane, 
        If this keyword is not specified, coords_on_surface_plane argument must be specified,
        by default None
    frac_coords_on_surface_plane : None | Iterable, optional
        fractional coordinates of at least 3 points on an atomic plane parallel to the surface plane, by default None

    Raises
    ------
    ValueError
        _description_
    """
    if miller_index is None and frac_coords_on_surface is None:
        raise ValueError("Neither miller_index nor coords_on_surface_plane is not given.")
    if frac_coords_on_surface is not None:
        if type(min_slab_size) != int or type(min_vacuum_size) != int:
            raise TypeError("the type of min_slab_size and min_vacuum_size must be integer.")
        miller_index = structure.lattice.get_miller_index_from_coords(frac_coords_on_surface, coords_are_cartesian=False)
    slabgen = SlabGenerator(structure, miller_index, min_slab_size, min_vacuum_size, *slabgen_args, in_unit_planes=in_unit_planes, **slabgen_kwargs)
    slabs = slabgen.get_slabs()
    cif_str = slabs[0].to(filename=".cif")
    
    slab_cif_prefix = str(slab_cif_prefix)
    with open(slab_cif_prefix + ".cif", 'w') as fp:
        fp.write(cif_str)
        
@click.command()
@click.argument("bulk_cif")
@click.argument("min_slab_size", type = int)
@click.argument("min_vacuum_size", type = int)
@click.option("--primitive_bulk",type = bool, default = False)
@click.option("--size_in_unit_planes", type = bool, default = True)
@click.option("--cif_prefix", default = "layered")
@click.option("--miller_index", nargs = 3, type = int)
@click.option("--points_on_surface", nargs = 9, type = float)
def cli_get_slab_cif(bulk_cif:str, 
                     min_slab_size:int|float, 
                    min_vacuum_size:int|float, 
                    primitive_bulk:bool = False,
                    size_in_unit_planes:bool = True,
                    miller_index:None|Iterable = None,
                    points_on_surface:None|Iterable = None,
                    cif_prefix:str = "layered"
                    ):
    """generate a slab cif file from a bulk cif file.

    Parameters
    ----------
    bulk_cif : str
        the file name of a bulk cif file from which a corresponding bulk file is generated
    min_slab_size : int | float
        the number of or the thickness in angstrom of the slab layers.
    min_vacuum_size : int | float
        the number of or the thickness in angstrom of the vacuum layer.
    primitive_bulk : bool, optional
        convert bulk unit cell into primitive, by default False
    size_in_unit_planes : bool, optional
        min_**_size is in unit of minimum distance to atomic planes, 
        If False, min_**_size is in unit of Angstrom
        by default True
    miller_index : None | Iterable, optional
        miller_index of an atomic plane parallel to the surface plane, by default None
    points_on_surface : None | Iterable, optional
        fractional coordinates of 3 points on a surface plane, by default None
    cif_prefix : str, optional
        prefix of the generated slab cif file name, by default "layered"
    """
    if (not miller_index) and (not points_on_surface):
        # NOTE: click prints only the errors defined in click.
        raise click.ClickException("Neither miller_index nor coords_on_surface_plane is not given.")
    bulk_structure = Structure.from_file(bulk_cif, primitive= primitive_bulk)
    try:
        get_slab_vac_cif(bulk_structure, 
                         min_slab_size, 
                         min_vacuum_size, 
                         slab_cif_prefix= cif_prefix,
                         miller_index= miller_index, 
                         frac_coords_on_surface= np.array(points_on_surface).reshape([-1,3]) if points_on_surface else points_on_surface,
                         in_unit_planes= size_in_unit_planes)
    except:
        raise click.ClickException("Error.")
    
if __name__ == "__main__":
    cli_get_slab_cif()  

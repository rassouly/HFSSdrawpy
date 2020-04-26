import numpy as np
from functools import wraps

from . import Lib
from .utils import parse_entry, Vector
from .KeyElement import move

__methods__ = []
register_method = Lib.register_method(__methods__)
eps = 1e-7
layer_TRACK = 1
layer_GAP = 0
layer_RLC = 2
layer_MESH = 3
layer_MASK = 4
layer_Default = 10


@register_method

@register_method
@move
def draw_coax_resonator_3D(self, thickness, in_length, out_length, in_radius, out_radius, side_holes=None, name="resonator"):

    thickness, in_length, out_length, in_radius, out_radius = parse_entry(
        thickness, in_length, out_length, in_radius, out_radius)

    mesh_resolution = parse_entry('3')

    cap_eps = parse_entry('0.05mm')

    resonator = self.box_corner_3D([-thickness-out_radius,
                                    -thickness-out_radius,
                                    0],
                                   [2*thickness+2*out_radius,
                                    2*thickness+2*out_radius,
                                    thickness+in_length+out_length],
                                   name=name)

    resonator_hole = self.cylinder_3D([0, 0, thickness],
                            out_radius,
                            in_length+out_length,
                            'Z',
                            name=name+"_hole")
    
    resonator.subtract(resonator_hole, True)

    resonator_tube = self.cylinder_3D([0, 0, thickness],
                                      in_radius,
                                      in_length,
                                      'Z',
                                      name=name+'_tube')
    
    resonator.unite(resonator_tube)

    resonator_hole.subtract(resonator, True)
    resonator_hole.assign_mesh_length((out_radius-in_radius)/mesh_resolution)

    cap = self.box_corner_3D([-thickness-out_radius,
                              -thickness-out_radius,
                              in_length+out_length+thickness+cap_eps],
                             [2*thickness+2*out_radius,
                              2*thickness+2*out_radius,
                              thickness],
                             name=name+'_cap')
    
    cap.assign_material("aluminum")
    cap.assign_perfect_E(name+'_PerfE')

    cap_space = self.box_corner_3D([-thickness-out_radius,
                                    -thickness-out_radius,
                                    in_length+out_length+thickness],
                                   [2*thickness+2*out_radius,
                                    2*thickness+2*out_radius,
                                    cap_eps],
                                   name=name+'_cap_space')
    
    cap_space.assign_mesh_length("2mm")

    if(side_holes is not None):

        if('-X' in side_holes):

            height, width = parse_entry(side_holes['-X']['height'], side_holes['-X']['width'])

            side_hole_west = self.box_corner_3D([-thickness-out_radius,
                                              -width/2,
                                              thickness+in_length],
                                             [thickness+(out_radius-in_radius)/2,
                                              width,
                                              height],
                                             name=name+'_side_hole_west')
        
            resonator.subtract(side_hole_west, True)
            side_hole_west.subtract(resonator_hole, True)
            side_hole_west.assign_mesh_length(width/mesh_resolution)

        if('+X' in side_holes):

            height, width = parse_entry(
                side_holes['+X']['height'], side_holes['+X']['width'])

            side_hole_est = self.box_corner_3D([in_radius+(out_radius-in_radius)/2,
                                              -width/2,
                                              thickness+in_length],
                                             [thickness+(out_radius-in_radius)/2,
                                              width,
                                              height],
                                             name=name+'_side_hole_est')
            
            resonator.subtract(side_hole_est, True)
            side_hole_est.subtract(resonator_hole, True)
            side_hole_est.assign_mesh_length(width/mesh_resolution)

        if('-Y' in side_holes):

            height, width = parse_entry(side_holes['-Y']['height'], side_holes['-Y']['width'])

            side_hole_south = self.box_corner_3D([-width/2,
                                              -thickness-out_radius,
                                              thickness+in_length],
                                             [width,
                                              thickness + (out_radius-in_radius)/2,
                                              height],
                                             name=name+'_side_hole_south')
        
            resonator.subtract(side_hole_south, True)
            side_hole_south.subtract(resonator_hole, True)
            side_hole_south.assign_mesh_length(width/mesh_resolution)

        if('+Y' in side_holes):

            height, width = parse_entry(side_holes['+Y']['height'], side_holes['+Y']['width'])

            side_hole_north = self.box_corner_3D([-width/2,
                                              in_radius+(out_radius-in_radius)/2,
                                              thickness+in_length],
                                             [width,
                                              thickness + (out_radius-in_radius)/2,
                                              height],
                                             name=name+'_side_hole_north')

            resonator.subtract(side_hole_north, True)
            side_hole_north.subtract(resonator_hole, True)
            side_hole_north.assign_mesh_length(width/mesh_resolution)

    resonator.assign_material("aluminum")
    resonator.assign_perfect_E(name+'_PerfE')

    return resonator


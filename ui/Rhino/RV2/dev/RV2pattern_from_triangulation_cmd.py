from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas_rhino.geometry import RhinoCurve
from compas_rv2.datastructures import Pattern
from compas.geometry import centroid_points_xy
from compas.utilities import geometric_key
from compas.utilities import pairwise
import rhinoscriptsyntax as rs

from compas.rpc import Proxy
triangle = Proxy('compas_triangle.delaunay')


__commandname__ = "RV2pattern_from_triangulation"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    boundary_guids = compas_rhino.select_curves('Select outer boundary.')
    if not boundary_guids:
        return

    hole_guids = compas_rhino.select_curves('Select inner boundaries.')
    segments_guids = compas_rhino.select_curves('Select constraint curves.')

    target_length = rs.GetReal('Specifiy target edge length.')
    if not target_length:
        return

    # boundary
    boundary = []
    boundary_seg_guids = compas_rhino.rs.ExplodeCurves(boundary_guids[0])
    for guid in boundary_seg_guids:
        curve = RhinoCurve.from_guid(guid)
        N = int(curve.length() / target_length)
        points = curve.divide(N, over_space=True)
        boundary.extend(map(list, points))

    # polylines
    polylines = []
    if segments_guids:
        for guid in segments_guids:
            curve = RhinoCurve.from_guid(guid)
            N = int(curve.length() / target_length)
            points = curve.divide(N, over_space=True)
            polylines.append(map(list, points))

    # polygons
    polygons = []
    if hole_guids:
        for guid in hole_guids:
            curve = RhinoCurve.from_guid(guid)
            N = int(curve.length() / target_length)
            points = curve.divide(N, over_space=True)
            polygons.append(map(list, points))

    area = target_length ** 2 * 0.5 * 0.5 * 1.732
    vertices, faces = triangle.constrained_delaunay_triangulation(
        boundary, polylines, polygons, area=area)

    pattern = Pattern.from_vertices_and_faces(vertices, faces)

    scene.clear()
    scene.add(pattern, name='pattern')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)

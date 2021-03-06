from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas.utilities import flatten

__commandname__ = "RV2boundaryconditions_supports"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    # mark all fixed vertices as anchors
    # mark all leaves as anchors

    fixed = list(pattern.datastructure.vertices_where({'is_fixed': True}))
    leaves = []
    for vertex in pattern.datastructure.vertices():
        nbrs = pattern.datastructure.vertex_neighbors(vertex)
        count = 0
        for nbr in nbrs:
            if pattern.datastructure.edge_attribute((vertex, nbr), '_is_edge'):
                count += 1
        if count == 1:
            leaves.append(vertex)

    anchors = list(set(fixed) | set(leaves))
    if anchors:
        pattern.datastructure.vertices_attribute('is_anchor', True, keys=anchors)
        scene.update()

    # manually Select or Unselect
    # shoudl this not be included in the while loop?

    options = ["Select", "Unselect", "ESC"]
    option1 = compas_rhino.rs.GetString("Select or unselect vertices as supports:", options[-1], options)

    if not option1 or option1 == 'ESC':
        return

    # layer = pattern.settings['layer']
    # group_supports = "{}::vertices::supports".format(layer)

    # compas_rhino.rs.ShowGroup(group_supports)
    # compas_rhino.rs.Redraw()

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual", "ESC"]

    while True:
        option2 = compas_rhino.rs.GetString("Selection mode:", options[-1], options)

        if not option2 or option2 == 'ESC':
            return

        elif option2 == "Corners":
            keys = []
            for key in pattern.datastructure.vertices_on_boundary():
                if pattern.datastructure.vertex_degree(key) == 2:
                    keys.append(key)

        elif option2 == "AllBoundaryVertices":
            keys = pattern.datastructure.vertices_on_boundary()

        elif option2 == 'ByContinuousEdges':
            temp = pattern.select_edges()
            keys = list(set(flatten([pattern.datastructure.continuous_vertices(key) for key in temp])))

        elif option2 == 'Manual':
            keys = pattern.select_vertices()

        else:
            raise NotImplementedError

        if keys:
            if option1 == "Select":
                pattern.datastructure.vertices_attribute('is_anchor', True, keys=keys)
            else:
                pattern.datastructure.vertices_attribute('is_anchor', False, keys=keys)

        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)

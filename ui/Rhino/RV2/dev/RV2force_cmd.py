from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import ForceDiagram
from compas.geometry import Translation
from compas.geometry import subtract_vectors
from compas.geometry import length_vector

__commandname__ = "RV2tna_start"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        return

    form = scene.get("form")[0]
    if not form:
        return

    force = ForceDiagram.from_formdiagram(form)

    bbox_form = form.bounding_box_xy()
    bbox_force = force.bounding_box_xy()
    xmin_form, xmax_form = bbox_form[0][0], bbox_form[1][0]
    xmin_force, _ = bbox_force[0][0], bbox_force[1][0]
    ymin_form, ymax_form = bbox_form[0][1], bbox_form[3][1]
    ymin_force, ymax_force = bbox_force[0][1], bbox_force[3][1]
    y_form = ymin_form + 0.5 * (ymax_form - ymin_form)
    y_force = ymin_force + 0.5 * (ymax_force - ymin_force)
    dx = 1.5 * (xmax_form - xmin_form) + (xmin_form - xmin_force)
    dy = y_form - y_force
    force.transform(Translation([dx, dy, 0]))

    scene.add(force, name='force')
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
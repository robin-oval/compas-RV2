from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino.objects.meshobject import MeshObject
from compas_rv2.rhino import delete_objects
from compas_rhino.artists import MeshArtist


__all__ = ["PatternObject"]


class PatternObject(MeshObject):
    """Scene object for mesh-based data structures in RV2.

    Parameters
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    pattern : :class:`compas_rv2.datastructures.Pattern`
        The pattern data structure.

    Attributes
    ----------
    scene : :class:`compas_rv2.scene.Scene`
        The RhinoVault 2 scene.
    pattern : :class:`compas_rv2.datastructures.Pattern`
        The pattern data structure.
    artist : :class:`compas_rv2.rhino.PatternArtist`
        The specialised pasttern artist.
    """

    __module__ = 'compas_rv2.rhino'

    settings = {
        'layer': "RV2::Pattern",
        'show.vertices': True,
        'show.edges': True,
        'show.faces': False,
        'color.vertices': [255, 255, 255],
        'color.vertices:is_anchor': [255, 0, 0],
        'color.vertices:is_fixed': [0, 0, 255],
        'color.edges': [0, 0, 0],
        'color.faces': [200, 200, 200],
        'from_surface.density.U': 10,
        'from_surface.density.V': 10,
    }

    def __init__(self, scene, pattern, **kwargs):
        super(PatternObject, self).__init__(scene, pattern, **kwargs)
        self.artist = MeshArtist(self.datastructure)

    def draw(self):
        """Draw the pattern in the Rhino scene using the current settings."""
        layer = self.settings['layer']

        self.artist.layer = layer
        self.artist.clear_layer()

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        # group_supports = "{}::supports".format(group_vertices)
        # group_fixed = "{}::fixed".format(group_vertices)
        # group_free = "{}::free".format(group_vertices)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        # if not compas_rhino.rs.IsGroup(group_supports):
        #     compas_rhino.rs.AddGroup(group_supports)

        # if not compas_rhino.rs.IsGroup(group_fixed):
        #     compas_rhino.rs.AddGroup(group_fixed)

        # if not compas_rhino.rs.IsGroup(group_free):
        #     compas_rhino.rs.AddGroup(group_free)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        # vertices

        guids_vertices = list(self.guid_vertex.keys())
        delete_objects(guids_vertices, purge=True)

        # supports = list(self.datastructure.vertices_where({'is_anchor': True}))
        # fixed = list(self.datastructure.vertices_where({'is_fixed': True}))
        # free = list(self.datastructure.vertices_where({'is_anchor': False, 'is_fixed': False}))
        # keys = supports + fixed + free

        keys = list(self.datastructure.vertices())

        color = {key: self.settings['color.vertices'] for key in keys}
        color_fixed = self.settings['color.vertices:is_fixed']
        color_anchor = self.settings['color.vertices:is_anchor']
        color.update({key: color_fixed for key in self.datastructure.vertices_where({'is_fixed': True}) if key in keys})
        color.update({key: color_anchor for key in self.datastructure.vertices_where({'is_anchor': True}) if key in keys})

        guids = self.artist.draw_vertices(keys, color)
        self.guid_vertex = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)
        # key_guid = dict(zip(keys, guids))
        # compas_rhino.rs.AddObjectsToGroup([key_guid[key] for key in supports], group_supports)
        # compas_rhino.rs.AddObjectsToGroup([key_guid[key] for key in fixed], group_fixed)
        # compas_rhino.rs.AddObjectsToGroup([key_guid[key] for key in free], group_free)

        if self.settings['show.vertices']:
            compas_rhino.rs.ShowGroup(group_vertices)
            # compas_rhino.rs.ShowGroup(group_supports)
            # compas_rhino.rs.ShowGroup(group_fixed)
            # compas_rhino.rs.ShowGroup(group_free)
        else:
            compas_rhino.rs.HideGroup(group_vertices)
            # compas_rhino.rs.ShowGroup(group_supports)
            # compas_rhino.rs.ShowGroup(group_fixed)
            # compas_rhino.rs.HideGroup(group_free)

        # edges

        guids_edges = list(self.guid_edge.keys())
        delete_objects(guids_edges, purge=True)

        keys = list(self.datastructure.edges())
        color = {key: self.settings['color.edges'] for key in keys}
        guids = self.artist.draw_edges(keys, color)
        self.guid_edge = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings['show.edges']:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # faces

        guids_faces = list(self.guid_face.keys())
        delete_objects(guids_faces, purge=True)

        keys = list(self.datastructure.faces())
        color = {key: self.settings['color.faces'] for key in keys}
        guids = self.artist.draw_faces(keys, color)
        self.guid_face = zip(guids, keys)
        compas_rhino.rs.AddObjectsToGroup(guids, group_faces)

        if self.settings['show.faces']:
            compas_rhino.rs.ShowGroup(group_faces)
        else:
            compas_rhino.rs.HideGroup(group_faces)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

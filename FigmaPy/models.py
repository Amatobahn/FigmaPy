# API Scope Resource Objects


class File:
    def __init__(self, name, document, components, last_modified, thumbnail_url, schema_version, styles):
        self.name = name
        self.last_modified = last_modified
        self.thumbnail_url = thumbnail_url
        self.document = document
        self.components = components
        self.schema_version = schema_version
        self.styles = styles


class FileImages:
    def __init__(self, images, err):
        self.err = err
        self.images = images


class FileVersions:
    def __init__(self, versions, pagination):
        self.versions = versions
        self.pagination = pagination


class Comments:
    def __init__(self, comments):
        self.comments = None

        if len(comments) > 0 or comments is not None:
            self.comments = []
            for comment in comments:
                self.comments.append(Comment(comment['id'], comment['file_key'], comment['parent_id'], comment['user'],
                                             comment['created_at'], comment['resolved_at'], comment['message'],
                                             comment['client_meta'], comment['order_id']))


class TeamProjects:
    def __init__(self, projects):
        self.projects = projects

    def get_project_name_by_id(self, id):
        for project in self.projects:
            if project['id'] == id:
                return project['name']

    def get_project_id_by_name(self, name):
        for project in self.projects:
            if project['name'] == name:
                return project['id']


class ProjectFiles:
    def __init__(self, files):
        self.files = files


# -------------------------------------------------------------------------
# NODE PROPERTIES
# -------------------------------------------------------------------------
class Document:
    # The root node
    def __init__(self, children):
        self.children = children  # An array of canvases attached to the document


class Canvas:
    # Represents a single page
    def __init__(self, children, background_color, export_settings=None):
        self.children = children  # An array of top level layers on the canvas
        self.background_color = background_color  # Background color of the canvas
        self.export_settings = export_settings  # An array of export settings representing images to export. Default: []


class Frame:
    # A node of fixed size containing other nodes
    def __init__(self, children, background_color, blend_mode, constraints, abs_bounding_box, size,
                 relative_transform, clips_content, preserve_ratio=False, transition_node_id=None, opacity=1,
                 layout_grids=None, effects=None, is_mask=False, export_settings=None):
        self.children = children  # An array of nodes that are direct children of this node
        self.background_color = background_color  # Background color of the node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.clips_content = clips_content  # Does this node clip content outside of its bounds?
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.layout_grids = layout_grids  # An array of layout grids attached to this node
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.export_settings = export_settings  # An array of export settings representing images to export from node


class Group:
    # A logical grouping of nodes [Holds properties of Frame except for layout_grids]
    def __init__(self, children, background_color, blend_mode, constraints, abs_bounding_box, size,
                 relative_transform, clips_content, preserve_ratio=False, transition_node_id=None, opacity=1,
                 effects=None, is_mask=False, export_settings=None):
        self.children = children  # An array of nodes that are direct children of this node
        self.background_color = background_color  # Background color of the node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.clips_content = clips_content  # Does this node clip content outside of its bounds?
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.export_settings = export_settings  # An array of export settings representing images to export from node


class Vector:
    # A vector network, consisting of vertices and edges
    def __init__(self, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Boolean:
    # A vector network, consisting of vertices and edges
    def __init__(self, children, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.children = children  # An array of nodes that are being boolean operated on
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Star:
    # A regular star shape [Shares properties of Vector]
    def __init__(self, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Line:
    # A straight line [Shares properties of Vector]
    def __init__(self, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Ellipse:
    # An ellipse [Shares properties of Vector]
    def __init__(self, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class RegularPolygon:
    # A regular n-sided polygon [Shares properties of Vector]
    def __init__(self, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Rectangle:
    # A rectangle [Shares properties of Vector plus corner_radius]
    def __init__(self, corner_radius, blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.corner_radius = corner_radius  # Radius of each corner of the rectangle
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Text:
    # A regular n-sided polygon [Shares properties of Vector]
    # plus characters, style, character_style_overrides, and style_override_table
    def __init__(self, characters, style, character_style_overrides, style_override_table,
                 blend_mode, constraints, abs_bounding_box, size, relative_transform, fill_geometry,
                 stroke_weight, stroke_geometry, stroke_align, export_settings=None, preserve_ratio=False,
                 transition_node_id=None, opacity=1, effects=None, is_mask=False, fills=None, strokes=None):
        self.characters = characters  # Text contained within text box
        self.style = style  # Style of text including font family and weight
        self.character_style_overrides = character_style_overrides  # Array with same number of elements as characters
        self.style_override_table = style_override_table  # Map from ID to TypeStyle for looking up style overrides
        self.export_settings = export_settings  # An array of export settings representing images to export from node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fill_geometry = fill_geometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.stroke_weight = stroke_weight  # The weight of strokes on the node
        self.stroke_geometry = stroke_geometry  # An array of paths representing the object stroke
        self.stroke_align = stroke_align  # Where stroke is drawn relative to vector outline as a string enum


class Slice:
    # A rectangular region of the canvas that can be exported
    def __init__(self, export_settings, abs_bounding_box, size, relative_transform):
        self.export_settings = export_settings  # An array of export settings of images to export from this node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry


class Component:
    # A node that can have instances created of it that share the same properties
    def __init__(self, children, background_color, blend_mode, constraints, abs_bounding_box, size,
                 relative_transform, clips_content, preserve_ratio=False, transition_node_id=None, opacity=1,
                 layout_grids=None, effects=None, is_mask=False, export_settings=None):
        self.children = children  # An array of nodes that are direct children of this node
        self.background_color = background_color  # Background color of the node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.clips_content = clips_content  # Does this node clip content outside of its bounds?
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.layout_grids = layout_grids  # An array of layout grids attached to this node
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.export_settings = export_settings  # An array of export settings representing images to export from node


class Instance:
    # An instance of a component, changes to the component result in the same changes applied to the instance
    def __init__(self, children, background_color, blend_mode, constraints, abs_bounding_box, size, component_id,
                 relative_transform, clips_content, preserve_ratio=False, transition_node_id=None, opacity=1,
                 layout_grids=None, effects=None, is_mask=False, export_settings=None):
        self.component_id = component_id  # ID of component that this instance came from - refers to components table
        self.children = children  # An array of nodes that are direct children of this node
        self.background_color = background_color  # Background color of the node
        self.blend_mode = blend_mode  # How this node blends with nodes behind it in the scene
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.absolute_bounding_box = abs_bounding_box  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relative_transform = relative_transform  # Use to transform coordinates in geometry.
        self.clips_content = clips_content  # Does this node clip content outside of its bounds?
        self.preserve_ratio = preserve_ratio  # Keep height and width constrained to same ratio
        self.transition_node_id = transition_node_id  # Node ID of node to transition to in prototyping
        self.opacity = opacity  # Opacity of the node
        self.layout_grids = layout_grids  # An array of layout grids attached to this node
        self.effects = effects  # An array of effects attached to this node
        self.is_mask = is_mask  # Does this node mask sibling nodes in front of it?
        self.export_settings = export_settings  # An array of export settings representing images to export from node


# -------------------------------------------------------------------------
# FILE FORMAT TYPES
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# GENERAL API TYPES
# -------------------------------------------------------------------------
class Comment:
    # A comment or reply left by a user
    def __init__(self, id, file_key, parent_id, user, created_at, resolved_at, message, client_meta, order_id):
        self.id = id  # Unique identifier for comment
        self.file_key = file_key  # The file in which the comment lives
        self.parent_id = parent_id  # If present, the id of the comment to which this is the reply
        self.user = user  # The user who left the comment
        self.created_at = created_at  # The UTC ISO 8601 time at which the comment was left
        self.resolved_at = resolved_at  # If set, the UTC ISO 8601 time the comment was resolved
        self.message = message  # Content of comment
        self.client_meta = client_meta  # The position of the comment. Absolute coordinates or relative offset
        self.order_id = order_id  # Only set for top level comments. The number displayed with the comment in the UI


class User:
    # A description of a user
    def __init__(self, handle, img_url):
        self.handle = handle  # Name of the user
        self.img_url = img_url  # URL link to the user's profile image


class Version:
    # A version of a file
    def __init__(self, id, created_at, label, description, user):
        self.id = id  # Unique identifier for version
        self.created_at = created_at  # the UTC ISO 8601 time at which the version was created
        self.label = label  # The label given to the version in the editor
        self.description = description  # The description of the version as entered in the editor
        self.user = user  # The user that created the version

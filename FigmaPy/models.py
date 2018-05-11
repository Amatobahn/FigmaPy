# API Scope Resource Objects
from enum import Enum


class File:
    # JSON file contents from a file
    def __init__(self, name, document, components, last_modified, thumbnail_url, schema_version, styles):
        self.name = name  # File name
        self.last_modified = last_modified  # Date file was last modified
        self.thumbnail_url = thumbnail_url  # File thumbnail URL
        self.document = document  # Document content from a file
        self.components = components  # Document components from a file
        self.schema_version = schema_version  # Schema version from a file
        self.styles = styles  # Styles contained within a file


class FileImages:
    # URLs for server-side rendered images from a file
    def __init__(self, images, err):
        self.err = err  # Error type as enum string
        self.images = images  # URLs of server-side rendered images from a file


class FileVersions:
    # Version history from a file
    def __init__(self, versions, pagination):
        self.versions = versions  # Version from a file
        self.pagination = pagination  # Pagination from a file


class Comments:
    # Comment(s) from a file
    def __init__(self, comments):
        self.comments = None  # Comment(s) from a file

        if len(comments) > 0 or comments is not None:
            self.comments = []
            for comment in comments:
                self.comments.append(Comment(comment['id'], comment['file_key'], comment['parent_id'], comment['user'],
                                             comment['created_at'], comment['resolved_at'], comment['message'],
                                             comment['client_meta'], comment['order_id']))


class TeamProjects:
    # Projects from a team
    def __init__(self, projects):
        self.projects = projects  # Projects from a team

    def get_project_name_by_id(self, id):
        for project in self.projects:
            if project['id'] == id:
                return project['name']

    def get_project_id_by_name(self, name):
        for project in self.projects:
            if project['name'] == name:
                return project['id']


class ProjectFiles:
    # Files from a project
    def __init__(self, files):
        self.files = files  # Files from a project


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
class Color:
    # An RGBA Color
    def __init__(self, r, g, b, a):
        self.r = r  # Red channel value, between 0 and 1
        self.g = g  # Green channel value, between 0 and 1
        self.b = b  # Blue channel value, between 0 and 1
        self.a = a  # Alpha channel value, between 0 and 1


class ExportSetting:
    # Format and size to export an asset at
    def __init__(self, suffix, format, constraint):
        self.suffix = suffix  # File suffix to append all file names
        self.format = format  # Image type, string enum that supports values 'JPG', 'PNG', and 'SVG'
        self.constraint = constraint  # Constraint that determines sizing of exported asset


class Constraint:
    # Sizing constraint for exports
    def __init__(self, type, value):
        self.type = type  # Type of constraint to apply; string enum with potential values 'SCALE', 'WIDTH', 'HEIGHT'
        self.value = value  # See type property for effect of this field


class Rect:
    # A rectangle that expresses a bounding box in absolute coordinates
    def __init__(self, x, y, width, height):
        self.x = x  # X coordinate of top left corner of the rectangle
        self.y = y  # Y coordinate of top left corner of the rectangle
        self.width = width  # Width of the rectangle
        self.height = height  # Height of the rectangle


class BlendMode(Enum):
    # Enum describing how layer blens with layers below
    # This type is a string enum with the following possible values:

    # Normal Blends
    PASS_THROUGH = 'PASS_THROUGH'
    NORMAL = 'NORMAL'
    # Darken
    DARKEN = 'DARKEN'
    MULTIPLY = 'MULTIPLY'
    LINEAR_BURN = 'LINEAR_BURN'
    COLOR_BURN = 'COLOR_BURN'
    # Lighten
    LIGHTEN = 'LIGHTEN'
    SCREEN = 'SCREEN'
    LINEAR_DODGE = 'LINEAR_DODGE'
    COLOR_DODGE = 'COLOR_DODGE'
    # Contrast
    OVERLAY = 'OVERLAY'
    SOFT_LIGHT = 'SOFT_LIGHT'
    HARD_LIGHT = 'HARD_LIGHT'
    # Inversion
    DIFFERENCE = 'DIFFERENCE'
    EXCLUSION = 'EXCLUSION'
    # Component
    HUE = 'HUE'
    SATURATION = 'SATURATION'
    COLOR = 'COLOR'
    LUMINOSITY = 'LUMINOSITY'


class LayoutConstraint:
    # Layout constraint relative to containing Frame
    def __init__(self, vertical, horizontal):
        self.vertical = vertical  # Vertical constraint as an enum
        self.horizontal = horizontal  # Horizontal constraint as an enum


class LayoutGrid:
    # Guides to align and place objects within a frame
    def __init__(self, pattern, section_size, visible, color, alignment, gutter_size, offset, count):
        self.pattern = pattern  # Orientatoin of the grid as a string enum
        self.section_size = section_size  # Width of column grid or height of row grid or square grid spacing
        self.visible = visible  # Is the grid currently visible?
        self.color = color  # Color of the grid
        # The following properties are only meaningful for directional grids (COLUMNS or ROWS)
        self.alignment = alignment  # Positioning of grid as a string enum
        self.gutter_size = gutter_size  # Spacing in between columns and rows
        self.offset = offset  # Spacing before the first column or row
        self.count = count  # Number of columns or rows


class Effect:
    # A visual effect such as a shadow or blur
    def __init__(self, type, visible, radius, color, blend_mode, offset):
        self.type = type  # Type of effect as a string enum
        self.visible = visible  # is the effect active?
        self.radius = radius  # Radius of the blur effect (applies to shadows as well)
        # The following properties are for shadows only:
        self.color = color  # The color of the shadow
        self.blend_mode = blend_mode  # Blend mode of the shadow
        self.offset = offset  # How far the shadow is projected in the x and y directions


class Paint:
    # A solid color, gradient, or image texture that can be applied as fills or strokes
    def __init__(self, type, color, gradient_handle_positions, gradient_stops, scale_mode,
                 visible=True, opacity=1):
        self.type = type  # Type of paint as a string enum
        self.visible = visible  # Is the paint enabled?
        self.opacity = opacity  # Overall opacity of paint (colors within the paint can also have opacity values)
        self.color = color  # Solid color of the paint
        # For gradient paints:
        self.gradient_handle_positions = gradient_handle_positions  # Three vectors, each are pos in normalized space
        self.gradient_stops = gradient_stops  # Positions of key points along the gradient axis with the anchored colors
        # For image paints:
        self.scale_mode = scale_mode  # Image scaling mode


class Vector2d:
    # A 2d vector
    def __init__(self, x, y):
        self.x = x  # X coordinate of the vector
        self.y = y  # Y coordinate of the vector


class Transform:
    # A 2x3 2D affine transformation matrix
    def __init__(self, matrix):
        self.matrix = matrix  # Transformation matrix


class Path:
    # A vector path
    def __init__(self, path, winding_rule):
        self.path = path  # A sequence of path commands in SVG notation
        self.winding_rule = winding_rule  # Winding rule for the path, either 'EVENODD' or 'NONZERO'


class FrameOffset:
    # A relative offset within a frame
    def __init__(self, node_id, node_offset):
        self.node_id = node_id  # Unique id specifying the frame
        self.node_offset = node_offset  # 2d vector offset within the frame


class ColorStop:
    # A position color pair representing a gradient stop
    def __init__(self, position, color):
        self.position = position  # Value between 0 and 1 representing position along gradient axis
        self.color = color  # Color attached to corresponding position


class TypeStyle:
    # Metadata for character formatting
    def __init__(self, font_family, font_post_script_name, italic, font_weight, font_size, text_align_horizontal,
                 text_align_vertical, letter_spacing, fills, line_height_px, line_height_percent):
        self.font_family = font_family  # Font family of text (standard name)
        self.font_post_script_name = font_post_script_name  # PostScript font name
        self.italic = italic  # Is text italicized?
        self.font_weight = font_weight  # Numeric font weight
        self.font_size = font_size  # Font size in px
        self.text_align_horizontal = text_align_horizontal  # Horizontal text alignment as string enum
        self.text_align_vertical = text_align_vertical  # Vertical text alignment as string enum
        self.letter_spacing = letter_spacing  # Space between characters in px
        self.fills = fills  # Paints applied to characters
        self.line_height_px = line_height_px  # Line height in px
        self.line_height_percent = line_height_percent  # Line height as a percentage of normal line height


class ComponentDescription:
    # A description of a master component. Helps you identify which component instances are attached to
    def __init__(self, name, description):
        self.name = name  # The name of the component
        self.description = description  # The description of the component as entered in the editor


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

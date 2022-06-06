# API Scope Resource Objects
import pprint
from enum import Enum


"""
TEAM
└─ USER(s)

PROJECT (collection of files which belong to user or team)
└─ FILES
    └─ VERSIONS
    └─ COMMENTS
    └─ DOCUMENT
        └─  CANVAS / PAGES
            └─  NODES
                └─ NODES (optional children)
                    └─  ...

COMPONENTS (metadata / styles in a team library)

requested data is returned as a dict / JSON
this python wrapper is used to convert the dict to a python object, and adds meta data such as parent of node
"""

def deserialize_properties(self):
    """
    deserialize properties to their matching type
    """
    if hasattr(self, 'color') and isinstance(self.color, dict) and self.color is not None:
        self.color = Color(**self.color)
    if hasattr(self, 'constraint') and isinstance(self.constraint, dict) and self.constraint is not None:
        self.constraint = Constraint(**self.constraint)
    if hasattr(self, 'absoluteBoundingBox') and isinstance(self.absoluteBoundingBox,
                                                           dict) and self.absoluteBoundingBox is not None:
        self.absoluteBoundingBox = Rect(**self.absoluteBoundingBox)
    if hasattr(self, 'blendMode') and isinstance(self.blendMode, str) and self.blendMode is not None:
        self.blendMode = BlendMode[self.blendMode]

    if hasattr(self, 'constraints') and isinstance(self.constraints, list) and self.constraints is not None:
        self.constraints = [Constraint(**constraint) for constraint in self.constraints]
    if hasattr(self, 'layoutGrids') and isinstance(self.layoutGrids, list) and self.layoutGrids is not None:
        self.layoutGrids = [LayoutGrid(**grid) for grid in self.layoutGrids]
    if hasattr(self, 'children') and isinstance(self.children, list) and self.children is not None:
        self.children = [self.deserialize(child) for child in self.children]
        if self:
            for child in self.children:
                child.parent = self
    if hasattr(self, 'fillGeometry') and isinstance(self.fillGeometry, list) and self.fillGeometry is not None:
        self.fillGeometry = [Path(**path) for path in self.fillGeometry]
    if hasattr(self, 'strokeGeometry') and isinstance(self.strokeGeometry, list) and self.strokeGeometry is not None:
        self.strokeGeometry = [Path(**path) for path in self.strokeGeometry]
    if hasattr(self, 'exportSettings') and isinstance(self.exportSettings, list) and self.exportSettings is not None:
        self.exportSettings = [ExportSetting(**setting) for setting in self.exportSettings]
    if hasattr(self, 'fills') and isinstance(self.fills, list) and self.fills is not None:
        self.fills = [Paint(**paint, pythonParent=self) for paint in self.fills]
    if hasattr(self, 'strokes') and isinstance(self.strokes, list) and self.strokes is not None:
        self.strokes = [Paint(**paint, pythonParent=self) for paint in self.strokes]
    if hasattr(self, 'effects') and isinstance(self.effects, list) and self.effects is not None:
        self.effects = [Effect(**effect) for effect in self.effects]


class File:
    # JSON file contents from a file
    def __init__(self, name, document, components, lastModified, thumbnailUrl, schemaVersion, styles, file_key=None, pythonParent=None):
        self.name = name  # File name
        self.lastModified = lastModified  # Date file was last modified
        self.thumbnailUrl = thumbnailUrl  # File thumbnail URL
        self.document = Document(**document, pythonParent=self)  # Document content from a file
        self.components = components  # Document components from a file
        self.schemaVersion = schemaVersion  # Schema version from a file
        self.styles = styles  # Styles contained within a file

        # python helpers
        self.file_key = file_key
        self.pythonParent = pythonParent

    def get_file_key(self):
        return self.file_key

class FileImages:
    # URLs for server-side rendered images from a file
    # https://www.figma.com/developers/api#get-images-endpoint
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

# for node types, we store every property mentioned in the figma API, in the order they are mentioned
# see https://www.figma.com/developers/api#node-types

class Node:
    def __init__(self, id, name, type, visible=True, pluginData=None, sharedPluginData=None, pythonParent=None, *args, **kwargs):
        # figma data
        self.id = id  # A string uniquely identifying this node within the document.
        self.name = name  # The name given to the node by the user in the tool.
        self.visible = visible  # Whether or not the node is visible on the canvas.
        self.type = type  # The type of the node
        self.pluginData = pluginData  # Data written by plugins that is visible only to the plugin that wrote it. Requires the `pluginData` to include the ID of the plugin.
        self.sharedPluginData = sharedPluginData  # Data written by plugins that is visible to all plugins. Requires the `pluginData` parameter to include the string "shared

        # python helpers
        self.pythonParent = pythonParent  # The python parent of this node. which holds this node.
        self.deserialize_properties()

        if args or kwargs:
            print("Node class has been instantiated with unsupported args and kwargs."
                  "this is likely due to a change in the Figma API, or an unsupported parameter in this wrapper")
            print(args, kwargs)
            print(self)

    def deserialize_properties(self):
        """
        deserialize properties to their matching type
        """
        return deserialize_properties(self)


    def deserialize(self, node_dict):
        """
        convert a json/dict into a figma node

        Deserialize a dictionary into a figma node.
        The keys in the dict need to match the names of the properties in our Node classes.
        this ensures the dicts returned by the figma API can be loaded directly into our classes.

        :param children: list of dictionaries
        :return:
        """
        if node_dict is None:
            return
        node_type = NodeTypes[node_dict.get('type')]
        node = node_type.value(**node_dict, pythonParent=self)
        return node

    def get_children_recursively(self):
        """
        get all children of this node, recursively.
        """
        nodes_found = []
        for node in self.children:
            nodes_found.append(node)
            if hasattr(node, 'children'):
                node.get_children_recursively()
        return nodes_found

    # @staticmethod
    # def serialize(node):
    #     raise NotImplementedError
    #     # TODO: implement

    def get_file_key(self):
        return get_file_key(self)


class Document(Node):
    # The root node
    def __init__(self,
                 children,
                 *args, **kwargs):
        self.children = children  # An array of canvases attached to the document
        super().__init__(*args, **kwargs)


class Canvas(Node):
    # Represents a single page
    def __init__(self,
                 children,
                 backgroundColor,
                 prototypeStartNodeID=None,
                 prototypeDevice=None,
                 flowStartingPoints=None,
                 exportSettings=None,
                 *args, **kwargs):
        self.children = children  # An array of top level layers on the canvas
        self.backgroundColor = backgroundColor  # Background color of the canvas
        self.prototypeStartNodeID = prototypeStartNodeID  # DEPRECATED] Node ID that corresponds to the start frame for prototypes. This is deprecated with the introduction of multiple flows. Please use the flowStartingPoints field.
        self.prototypeDevice = prototypeDevice
        self.flowStartingPoints = flowStartingPoints  # An array of flow starting points sorted by its position in the prototype settings panel.
        self.exportSettings = exportSettings  # An array of export settings representing images to export. Default: []
        super().__init__(*args, **kwargs)


class Frame(Node):
    # A node of fixed size containing other nodes
    def __init__(self,
                 children,
                 background,
                 backgroundColor,
                 blendMode,
                 constraints,
                 absoluteBoundingBox,
                 clipsContent,
                 size=None,
                 relativeTransform=None,
                 locked=False,
                 fills=None,
                 strokes=None,
                 strokeWeight=None,
                 strokeAlign=None,
                 cornerRadius=None,
                 rectangleCornerRadii=None,
                 preserveRatio=False,
                 layoutAlign=None,
                 transitionNodeID=None,
                 transitionDuration=None,
                 transitionEasing=None,
                 opacity=1,
                 exportSettings=None,
                 primaryAxisSizingMode=None,
                 counterAxisSizingMode=None,
                 primaryAxisAlignItems=None,
                 counterAxisAlignItems=None,
                 paddingLeft=None,
                 paddingRight=None,
                 paddingTop=None,
                 paddingBottom=None,
                 horizontalPadding=None,
                 verticalPadding=None,
                 itemSpacing=None,
                 layoutGrids=None,
                 overflowDirection=None,
                 effects=None,
                 isMask=None,
                 layoutMode=None,
                 *args, **kwargs):
        self.children = children  # An array of nodes that are direct children of this node
        self.locked = locked  # If true, layer is locked and cannot be edited
        self.background = background  # [DEPRECATED] Background of the node. This is deprecated, as backgrounds for frames are now in the fills field.
        self.backgroundColor = backgroundColor  # [DEPRECATED] Background color of the node. This is deprecated, as frames now support more than a solid color as a background. Please use the fills field instead.
        self.fills = fills
        self.strokes = strokes
        self.strokeWeight = strokeWeight
        self.strokeAlign = strokeAlign
        self.cornerRadius = cornerRadius
        self.rectangleCornerRadii = rectangleCornerRadii
        self.exportSettings = exportSettings  # An array of export settings representing images to export from node
        self.blendMode = blendMode  # How this node blends with nodes behind it in the scene
        self.preserveRatio = preserveRatio  # Keep height and width constrained to same ratio
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.layoutAlign = layoutAlign
        self.transitionNodeID = transitionNodeID  # Node ID of node to transition to in prototyping
        self.transitionDuration = transitionDuration
        self.transitionEasing = transitionEasing
        self.opacity = opacity  # Opacity of the node
        self.absoluteBoundingBox = absoluteBoundingBox  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relativeTransform = relativeTransform  # Use to transform coordinates in geometry.
        self.clipsContent = clipsContent  # Does this node clip content outside of its bounds?
        self.layoutMode = layoutMode
        self.primaryAxisSizingMode = primaryAxisSizingMode
        self.counterAxisSizingMode = counterAxisSizingMode
        self.primaryAxisAlignItems = primaryAxisAlignItems
        self.counterAxisAlignItems = counterAxisAlignItems
        self.paddingLeft = paddingLeft
        self.paddingRight = paddingRight
        self.paddingTop = paddingTop
        self.paddingBottom = paddingBottom
        self.horizontalPadding = horizontalPadding
        self.verticalPadding = verticalPadding
        self.itemSpacing = itemSpacing
        self.layoutGrids = layoutGrids  # An array of layout grids attached to this node
        self.overflowDirection = overflowDirection
        self.effects = effects  # An array of effects attached to this node
        self.isMask = isMask  # Does this node mask sibling nodes in front of it?
        super().__init__(*args, **kwargs)


class Group(Frame):
    # A logical grouping of nodes [Holds properties of Frame except for layoutGrids]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Vector(Node):
    # A vector network, consisting of vertices and edges
    def __init__(self, blendMode, constraints, absoluteBoundingBox, size=None, relativeTransform=None,
                 fillGeometry=None,
                 strokeWeight=None, strokeGeometry=None, strokeAlign=None, exportSettings=None, preserveRatio=False,
                 transitionNodeID=None, opacity=1, transitionNodeDuration=None,
                 transitionEasing=None, layoutGrow=0, locked=False, layoutAlign=None, effects=None,
                 isMask=False, fills=None,
                 strokeJoin=None,
                 strokes=None,
                 strokeDashes=None,
                 strokeMiterAngle=None,
                 strokeCap=None,
                 styles=None,
                 *args, **kwargs):
        self.locked = locked  # If true, layer is locked and cannot be edited
        self.exportSettings = exportSettings  # An array of export settings representing images to export from node
        self.blendMode = blendMode  # How this node blends with nodes behind it in the scene
        self.preserveRatio = preserveRatio  # Keep height and width constrained to same ratio
        self.layoutAlign = layoutAlign
        self.layoutGrow = layoutGrow
        self.constraints = constraints  # Horizontal and vertical layout constraints for node
        self.transitionNodeID = transitionNodeID  # Node ID of node to transition to in prototyping
        self.transitionNodeDuration = transitionNodeDuration
        self.transitionEasing = transitionEasing
        self.opacity = opacity  # Opacity of the node
        self.absoluteBoundingBox = absoluteBoundingBox  # Bounding box of the node in absolute space coordinates
        self.effects = effects  # An array of effects attached to this node
        self.size = size  # Width and height of element. Only present if geometry=paths is passed
        self.relativeTransform = relativeTransform  # Use to transform coordinates in geometry.
        self.isMask = isMask  # Does this node mask sibling nodes in front of it?
        self.fills = fills  # An array of fill paints applied to the node
        self.fillGeometry = fillGeometry  # An array of paths representing the object fill
        self.strokes = strokes  # An array of stroke paints applied to the node
        self.strokeWeight = strokeWeight  # The weight of strokes on the node
        self.strokeCap = strokeCap
        self.strokeJoin = strokeJoin
        self.strokeDashes = strokeDashes
        self.strokeMiterAngle = strokeMiterAngle
        self.strokeGeometry = strokeGeometry  # An array of paths representing the object stroke
        self.strokeAlign = strokeAlign  # Where stroke is drawn relative to vector outline as a string enum
        self.styles = styles
        super().__init__(*args, **kwargs)


class BooleanOperation(Vector):
    # A vector network, consisting of vertices and edges
    def __init__(self, children, booleanOperation, *args, **kwargs):
        self.children = children  # An array of nodes that are direct children of this node
        self.booleanOperation = booleanOperation
        super().__init__(*args, **kwargs)


class Star(Vector):
    # A regular star shape [Shares properties of Vector]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Line(Vector):
    # A straight line [Shares properties of Vector]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ellipse(Vector):
    # An ellipse [Shares properties of Vector]
    def __init__(self, arcData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arcData = arcData


class RegularPolygon(Vector):
    # A regular n-sided polygon [Shares properties of Vector]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Rectangle(Vector):
    # A rectangle [Shares properties of Vector plus cornerRadius]
    def __init__(self, cornerRadius=None, rectangleCornerRadii=None, *args, **kwargs):
        self.cornerRadius = cornerRadius  # Radius of each corner of the rectangle
        self.rectangleCornerRadii = rectangleCornerRadii
        super().__init__(*args, **kwargs)


class Text(Vector):
    # A regular n-sided polygon [Shares properties of Vector]
    # plus characters, style, characterStyleOverrides, and styleOverrideTable
    def __init__(self, characters, style, characterStyleOverrides, styleOverrideTable, lineTypes, lineIndentations,
                 layoutVersion=None,
                 *args, **kwargs):
        self.characters = characters  # Text contained within text box
        self.style = style  # Style of text including font family and weight
        self.characterStyleOverrides = characterStyleOverrides  # Array with same number of elements as characters
        self.styleOverrideTable = styleOverrideTable  # Map from ID to TypeStyle for looking up style overrides
        self.lineTypes = lineTypes
        self.lineIndentations = lineIndentations
        self.layoutVersion = layoutVersion  # -> int, not documented in figma API
        super().__init__(*args, **kwargs)


class Slice(Node):
    # A rectangular region of the canvas that can be exported
    def __init__(self, exportSettings, absoluteBoundingBox, size, relativeTransform, *args, **kwargs):
        self.exportSettings = exportSettings  # An array of export settings of images to export from this node
        self.absoluteBoundingBox = absoluteBoundingBox  # Bounding box of the node in absolute space coordinates
        self.size = size  # Width and height of element
        self.relativeTransform = relativeTransform  # Use to transform coordinates in geometry
        super().__init__(*args, **kwargs)


class Component(Frame):
    # A node that can have instances created of it that share the same properties
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ComponentSet(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Instance(Frame):
    # An instance of a component, changes to the component result in the same changes applied to the instance
    def __init__(self, component_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component_id = component_id  # ID of component that this instance came from - refers to components table


class Sticky(Node):
    # FigJam Sticky node
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Sticky is not implemented yet")
        super().__init__(*args, **kwargs)


class ShapeWithText(Node):
    # FigJam Shape-with-text node
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("ShapeWithText is not implemented")
        super().__init__(*args, **kwargs)


class Connector(Node):
    # FigJam Connector node
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Connector is not implemented yet")
        super().__init__(*args, **kwargs)


class NodeTypes(Enum):
    # Enum describing node types
    # This type is a string enum with the following possible values:
    DOCUMENT = Document
    CANVAS = Canvas
    FRAME = Frame
    GROUP = Group
    VECTOR = Vector
    BOOLEAN_OPERATION = BooleanOperation
    STAR = Star
    LINE = Line
    ELLIPSE = Ellipse
    REGULAR_POLYGON = RegularPolygon
    RECTANGLE = Rectangle
    TEXT = Text
    SLICE = Slice
    COMPONENT = Component
    COMPONENT_SET = ComponentSet
    INSTANCE = Instance
    STICKY = Sticky
    SHAPE_WITH_TEXT = ShapeWithText
    CONNECTOR = Connector


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
    def __init__(self, pattern, sectionSize, visible, color, alignment, gutterSize, offset, count):
        self.pattern = pattern  # Orientatoin of the grid as a string enum
        self.sectionSize = sectionSize  # Width of column grid or height of row grid or square grid spacing
        self.visible = visible  # Is the grid currently visible?
        self.color = color # Color of the grid
        # The following properties are only meaningful for directional grids (COLUMNS or ROWS)
        self.alignment = alignment  # Positioning of grid as a string enum
        self.gutterSize = gutterSize  # Spacing in between columns and rows
        self.offset = offset  # Spacing before the first column or row
        self.count = count  # Number of columns or rows


class Effect:
    # A visual effect such as a shadow or blur
    def __init__(self, type, visible, radius, color, blendMode, offset):
        self.type = type  # Type of effect as a string enum
        self.visible = visible  # is the effect active?
        self.radius = radius  # Radius of the blur effect (applies to shadows as well)
        # The following properties are for shadows only:
        self.color = color # The color of the shadow
        self.blendMode = blendMode  # Blend mode of the shadow
        self.offset = offset  # How far the shadow is projected in the x and y directions


class Paint:
    # A solid color, gradient, or image texture that can be applied as fills or strokes
    def __init__(self, type,
                 color=None,
                 gradientHandlePositions=None,
                 gradientStops=None,
                 scaleMode=None,
                 blendMode=None,
                 imageTransform=None,
                 scalingFactor=None,
                 rotation=None,
                 imageRef=None,
                 filters=None,
                 gifRef=None,
                 visible=True,
                 opacity=1,
                 pythonParent=None):
        self.type = type  # Type of paint as a string enum
        self.visible = visible  # Is the paint enabled?
        self.opacity = opacity  # Overall opacity of paint (colors within the paint can also have opacity values)
        self.blendMode = blendMode

        # For solid paints:
        self.color = color  # Solid color of the paint

        # For gradient paints:
        self.gradientHandlePositions = gradientHandlePositions  # Three vectors, each are pos in normalized space
        self.gradientStops = gradientStops  # Positions of key points along the gradient axis with the anchored colors

        # For image paints:
        self.scaleMode = scaleMode  # Image scaling mode
        self.imageTransform = imageTransform
        self.scalingFactor = scalingFactor
        self.rotation = rotation
        self.imageRef = imageRef
        self.filters = filters
        self.gifRef = gifRef

        # todo move to decorator
        self.pythonParent = pythonParent

    def get_image_url(self):
        """get url of image"""
        if self.imageRef is None:
            return

        # TODO get attr from parent
        root_parent = self.pythonParent  # get FigmaPy instance
        while hasattr(root_parent, 'pythonParent'):
            root_parent = root_parent.pythonParent

        file_images = root_parent.get_file_images(file_key=self.get_file_key(),
                                                  ids=[self.pythonParent.id],
                                                  format='svg')

        # img_url_dict = root_parent.get_image_fills(file_key=self.get_file_key())
        # return img_url_dict['meta']['images'][self.imageRef]



    # todo property get setter
    def get_file_key(self):
        return get_file_key(self)


# todo property get setter
def get_file_key(node):
    if hasattr(node, 'file_key'):
        return node.file_key
    # return pythonParent.file_key  # todo property get setter
    return node.pythonParent.get_file_key()


class Vector2d:
    # A 2d vector
    def __init__(self, x, y):
        self.x = x  # X coordinate of the vector
        self.y = y  # Y coordinate of the vector


class Transform:
    # A 2x3 2D affine transformation matrix
    def __init__(self, matrix):
        self.matrix = matrix  # Transformation matrix


# not documented in the usual figma doc page: https://www.figma.com/developers/api
# instead see https://www.figma.com/plugin-docs/api/VectorPath/#docsNav
class Path:
    # A vector path
    def __init__(self, path, windingRule):
        self.path = path  # A sequence of path commands in SVG notation
        self.windingRule = windingRule  # Winding rule for the path, either 'EVENODD' or 'NONZERO'


class FrameOffset:
    # A relative offset within a frame
    def __init__(self, node_id, node_offset):
        self.node_id = node_id  # Unique id specifying the frame
        self.node_offset = Vector2d(**node_offset)  # 2d vector offset within the frame


class ColorStop:
    # A position color pair representing a gradient stop
    def __init__(self, position, color):
        self.position = position  # Value between 0 and 1 representing position along gradient axis
        self.color = color # Color attached to corresponding position


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

        deserialize_properties(self)


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

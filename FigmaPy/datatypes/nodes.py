from enum import Enum
from FigmaPy.utils import get_file_key
from .properties import deserialize_properties


# -------------------------------------------------------------------------
# NODE PROPERTIES
# -------------------------------------------------------------------------
# every property is wrapped in the order they are mentioned in the figma API
# see https://www.figma.com/developers/api#node-types


class Node:
    def __init__(self, id, name, type, visible=True, pluginData=None, sharedPluginData=None, pythonParent=None, *args,
                 **kwargs):
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
        # print('type:', node_type)
        # print('name:', node_dict.get('name'))
        # pprint.pprint(node_dict)
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

    def get_file_image_url(self):
        """
        get the image source url from the fill (paint) of this node.
        """
        # todo use export settings if found? they seem to be ignored by the figma API
        # if self.type == 'IMAGE':
        paint = self.fills[0]  # -> Paint
        return paint.get_file_image_url()

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
                 layoutGrow=None,
                 styles=None,
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
        self.layoutGrow = layoutGrow,
        self.styles = styles,
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
                 cornerRadius=None,
                 rectangleCornerRadii=None,
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
        self.cornerRadius = cornerRadius
        self.rectangleCornerRadii = rectangleCornerRadii
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
    def __init__(self, componentId=None, *args, **kwargs):
        self.componentId = componentId  # ID of component that this instance came from - refers to components table
        super().__init__(*args, **kwargs)


class Sticky(Node):
    def __init__(self, absoluteBoundingBox=None, authorVisible=None, backgroundColor=None, blendMode=None,
                 characters=None, effects=None, exportSettings=None, fills=None, isMask=None,
                 locked=None, opacity=None, relativeTransform=None, *args, **kwargs):
        self.absoluteBoundingBox = absoluteBoundingBox  # Rectangle: Bounding box of the node in absolute space coordinates
        self.authorVisible = authorVisible  # Boolean: If true, author name is visible.
        self.backgroundColor = backgroundColor  # Color: Background color of the canvas.
        self.blendMode = blendMode  # BlendMode: How this node blends with nodes behind it in the scene (see blend mode section for more details)
        self.characters = characters  # String: Text contained within a text box
        self.effects = effects  # Effect[]: An array of effects attached to this node (see effects section for more details)
        self.exportSettings = exportSettings  # ExportSetting[]: An array of export settings representing images to export from the node
        self.fills = fills  # Paint[]: An array of fill paints applied to the node
        self.isMask = isMask  # Boolean: Does this node mask sibling nodes in front of it?
        self.locked = locked  # Boolean: If true, sticky is locked and cannot be edited
        self.opacity = opacity  # Number: Overall opacity of paint (colors within the paint can also have opacity values which would blend with this)
        self.relativeTransform = relativeTransform  # Transform: The top two rows of a matrix that represents the 2D transform of this node relative to its parent. The bottom row of the matrix is implicitly always (0, 0, 1). Use to transform coordinates in geometry. Only present if geometry=paths is passed
        super().__init__(*args, **kwargs)


class ShapeWithText(Node):
    def __init__(self,
                 absoluteBoundingBox=None,
                 backgroundColor=None, blendMode=None, characters=None, cornerRadius=None, rectangleCornerRadii=None,
                 effects=None, exportSettings=None, fills=None, isMask=None,
                 locked=None, opacity=None, shapeType=None, strokes=None, strokeWeight=None, strokeCap=None,
                 strokeJoin=None, strokeDashes=None, strokeAlign=None, relativeTransform=None,
                 *args, **kwargs):
        self.absoluteBoundingBox = absoluteBoundingBox  # Rectangle: Bounding box of the node in absolute space coordinates
        self.backgroundColor = backgroundColor  # Color: Background color of the canvas.
        self.blendMode = blendMode  # BlendMode: How this node blends with nodes behind it in the scene (see blend mode section for more details)
        self.characters = characters  # String: Text contained within a text box
        self.cornerRadius = cornerRadius  # Number: Radius of each corner of the rectangle if a single radius is set for all corners
        self.rectangleCornerRadii = rectangleCornerRadii  # Number[]: Array of length 4 of the radius of each corner of the rectangle, starting in the top left and proceeding clockwise
        self.effects = effects  # Effect[]: An array of effects attached to this node (see effects section for more details)
        self.exportSettings = exportSettings  # ExportSetting[]: An array of export settings representing images to export from the node
        self.fills = fills  # Paint[]: An array of fill paints applied to the node
        self.isMask = isMask  # Boolean: Does this node mask sibling nodes in front of it?
        self.locked = locked  # Boolean: If true, sticky is locked and cannot be edited
        self.opacity = opacity  # Number: Overall opacity of paint (colors within the paint can also have opacity values which would blend with this)
        self.shapeType = shapeType  # ShapeType: Shape-with-text geometric shape type.
        self.strokes = strokes  # Paint[]: An array of stroke paints applied to the node
        self.strokeWeight = strokeWeight  # Number: The weight of strokes on the node
        self.strokeCap = strokeCap  # String: A string enum with value of "NONE", "ROUND", "SQUARE", "LINE_ARROW", or "TRIANGLE_ARROW", describing the end caps of vector paths.
        self.strokeJoin = strokeJoin  # String: A string enum with value of "MITER", "BEVEL", or "ROUND", describing how corners in vector paths are rendered.
        self.strokeDashes = strokeDashes  # Number[]: An array of floating point numbers describing the pattern of dash length and gap lengths that the vector path follows. For example a value of [1, 2] indicates that the path has a dash of length 1 followed by a gap of length 2, repeated.
        self.strokeAlign = strokeAlign  # String: Position of stroke relative to vector outline, as a string enum.
        self.relativeTransform = relativeTransform  # Transform: The top two rows of a matrix that represents the 2D transform of this node relative to its parent. The bottom row of the matrix is implicitly always (0, 0, 1). Use to transform coordinates in geometry. Only present if geometry=paths is passed
        super().__init__(*args, **kwargs)


class Connector(Node):
    def __init__(self,
                 absoluteBoundingBox=None,
                 backgroundColor=None, blendMode=None, characters=None, connectorStart=None, connectorEnd=None,
                 connectorLineType=None, cornerRadius=None, rectangleCornerRadii=None, effects=None,
                 exportSettings=None, fills=None, isMask=None,
                 locked=None, opacity=None, strokes=None, strokeWeight=None, strokeCap=None, strokeJoin=None,
                 strokeDashes=None, strokeAlign=None, relativeTransform=None, textBackground=None, *args, **kwargs):
        self.absoluteBoundingBox = absoluteBoundingBox  # Rectangle: Bounding box of the node in absolute space coordinates
        self.backgroundColor = backgroundColor  # Color: Background color of the canvas.
        self.blendMode = blendMode  # BlendMode: How this node blends with nodes behind it in the scene (see blend mode section for more details)
        self.characters = characters  # String: Text contained within a text box
        self.connectorStart = connectorStart  # ConnectorEndpoint: Connector starting endpoint.
        self.connectorEnd = connectorEnd  # ConnectorEndpoint: Connector ending endpoint.
        self.connectorLineType = connectorLineType
        self.cornerRadius = cornerRadius  # Number: Radius of each corner of the rectangle if a single radius is set for all corners
        self.rectangleCornerRadii = rectangleCornerRadii  # Number[] default: []
        self.effects = effects  # Effect[] default: []
        self.exportSettings = exportSettings  # ExportSetting[] default: []
        self.fills = fills  # Paint[] default: []
        self.isMask = isMask  # Boolean: Does this node mask sibling nodes in front of it?
        self.locked = locked  # Boolean: If true, connector is locked and cannot be edited
        self.opacity = opacity  # Number: Overall opacity of paint (colors within the paint can also have opacity values which would blend with this)
        self.strokes = strokes  # Paint[] default: []
        self.strokeWeight = strokeWeight  # Number: The weight of strokes on the node
        self.strokeCap = strokeCap  # String: A string enum with value of "NONE", "ROUND", "SQUARE", "LINE_ARROW", or "TRIANGLE_ARROW", describing the end caps of vector paths.
        self.strokeJoin = strokeJoin  # String: A string enum with value of "MITER", "BEVEL", or "ROUND", describing how corners in vector paths are rendered.
        self.strokeDashes = strokeDashes  # Number[] default: []
        self.strokeAlign = strokeAlign  # String: Position of stroke relative to vector outline, as a string enum
        self.textBackground = textBackground  # ConnectorTextBackground: Connector text background.
        self.relativeTransform = relativeTransform  # Transform: The top two rows of a matrix that represents the 2D transform of this node relative to its parent. The bottom row of the matrix is implicitly always (0, 0, 1). Use to transform coordinates in geometry. Only present if geometry=paths is passed
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

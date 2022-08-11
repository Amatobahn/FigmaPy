"""FILE FORMAT TYPES"""

from enum import Enum

from FigmaPy.utils import get_file_key


class Color:
    """An RGBA Color"""

    def __init__(self, r, g, b, a):
        """Create an instance of Color"""
        self.r = r  # Red channel value, between 0 and 1
        self.g = g  # Green channel value, between 0 and 1
        self.b = b  # Blue channel value, between 0 and 1
        self.a = a  # Alpha channel value, between 0 and 1


class ExportSetting:
    """Format and size to export an asset at"""

    def __init__(self, suffix, format, constraint):
        """Create a new instance of ExportSetting"""
        self.suffix = suffix  # File suffix to append all file names
        self.format = format  # Image type, string enum that supports values 'JPG', 'PNG', and 'SVG'
        self.constraint = (
            constraint  # Constraint that determines sizing of exported asset
        )


class Constraint:
    """Sizing constraint for exports"""

    def __init__(self, type, value):
        """Create a new instance of Constraint"""
        self.type = type  # Type of constraint to apply; string enum with potential values 'SCALE', 'WIDTH', 'HEIGHT'
        self.value = value  # See type property for effect of this field


class Rect:
    """A rectangle that expresses a bounding box in absolute coordinates"""

    def __init__(self, x, y, width, height):
        """Create a new instance of Rect"""
        self.x = x  # X coordinate of top left corner of the rectangle
        self.y = y  # Y coordinate of top left corner of the rectangle
        self.width = width  # Width of the rectangle
        self.height = height  # Height of the rectangle


class BlendMode(Enum):
    """
    Enum describing how layer blens with layers below

    This type is a string enum with the following possible values:
    """

    # Normal Blends
    PASS_THROUGH = "PASS_THROUGH"
    NORMAL = "NORMAL"
    # Darken
    DARKEN = "DARKEN"
    MULTIPLY = "MULTIPLY"
    LINEAR_BURN = "LINEAR_BURN"
    COLOR_BURN = "COLOR_BURN"
    # Lighten
    LIGHTEN = "LIGHTEN"
    SCREEN = "SCREEN"
    LINEAR_DODGE = "LINEAR_DODGE"
    COLOR_DODGE = "COLOR_DODGE"
    # Contrast
    OVERLAY = "OVERLAY"
    SOFT_LIGHT = "SOFT_LIGHT"
    HARD_LIGHT = "HARD_LIGHT"
    # Inversion
    DIFFERENCE = "DIFFERENCE"
    EXCLUSION = "EXCLUSION"
    # Component
    HUE = "HUE"
    SATURATION = "SATURATION"
    COLOR = "COLOR"
    LUMINOSITY = "LUMINOSITY"


class LayoutConstraint:
    """Layout constraint relative to containing Frame"""

    def __init__(self, vertical, horizontal):
        """Create a new instance of LayoutConstraint"""
        self.vertical = vertical  # Vertical constraint as an enum
        self.horizontal = horizontal  # Horizontal constraint as an enum


class LayoutGrid:
    """Guides to align and place objects within a frame"""

    def __init__(
        self, pattern, sectionSize, visible, color, alignment, gutterSize, offset, count
    ):
        """Create a new instance of LayoutGrid"""
        self.pattern = pattern  # Orientatoin of the grid as a string enum
        self.sectionSize = sectionSize  # Width of column grid or height of row grid or square grid spacing
        self.visible = visible  # Is the grid currently visible?
        self.color = color  # Color of the grid
        # The following properties are only meaningful for directional grids (COLUMNS or ROWS)
        self.alignment = alignment  # Positioning of grid as a string enum
        self.gutterSize = gutterSize  # Spacing in between columns and rows
        self.offset = offset  # Spacing before the first column or row
        self.count = count  # Number of columns or rows


class Effect:
    """A visual effect such as a shadow or blur"""

    def __init__(
        self,
        type,
        visible,
        radius,
        color=None,
        blendMode=None,
        offset=None,
        showShadowBehindNode=None,
        spread=0,
    ):
        """Create a new instance of Effect"""
        self.type = type  # Type of effect as a string enum
        self.visible = visible  # is the effect active?
        self.radius = radius  # Radius of the blur effect (applies to shadows as well)

        # The following properties are for shadows only:
        self.color = color  # The color of the shadow
        self.blendMode = blendMode  # Blend mode of the shadow
        self.offset = (
            offset  # How far the shadow is projected in the x and y directions
        )
        self.spread = spread
        self.showShadowBehindNode = showShadowBehindNode


class Paint:
    """
    A solid color, gradient, or image texture

    Can be applied as fills or strokes
    """

    def __init__(
        self,
        type,
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
        _parent=None,
    ):
        """Create a new instance of Paint"""
        self.type = type  # Type of paint as a string enum
        self.visible = visible  # Is the paint enabled?
        self.opacity = opacity  # Overall opacity of paint (colors within the paint can also have opacity values)
        self.blendMode = blendMode

        # For solid paints:
        self.color = color  # Solid color of the paint

        # For gradient paints:
        self.gradientHandlePositions = (
            gradientHandlePositions  # Three vectors, each are pos in normalized space
        )
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
        self._parent = _parent

    def get_file_image_url(self):
        """Get url of image"""
        if self.imageRef is None:
            return

        file_images = self.root_parent.get_file_images(
            file_key=self.get_file_key(), ids=[self._parent.id], format="svg"
        )
        # get file images is a figmapy session method. the root parent is the figmapy session
        # seems there might be a better way for this, instead of relying on root parent

        return file_images.images[self._parent.id]

    @property
    def root_parent(self):
        """Get root parent from instance"""
        root_parent = self._parent  # get FigmaPy instance
        while hasattr(root_parent, "_parent"):
            root_parent = root_parent._parent
        return root_parent

    def get_file_key(self):
        """
        Get file key

        TODO: property get setter
        """
        return get_file_key(self)


class Vector2d:
    """A 2d vector"""

    def __init__(self, x, y):
        """Create a new instance of Vector2d"""
        self.x = x  # X coordinate of the vector
        self.y = y  # Y coordinate of the vector


class Transform:
    """A 2x3 2D affine transformation matrix"""

    def __init__(self, matrix):
        """Create a new instance of Transform"""
        self.matrix = matrix  # Transformation matrix


class Path:
    """
    Not documented in the usual figma doc page: https://www.figma.com/developers/api

    instead see https://www.figma.com/plugin-docs/api/VectorPath/#docsNav
    A vector path
    """

    def __init__(self, path, windingRule):
        """Create a new instance of Path"""
        self.path = path  # A sequence of path commands in SVG notation
        self.windingRule = (
            windingRule  # Winding rule for the path, either 'EVENODD' or 'NONZERO'
        )


class FrameOffset:
    """A relative offset within a frame"""

    def __init__(self, node_id, node_offset):
        """Create a new instance of FrameOffset"""
        self.node_id = node_id  # Unique id specifying the frame
        self.node_offset = Vector2d(**node_offset)  # 2d vector offset within the frame


class ColorStop:
    """A position color pair representing a gradient stop"""

    def __init__(self, position, color):
        """Create a new instance of ColorStop"""
        self.position = (
            position  # Value between 0 and 1 representing position along gradient axis
        )
        self.color = color  # Color attached to corresponding position


class TypeStyle:
    """Metadata for character formatting"""

    def __init__(
        self,
        font_family,
        font_post_script_name,
        italic,
        font_weight,
        font_size,
        text_align_horizontal,
        text_align_vertical,
        letter_spacing,
        fills,
        line_height_px,
        line_height_percent,
    ):
        """Create a new instance of TypeStyle"""
        self.font_family = font_family  # Font family of text (standard name)
        self.font_post_script_name = font_post_script_name  # PostScript font name
        self.italic = italic  # Is text italicized?
        self.font_weight = font_weight  # Numeric font weight
        self.font_size = font_size  # Font size in px
        self.text_align_horizontal = (
            text_align_horizontal  # Horizontal text alignment as string enum
        )
        self.text_align_vertical = (
            text_align_vertical  # Vertical text alignment as string enum
        )
        self.letter_spacing = letter_spacing  # Space between characters in px
        self.fills = fills  # Paints applied to characters
        self.line_height_px = line_height_px  # Line height in px
        self.line_height_percent = (
            line_height_percent  # Line height as a percentage of normal line height
        )

        deserialize_properties(self)


class ComponentDescription:
    """
    A description of a master component.

    Helps you identify which component instances are attached to
    """

    def __init__(self, name, description):
        """Create a new instance of ComponentDescription"""
        self.name = name  # The name of the component
        self.description = (
            description  # The description of the component as entered in the editor
        )


def deserialize_properties(self):
    """Deserialize properties to their matching type"""
    # fmt:off
    if (hasattr(self, "color") and isinstance(self.color, dict) and self.color is not None): # noqa
        self.color = Color(**self.color)

    if (hasattr(self, "constraint") and isinstance(self.constraint, dict) and self.constraint is not None): # noqa
        self.constraint = Constraint(**self.constraint)

    if (hasattr(self, "absoluteBoundingBox") and isinstance(self.absoluteBoundingBox, dict) and self.absoluteBoundingBox is not None): # noqa
        self.absoluteBoundingBox = Rect(**self.absoluteBoundingBox)

    if (hasattr(self, "blendMode") and isinstance(self.blendMode, str) and self.blendMode is not None): # noqa
        self.blendMode = BlendMode[self.blendMode]

    if (hasattr(self, "constraints") and isinstance(self.constraints, list) and self.constraints is not None): # noqa
        self.constraints = [Constraint(**constraint) for constraint in self.constraints]

    if (hasattr(self, "layoutGrids") and isinstance(self.layoutGrids, list) and self.layoutGrids is not None): # noqa
        self.layoutGrids = [LayoutGrid(**grid) for grid in self.layoutGrids]

    if (hasattr(self, "children") and isinstance(self.children, list) and self.children is not None): # noqa
        self.children = [self.deserialize(child) for child in self.children]
        if self:
            for child in self.children:
                child._parent = self

    if (hasattr(self, "fillGeometry") and isinstance(self.fillGeometry, list) and self.fillGeometry is not None): # noqa
        self.fillGeometry = [Path(**path) for path in self.fillGeometry]

    if (hasattr(self, "strokeGeometry") and isinstance(self.strokeGeometry, list) and self.strokeGeometry is not None): # noqa
        self.strokeGeometry = [Path(**path) for path in self.strokeGeometry]

    if (hasattr(self, "exportSettings") and isinstance(self.exportSettings, list) and self.exportSettings is not None): # noqa
        self.exportSettings = [
            ExportSetting(**setting) for setting in self.exportSettings
        ]

    if (hasattr(self, "fills") and isinstance(self.fills, list) and self.fills is not None): # noqa
        self.fills = [Paint(**paint, _parent=self) for paint in self.fills]

    if (hasattr(self, "strokes") and isinstance(self.strokes, list) and self.strokes is not None): # noqa
        self.strokes = [Paint(**paint, _parent=self) for paint in self.strokes]

    if (hasattr(self, "effects") and isinstance(self.effects, list) and self.effects is not None): # noqa
        self.effects = [Effect(**effect) for effect in self.effects]

    # fmt:on

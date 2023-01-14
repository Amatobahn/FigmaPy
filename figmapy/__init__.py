# -*- coding: utf-8 -*-

"""
Figma API Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Figma API.

:copyright: (c) 2018 Greg Amato
:license: Apache V2.0, see LICENSE for more details.

"""

__title__ = 'FigmaPy'
__author__ = 'Greg Amato'
__license__ = 'Apache V2.0'
__copyright__ = 'Copyright 2018 Greg Amato'
__version__ = '2018.1.0'

from .session.figma_aiohttp import AioHttpFigmaPy
from .session.figma_requests import FigmaPy
from . import datatypes
dt = datatypes  # alias for convenience

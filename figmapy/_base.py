"""Base class for every generated model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FigmaModel(BaseModel):
    """Base for all generated Figma models.

    ``extra="allow"`` is the reason this wrapper does not go stale: when Figma adds a
    field to a response, it lands on the model as a plain attribute straight away. No
    release of figmapy is needed to read it, it just will not be typed until the spec
    is re-synced.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    def __repr__(self) -> str:
        name = getattr(self, "name", None)
        if name is not None:
            return f"{type(self).__name__}({name!r})"
        return f"{type(self).__name__}()"

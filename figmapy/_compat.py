"""Names kept from figmapy 2018.1.0 so existing scripts keep running.

Mixed into both clients ahead of the generated endpoints, so it can adapt arguments
before handing off. Every method here returns whatever the generated method returns,
which for :class:`~figmapy.AsyncFigma` is an awaitable -- so one shim covers both
clients without duplicating anything.
"""

from __future__ import annotations

from typing import Any


class LegacyAliases:
    def get_file(self, file_key: str | None = None, *, key: str | None = None, **kwargs: Any) -> Any:
        """Get file JSON. ``key=`` is the pre-1.0 name for ``file_key``."""
        return super().get_file(file_key or key, **kwargs)  # type: ignore[misc]

    def get_file_images(self, file_key: str, ids: Any, **kwargs: Any) -> Any:
        """Deprecated alias for :meth:`get_images`, which is the spec's name."""
        return self.get_images(file_key, ids=ids, **kwargs)  # type: ignore[attr-defined]

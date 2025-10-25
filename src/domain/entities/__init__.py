"""Domain entities package.

Entities are domain objects with identity and lifecycle.
They encapsulate business logic and validate their own invariants.
"""

from .task import Task

__all__ = ["Task"]

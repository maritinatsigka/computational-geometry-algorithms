from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float

    def as_tuple(self) -> tuple[float, float]:
        # Convert to (x, y)
        return (self.x, self.y)
from __future__ import annotations
import random
from .primitives2d import Point2D
from .primitives3d import Point3D

def random_points_2d(n: int, seed: int = 0, lo: float = 0.0, hi: float = 1000.0) -> list[Point2D]:
    # Generate n random 2D points
    rng = random.Random(seed)
    points: list[Point2D] = []
    for _ in range(n):
        x = rng.uniform(lo, hi)
        y = rng.uniform(lo, hi)
        p = Point2D(x, y)
        points.append(p)

    return points


def random_points_3d(n: int, seed: int = 0, lo: float = 0.0, hi: float = 1000.0) -> list[Point3D]:
    # Generate n random 3D points
    rng = random.Random(seed)
    points: list[Point3D] = []
    for _ in range(n):
        x = rng.uniform(lo, hi)
        y = rng.uniform(lo, hi)
        z = rng.uniform(lo, hi)
        p = Point3D(x, y, z)
        points.append(p)

    return points
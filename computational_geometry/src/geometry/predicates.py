from __future__ import annotations
from .primitives2d import Point2D
from .primitives3d import Point3D

def ccw(a: Point2D, b: Point2D, c: Point2D) -> float:
    # Orientation test in 2D (left/right/collinear)
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

def dist2(a: Point2D, b: Point2D) -> float:
    # Squared Euclidean distance
    return (a.x - b.x)**2 + (a.y - b.y)**2

def orient3d(a: Point3D, b: Point3D, c: Point3D, d: Point3D) -> float:
    # Orientation test in 3D (positive/negative/zero)
    abx, aby, abz = b.x - a.x, b.y - a.y, b.z - a.z
    acx, acy, acz = c.x - a.x, c.y - a.y, c.z - a.z
    adx, ady, adz = d.x - a.x, d.y - a.y, d.z - a.z

    return abx*(acy*adz - acz*ady) - acx*(aby*adz - abz*ady) + adx*(aby*acz - abz*acy)
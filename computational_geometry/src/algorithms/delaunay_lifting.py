from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from src.geometry.primitives2d import Point2D
from src.geometry.primitives3d import Point3D
from src.algorithms.hull3d_incremental import convex_hull_3d_incremental

EPS = 1e-9
Tri = tuple[int, int, int]
Edge = tuple[int, int]

# Paraboloid lifting: (x,y)->(x,y,x^2+y^2)
def lift(p: Point2D) -> Point3D:
    return Point3D(p.x, p.y, p.x * p.x + p.y * p.y)


def normal_z(a: Point3D, b: Point3D, c: Point3D) -> float:
    abx, aby = b.x - a.x, b.y - a.y
    acx, acy = c.x - a.x, c.y - a.y
    return abx * acy - aby * acx


def delaunay_triangulation_lifting(points: list[Point2D]) -> tuple[list[Point2D], list[Tri]]:
    # Remove duplicates
    uniq_xy = sorted(set((p.x, p.y) for p in points))
    pts2_in = [Point2D(x, y) for x, y in uniq_xy]
    if len(pts2_in) < 3:
        return pts2_in, []

    # Lift to 3D and compute convex hull
    lifted = [lift(p) for p in pts2_in]
    pts3, faces = convex_hull_3d_incremental(lifted)
    pts2 = [Point2D(p.x, p.y) for p in pts3] 

    # Keep only lower hull faces
    lower_faces: list[Tri] = []
    for (i, j, k) in faces:
        nz = normal_z(pts3[i], pts3[j], pts3[k])
        if nz < -EPS:
            lower_faces.append((i, j, k))

    return pts2, lower_faces


# Unique undirected edges from triangles
def triangulation_edges(tris: Iterable[Tri]) -> list[Edge]:
    edges: set[Edge] = set()
    for a, b, c in tris:
        e1 = (a, b) if a < b else (b, a)
        e2 = (b, c) if b < c else (c, b)
        e3 = (c, a) if c < a else (a, c)
        edges.add(e1)
        edges.add(e2)
        edges.add(e3)
    return sorted(edges)


def delaunay_lifting_steps(points: list[Point2D], start: int = 3) -> list[tuple[list[Point2D], list[Tri]]]:
    # Recompute triangulation after each insertion
    uniq_xy = sorted(set((p.x, p.y) for p in points))
    pts = [Point2D(x, y) for x, y in uniq_xy]

    steps: list[tuple[list[Point2D], list[Tri]]] = []
    for k in range(max(start, 3), len(pts) + 1):
        pts2, tris = delaunay_triangulation_lifting(pts[:k])
        steps.append((pts2, tris))
    return steps

from __future__ import annotations
from src.geometry.primitives2d import Point2D
from src.geometry.predicates import ccw


def extreme_points(points: list[Point2D]) -> tuple[Point2D, Point2D]:
    # Leftmost and rightmost points
    pts_xy = sorted(set((p.x, p.y) for p in points))
    pts = [Point2D(x, y) for x, y in pts_xy]
    if len(pts) == 0:
        raise ValueError("No points given")

    A = min(pts, key=lambda p: (p.x, p.y)) 
    B = max(pts, key=lambda p: (p.x, p.y))  
    return A, B


def split_by_line(A: Point2D, B: Point2D, points: list[Point2D]) -> tuple[list[Point2D], list[Point2D], list[Point2D]]:
    # Split points by the directed line A->B
    above: list[Point2D] = []
    below: list[Point2D] = []
    collinear: list[Point2D] = []

    for p in points:
        if p == A or p == B:
            continue
        s = ccw(A, B, p)
        if s > 0:
            above.append(p)
        elif s < 0:
            below.append(p)
        else:
            collinear.append(p)

    return above, below, collinear


def farthest_point_from_line(A: Point2D, B: Point2D, pts: list[Point2D]) -> Point2D:
    # Max distance from line AB
    return max(pts, key=lambda p: abs(ccw(A, B, p)))


def points_left_of_line(A: Point2D, B: Point2D, pts: list[Point2D]) -> list[Point2D]:
    # Points strictly to the left of directed line A->B
    return [p for p in pts if ccw(A, B, p) > 0]


def quickhull_side(A: Point2D, B: Point2D, S: list[Point2D]) -> list[Point2D]:
    # Recursive QuickHull on one side of line AB
    if len(S) == 0:
        return []

    C = farthest_point_from_line(A, B, S)
    S1 = points_left_of_line(A, C, S)
    S2 = points_left_of_line(C, B, S)

    return quickhull_side(A, C, S1) + [C] + quickhull_side(C, B, S2)


def convex_hull_quickhull(points: list[Point2D]) -> list[Point2D]:
    # QuickHull convex hull
    pts_xy = sorted(set((p.x, p.y) for p in points))
    pts = [Point2D(x, y) for x, y in pts_xy]
    if len(pts) <= 1:
        return pts

    A, B = extreme_points(pts)
    above, below, _ = split_by_line(A, B, pts)

    upper = quickhull_side(A, B, above)
    lower = quickhull_side(B, A, below)

    return [A] + upper + [B] + lower
from __future__ import annotations
from src.geometry.primitives2d import Point2D
from src.geometry.predicates import ccw, dist2


def convex_hull_jarvis(points: list[Point2D]) -> list[Point2D]:
    # Remove duplicates
    pts_xy = sorted(set((p.x, p.y) for p in points))
    pts = [Point2D(x, y) for x, y in pts_xy]
    n = len(pts)
    if n <= 1:
        return pts

    # Start from the leftmost point
    start = min(pts, key=lambda p: (p.x, p.y))
    hull: list[Point2D] = []

    p = start
    while True:
        hull.append(p)
        # Pick an initial candidate for the next hull point
        q = pts[0]
        if q == p:
            q = pts[1]

        for r in pts:
            if r == p:
                continue
            turn = ccw(p, q, r)
            if turn > 0:
                q = r
            elif turn == 0 and dist2(p, r) > dist2(p, q):
                q = r   # keep the farthest collinear point

        p = q
        if p == start:
            break

    return hull

from __future__ import annotations
from src.geometry.primitives2d import Point2D
from src.geometry.predicates import ccw

def convex_hull_incremental(points: list[Point2D]) -> list[Point2D]:
        # Monotone chain convex hull
        pts_xy = sorted(set((p.x, p.y) for p in points))
        pts = [Point2D(x, y) for x, y in pts_xy]

        n = len(pts)
        if n <= 1:
            return pts

        def is_right_turn(a: Point2D, b: Point2D, c: Point2D) -> bool:
            return ccw(a, b, c) < 0

        # Build upper hull
        upper: list[Point2D] = [pts[0], pts[1]]
        for i in range (2, n):
            upper.append(pts[i])
            while len(upper) >= 3 and (not is_right_turn(upper[-3], upper[-2], upper[-1])):
                upper.pop(-2)

        # Lower hull  
        lower: list[Point2D] = [pts[n-1], pts[n-2]]
        for i in range (n-3, -1, -1):
            lower.append(pts[i])
            while len(lower) >= 3 and (not is_right_turn(lower[-3], lower[-2], lower[-1])):
                lower.pop(-2)

        # Remove endpoints before joining
        if len(lower) >= 2: 
            lower = lower[1:-1]
        
        return upper + lower


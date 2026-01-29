from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
import random
import math
from src.geometry.primitives2d import Point2D

EPS = 1e-9

@dataclass(frozen=True)
class Halfplane:
    # a*x + b*y <= c
    a: float
    b: float
    c: float

    def ok(self, p: Point2D) -> bool:
        return self.a * p.x + self.b * p.y <= self.c + EPS


def to_leq(a: float, b: float, c: float, relation: str) -> Halfplane:
    # Convert ">=" to "<=" form
    if relation == "<=":
        return Halfplane(a, b, c)
    if relation == ">=":
        return Halfplane(-a, -b, -c)
    raise ValueError("relation must be '<=' or '>='")


def intersect_lines(h1: Halfplane, h2: Halfplane) -> Optional[Point2D]:
    # Intersection of boundary lines
    a1, b1, c1 = h1.a, h1.b, h1.c
    a2, b2, c2 = h2.a, h2.b, h2.c
    det = a1 * b2 - a2 * b1
    if abs(det) < EPS:
        return None
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return Point2D(x, y)


def feasible(p: Point2D, H: List[Halfplane]) -> bool:
    return all(h.ok(p) for h in H)


def obj(p: Point2D, c1: float, c2: float) -> float:
    return c1 * p.x + c2 * p.y

def _point_on_line(h: Halfplane) -> Point2D:
    # Find any point on the line a*x + b*y = c
    a, b, c = h.a, h.b, h.c
    if abs(a) < EPS and abs(b) < EPS:
        raise ValueError("Invalid constraint: a=b=0")
    if abs(b) >= abs(a):
        # x = 0
        return Point2D(0.0, c / b)
    else:
        # y = 0
        return Point2D(c / a, 0.0)


def _solve_on_boundary(boundary: Halfplane, prev: List[Halfplane], c1: float, c2: float) -> Point2D:
    # maximize on the line a*x + b*y = c
    p0 = _point_on_line(boundary)
    dx, dy = boundary.b, -boundary.a

    tmin = -math.inf
    tmax = math.inf

    for g in prev:
        alpha = g.a * dx + g.b * dy
        beta = g.c - (g.a * p0.x + g.b * p0.y) 

        if abs(alpha) < EPS:
            if beta < -EPS:
                raise ValueError("Infeasible on boundary.")
            continue

        t_bound = beta / alpha
        if alpha > 0:
            tmax = min(tmax, t_bound)
        else:
            tmin = max(tmin, t_bound)

        if tmin > tmax + EPS:
            raise ValueError("Infeasible on boundary.")

    slope = c1 * dx + c2 * dy

    if math.isinf(tmin) or math.isinf(tmax):
        raise ValueError("Unbounded (missing box).")

    if slope > EPS:
        t = tmax
    elif slope < -EPS:
        t = tmin
    else:
        t = min(max(0.0, tmin), tmax)

    return Point2D(p0.x + t * dx, p0.y + t * dy)


def solve_lp_incremental_2d(constraints: List[Halfplane], c1: float, c2: float, seed: int = 0) -> Point2D:
    if not constraints:
        raise ValueError("No constraints given.")

    # Bounding box size
    scale = max(1.0, max(abs(h.c) for h in constraints))
    M = 1000.0 * scale 

    box = [
        Halfplane(1, 0, M),  # x <= M
        Halfplane(-1, 0, M),  # x >= -M
        Halfplane(0, 1, M),   # y <= M
        Halfplane(0,-1, M),  # y >= -M
    ]

    rng = random.Random(seed)
    H = list(constraints)
    rng.shuffle(H)

    # Start from the best corner of the box for the objective
    x0 = M if c1 > 0 else -M
    y0 = M if c2 > 0 else -M
    p = Point2D(x0, y0)

    prev: List[Halfplane] = list(box)

    # Ensure start is feasible for box
    for h in H:
        if not h.ok(p):
            p = _solve_on_boundary(h, prev, c1, c2)
        prev.append(h)

    if not feasible(p, prev):
        raise ValueError("Internal error: infeasible result.")

    return p



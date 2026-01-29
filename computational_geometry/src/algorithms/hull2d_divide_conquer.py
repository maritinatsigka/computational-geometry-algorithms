from __future__ import annotations
from src.geometry.primitives2d import Point2D
from src.geometry.predicates import ccw
from src.algorithms.hull2d_incremental import convex_hull_incremental


def convex_hull_dc(points: list[Point2D]) -> list[Point2D]:
    # Remove duplicates and sort points by (x, y)
    pts_xy = sorted(set((p.x, p.y) for p in points))
    pts = [Point2D(x, y) for x, y in pts_xy]
    n = len(pts)
    if n <= 1:
        return pts

    return build_hull_dc(pts)


def build_hull_dc(pts_sorted: list[Point2D]) -> list[Point2D]:
    # Recursively build hull on sorted points
    n = len(pts_sorted)
    if n <= 8:
        # Small base case: use monotone chain (incremental) hull
        return convex_hull_incremental(pts_sorted)

    mid = n // 2
    left = build_hull_dc(pts_sorted[:mid])
    right = build_hull_dc(pts_sorted[mid:])

    return merge_hulls(left, right)  # Merge the two convex hulls


def merge_hulls(L: list[Point2D], R: list[Point2D]) -> list[Point2D]:
    if len(L) == 0:
        return R
    if len(R) == 0:
        return L
    if len(L) == 1 and len(R) == 1:
        if L[0] == R[0]:
            return [L[0]]
        else:
            return [L[0], R[0]]
    if len(L) == 1:
        return convex_hull_incremental(R + L)
    if len(R) == 1:
        return convex_hull_incremental(L + R)

    # Start from rightmost point of L and leftmost point of R
    i = idx_rightmost(L)
    j = idx_leftmost(R)

    # Find upper and lower tangents
    i_upper, j_upper = upper_tangent(L, R, i, j)
    i_lower, j_lower = lower_tangent(L, R, i, j)

    merged: list[Point2D] = []

    # Walk on L hull from upper tangent to lower tangent
    idx = i_upper
    merged.append(L[idx])
    while idx != i_lower:
        idx = next_idx(idx, len(L))
        merged.append(L[idx])

    # Walk on R hull from lower tangent to upper tangent
    idx = j_lower
    merged.append(R[idx])
    while idx != j_upper:
        idx = next_idx(idx, len(R))
        merged.append(R[idx])

    # Remove consecutive duplicates
    cleaned: list[Point2D] = []
    for p in merged:
        if not cleaned or p != cleaned[-1]:
            cleaned.append(p)

    return convex_hull_incremental(cleaned)


def upper_tangent(L: list[Point2D], R: list[Point2D], i: int, j: int) -> tuple[int, int]:
    # Move i and j until the upper tangent is found
    changed = True
    while changed:
        changed = False

        while ccw(R[j], L[i], L[next_idx(i, len(L))]) >= 0:
            i = next_idx(i, len(L))
            changed = True

        while ccw(L[i], R[j], R[prev_idx(j, len(R))]) <= 0:
            j = prev_idx(j, len(R))
            changed = True

    return i, j


def lower_tangent(L: list[Point2D], R: list[Point2D], i: int, j: int) -> tuple[int, int]:
    # Move i and j until the lower tangent is found
    changed = True
    while changed:
        changed = False

        while ccw(R[j], L[i], L[prev_idx(i, len(L))]) <= 0:
            i = prev_idx(i, len(L))
            changed = True

        while ccw(L[i], R[j], R[next_idx(j, len(R))]) >= 0:
            j = next_idx(j, len(R))
            changed = True

    return i, j


def next_idx(k: int, n: int) -> int:
    # Next index in a circular list
    return (k + 1) % n


def prev_idx(k: int, n: int) -> int:
    # Previous index in a circular list
    return (k - 1) % n


def idx_rightmost(H: list[Point2D]) -> int:
    # Index of rightmost point
    best = 0
    for idx, p in enumerate(H):
        if (p.x, p.y) > (H[best].x, H[best].y):
            best = idx
    return best


def idx_leftmost(H: list[Point2D]) -> int:
    # Index of leftmost point
    best = 0
    for idx, p in enumerate(H):
        if (p.x, p.y) < (H[best].x, H[best].y):
            best = idx
    return best
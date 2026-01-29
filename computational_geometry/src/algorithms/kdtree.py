from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.geometry.primitives2d import Point2D

@dataclass(slots=True)
class KDNode:
    p: Point2D
    axis: int          # 0: split x, 1: split y
    left: Optional["KDNode"] = None
    right: Optional["KDNode"] = None

def build_kdtree(points: list[Point2D], depth: int = 0) -> Optional[KDNode]:
    if not points:
        return None

    axis = depth % 2
    if axis == 0:
        key_fn = lambda q: (q.x, q.y)   # sort by x first
    else:
        key_fn = lambda q: (q.y, q.x)   # sort by y first

    pts = sorted(points, key=key_fn)
    mid = len(pts) // 2

    node = KDNode(pts[mid], axis)
    # Build subtrees from points left/right of the median
    node.left = build_kdtree(pts[:mid], depth + 1)
    node.right = build_kdtree(pts[mid + 1 :], depth + 1)
    return node

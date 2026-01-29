from __future__ import annotations
from dataclasses import dataclass
from src.geometry.primitives2d import Point2D
from src.algorithms.kdtree import KDNode

@dataclass(frozen=True, slots=True)
class Rect:
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def contains(self, p: Point2D) -> bool:  
        # Check if point is inside the rectangle (including borders)
        in_x = self.xmin <= p.x <= self.xmax
        in_y = self.ymin <= p.y <= self.ymax
        return in_x and in_y

def range_search(root: KDNode | None, r: Rect) -> list[Point2D]:
    # Report all points inside r
    result: list[Point2D] = []

    def rec(node: KDNode | None) -> None:
        if node is None:
            return
        p = node.p
        if r.contains(p):   # Add point if it is inside
            result.append(p)

        # Go to subtrees that can intersect the rectangle
        if node.axis == 0:  # split by x
            if r.xmin <= p.x: 
                rec(node.left)
            if r.xmax >= p.x: 
                rec(node.right)
        else:                 # y split
            if r.ymin <= p.y: 
                rec(node.left)
            if r.ymax >= p.y: 
                rec(node.right)

    rec(root)
    return result

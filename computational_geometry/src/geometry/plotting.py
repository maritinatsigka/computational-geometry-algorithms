from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from .primitives2d import Point2D
from src.algorithms.kdtree import KDNode
from src.algorithms.range_search import Rect

def plot_points_and_hull(points: list[Point2D], hull: list[Point2D], show: bool = True, title=None) -> None:
    # Scatter plot of input points
    xs = [p.x for p in points]
    ys = [p.y for p in points]

    plt.figure()
    plt.scatter(xs, ys)

    if len(hull) >= 2:
        hx = [p.x for p in hull] + [hull[0].x]
        hy = [p.y for p in hull] + [hull[0].y]
        plt.plot(hx, hy)

    if title:
        plt.title(title)

    if show:
        plt.show()
    else:
        plt.close()


def plot_kdtree(points, root, title: str = "KD-tree"):
    # Plot points + kd-tree split lines   
    if not points:
        return

    xs = [p.x for p in points]
    ys = [p.y for p in points]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    plt.figure()
    plt.scatter(xs, ys)

    def rec(node: KDNode | None, x0: float, x1: float, y0: float, y1: float) -> None:
        if node is None: 
            return
        
        p = node.p
        if node.axis == 0:
            # Vertical split
            plt.plot([p.x, p.x], [y0, y1])
            rec(node.left, x0, p.x, y0, y1)
            rec(node.right, p.x, x1, y0, y1)
        else:
            # Horizontal split
            plt.plot([x0, x1], [p.y, p.y])
            rec(node.left, x0, x1, y0, p.y)
            rec(node.right, x0, x1, p.y, y1)

    rec(root, xmin, xmax, ymin, ymax)
    plt.title(title)
    plt.axis("equal")
    plt.show()


def plot_range(points, r, reported, title: str = "Range query"):
    # Plot rectangle + reported points
    plt.figure()
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    plt.scatter(xs, ys, label="points")

    rx = [r.xmin, r.xmax, r.xmax, r.xmin, r.xmin]
    ry = [r.ymin, r.ymin, r.ymax, r.ymax, r.ymin]
    plt.plot(rx, ry, label="rectangle")

    if reported:
        rxs = [p.x for p in reported]
        rys = [p.y for p in reported]
        plt.scatter(rxs, rys, marker="x", s=120, label="reported")

    plt.title(title)
    plt.axis("equal")
    plt.legend()
    plt.show()
from __future__ import annotations
from src.geometry.primitives3d import Point3D
from src.geometry.predicates import orient3d

EPS = 1e-9
Face = tuple[int, int, int]


def initial_tetra(pts: list[Point3D]) -> tuple[int, int, int, int]:
    # Pick 4 non-coplanar points to form an initial tetrahedron
    n = len(pts)
    if n < 4:
        raise ValueError("Need at least 4 points")

    a = min(range(n), key=lambda i: (pts[i].x, pts[i].y, pts[i].z))
    b = max(range(n), key=lambda i: (pts[i].x, pts[i].y, pts[i].z))
    if a == b:
        raise ValueError("All points identical")

    p0, p1 = pts[a], pts[b]

    def line_score(i: int) -> float:
        # Squared distance from point i to line (p0,p1)
        ux, uy, uz = p1.x - p0.x, p1.y - p0.y, p1.z - p0.z
        vx, vy, vz = pts[i].x - p0.x, pts[i].y - p0.y, pts[i].z - p0.z
        cx, cy, cz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        return cx * cx + cy * cy + cz * cz

    c = max((i for i in range(n) if i not in (a, b)), key=line_score)
    if line_score(c) < EPS:
        raise ValueError("All points collinear")

    def plane_score(i: int) -> float:
        # Plane score
        return abs(orient3d(pts[a], pts[b], pts[c], pts[i]))

    d = max((i for i in range(n) if i not in (a, b, c)), key=plane_score)
    if plane_score(d) < EPS:
        raise ValueError("All points coplanar")

    return a, b, c, d


def convex_hull_3d_incremental(points: list[Point3D]) -> tuple[list[Point3D], list[Face]]:
    # Incremental 3D convex hull (returns vertices and triangular faces)
    uniq = sorted(set((p.x, p.y, p.z) for p in points))
    pts = [Point3D(x, y, z) for x, y, z in uniq]
    if len(pts) < 4:
        raise ValueError("Need at least 4 unique points")

    a, b, c, d = initial_tetra(pts)

    inside = Point3D(
        (pts[a].x + pts[b].x + pts[c].x + pts[d].x) / 4.0,
        (pts[a].y + pts[b].y + pts[c].y + pts[d].y) / 4.0,
        (pts[a].z + pts[b].z + pts[c].z + pts[d].z) / 4.0,
    )

    # Make face orientation consistent
    def fix(face: Face) -> Face:
        i, j, k = face
        return (i, k, j) if orient3d(pts[i], pts[j], pts[k], inside) > 0 else face

    def is_visible(face: Face, p: Point3D) -> bool:
        i, j, k = face
        return orient3d(pts[i], pts[j], pts[k], p) > EPS

    # Initial tetra faces
    faces: list[Face] = [(a, b, c), (a, d, b), (a, c, d), (b, d, c),]
    faces = [fix(f) for f in faces]

    seed = {a, b, c, d}

    for pid, p in enumerate(pts):
        if pid in seed:
            continue
        
        # Find faces visible from p
        visible_faces = [f for f in faces if is_visible(f, p)]
        if not visible_faces:
            continue

        # Count edges of visible faces to find the horizon
        edge_count: dict[tuple[int, int], int] = {}
        edge_dir: dict[tuple[int, int], tuple[int, int]] = {}

        def add_edge(u: int, v: int) -> None:
            key = (u, v) if u < v else (v, u)
            edge_count[key] = edge_count.get(key, 0) + 1
            edge_dir[key] = (u, v)

        for i, j, k in visible_faces:
            add_edge(i, j)
            add_edge(j, k)
            add_edge(k, i)

        # Remove visible faces
        vis_set = set(visible_faces)
        faces = [f for f in faces if f not in vis_set]

        # Horizon edges appear exactly once
        for key, cnt in edge_count.items():
            if cnt == 1:
                u, v = edge_dir[key]
                faces.append(fix((u, v, pid)))

    return pts, faces


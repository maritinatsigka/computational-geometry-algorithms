# Computational Geometry Algorithms

This project implements fundamental algorithms from computational geometry in Python, such as convex hulls, Delaunay triangulation, linear programming, and geometric searching.

---

## Implemented Algorithms and Structures

1. **Convex Hull in the Plane (2D)**

Multiple classical algorithms for computing the convex hull of a finite set of points in the plane are implemented:

   - Incremental Convex Hull Algorithm 
   - Jarvis March
   - Divide and Conquer Convex Hull Algorithm
   - QuickHull

All algorithms:

- Assume point sets in general position (no three points collinear)
- Rely on orientation (CCW) predicates
- Return the vertices of the convex hull in circular (counter-clockwise) order

Each algorithm is implemented independently.

Code:

- `src/algorithms/hull2d_incremental.py`
- `src/algorithms/hull2d_jarvis.py`
- `src/algorithms/hull2d_divide_conquer.py`
- `src/algorithms/hull2d_quickhull.py`

2. **Convex Hull in Three Dimensions (3D)**

An incremental algorithm for computing the convex hull of points in ℝ³ is implemented.

The implementation:

- Constructs an initial tetrahedron from non-coplanar points
- Adds points incrementally
- Detects faces visible from each new point using the `orient3d` predicate
- Removes visible faces and creates new triangular faces along the horizon

The algorithm returns:

- The set of hull vertices
- The set of triangular faces defining the convex hull

Code:

- `src/algorithms/hull3d_incremental.py`


3. **Linear Programming in Two Dimensions**

An incremental geometric algorithm for solving linear programming problems in the plane is implemented.

The algorithm:

   - Represents constraints as half-planes
   - Constructs the feasible region incrementally
   - Determines the optimal solution by examining extreme points of the feasible region

Code:

- `src/algorithms/lp2d_incremental.py`

4. **Delaunay Triangulation via Lifting**

The repository includes an implementation of Delaunay triangulation using the lifting to a paraboloid technique.

Specifically:

- Planar points are lifted to ℝ³ via a paraboloid mapping
- The lower convex hull of the lifted points is computed
- The Delaunay triangulation is obtained by projecting the lower hull back to ℝ²

The implementation relies on geometric predicates and convex hull construction, and supports visualization of intermediate steps for small point sets.

Code:

- `src/algorithms/delaunay_lifting.py`


5. **Geometric Searching with KD-Trees**

A KD-tree data structure for planar point sets is implemented, along with orthogonal range searching.

This component includes:

- Recursive KD-tree construction with alternating split dimensions
- Visualization of the induced spatial subdivision
- Orthogonal (axis-aligned) range queries

Code:

- `src/algorithms/kdtree.py`
- `src/algorithms/range_search.py`

---

## Geometry Foundations

All algorithms are built upon a shared geometric foundation that includes:

- Orientation (CCW) and orientation-in-3D predicates
- In-circle predicates where required
- Basic 2D and 3D geometric primitives
- Random point generation under general position assumptions
- Visualization utilities for geometric verification

Code:

- `src/geometry/predicates.py`
- `src/geometry/primitives2d.py`
- `src/geometry/primitives3d.py`
- `src/geometry/random_points.py`
- `src/geometry/plotting.py`

---











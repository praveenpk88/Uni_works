# Member 1 – A* Pathfinding Specialist: Complete Implementation Guide

**Course:** COSC2527/COSC3144 Games and AI Techniques, RMIT  
**Assignment:** Assignment 2 – Frog Game  
**Role:** Member 1 – A* Pathfinding Specialist  
**Marks scope:** Core A* movement + 4 enhancements (Varying Terrain, Varying Heuristics, Path Smoothing, Dynamic Obstacles)

---

## How to use this guide

This document captures **every single code change** made from the starter code to the final implementation. For each change you will find:
- The file name and line number (in the final code)
- The exact before and after code
- An explanation of why the change was made

Work through the files in this order: `Node.cs` → `AStarGrid.cs` → `Pathfinding.cs` → `Frog.cs`.

---

## Architecture decision (read this first)

The starter code had an odd split:
- `AStarGrid.cs` contained a **complete A* algorithm** (`FindPath`) and the `Node` class as an **inner class** inside `AStarGrid`
- `Pathfinding.cs` contained **empty TODO stubs** for a different A* implementation, referencing `AStarGrid.Node`
- `Node.cs` existed as a standalone file but was not connected to AStarGrid

These two architectures conflict. The decision was:

1. **Keep `Node.cs` as the standalone node class** and extend it (do not use the inner class)
2. **Rebuild `AStarGrid.cs` as a pure grid provider** — it creates the grid, stores nodes, and provides helper methods. It does NOT run A* itself.
3. **Fill in `Pathfinding.cs` as the A* engine** — it calls AStarGrid helpers but owns the search loop

This clean separation means AStarGrid handles "what is the map" and Pathfinding handles "how do I search it."

---

## 1. Node.cs

**File:** `Assets/Scripts/Pathfinding/Node.cs`

### Change 1.1 — Add TerrainType enum

**Lines 9–15 (current)**

**Before (starter):**
```csharp
public class Node : IHeapItem<Node>
{
    // Can the node be reached (ie, no obstacle)
    public bool walkable;
```

**After:**
```csharp
public class Node : IHeapItem<Node>
{
    public enum TerrainType
    {
        Normal,
        Mud,
        Water,
        Grass
    }

    public bool walkable;
```

**Why:** The spec requires Varying Terrain — different terrain types must influence pathfinding cost. The enum lives on `Node` because every node needs to know its own terrain type. Putting it here (not inside AStarGrid) means terrain is part of the node data model itself, accessible anywhere without importing AStarGrid.

---

### Change 1.2 — Add terrain fields to Node

**Lines 37–38 (current)**

**Before (starter):**
```csharp
    // Parent for this node (for reconstructing the path)
    public Node parent;

    // For heap management
    int heapIndex;
```

**After:**
```csharp
    public Node parent;

    // Terrain information used by weighted A*.
    public TerrainType terrainType;
    public float movementCost;

    int heapIndex;
```

**Why:** `terrainType` stores what kind of ground this node sits on. `movementCost` stores the pre-computed movement penalty for that terrain (e.g. mud = 3x, water = 5x). Storing the cost directly on the node avoids looking it up in a table during every A* iteration — the cost is baked at grid creation time.

---

### Change 1.3 — Extend the constructor signature

**Line 43 (current)**

**Before (starter):**
```csharp
    public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY)
    {
        walkable = _walkable;
        worldPosition = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
    }
```

**After:**
```csharp
    public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY, TerrainType _terrainType = TerrainType.Normal, float _movementCost = 1f)
    {
        walkable = _walkable;
        worldPosition = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
        terrainType = _terrainType;
        movementCost = _movementCost;
    }
```

**Why:** The two new parameters have defaults (`Normal` and `1f`) so all existing code that creates nodes without terrain data still compiles unchanged. AStarGrid passes real terrain data when it builds the grid.

---

### Change 1.4 — Extend Clone() to preserve terrain data

**Line 55 (current)**

**Before (starter):**
```csharp
    public Node Clone()
    {
        return new Node(walkable, worldPosition, gridX, gridY);
    }
```

**After:**
```csharp
    public Node Clone()
    {
        return new Node(walkable, worldPosition, gridX, gridY, terrainType, movementCost);
    }
```

**Why:** A cloned node must carry its terrain data. Without this, a clone would lose its movement cost (defaulting to 1), making terrain-aware clones silently wrong.

---

## 2. AStarGrid.cs

**File:** `Assets/Scripts/Pathfinding/AStarGrid.cs`

The starter's `AStarGrid.cs` contained a full embedded A* algorithm and a `Node` inner class. The entire file was rebuilt as a **pure grid provider**. Every change below is documented individually.

---

### Change 2.1 — Replace the class header and Inspector fields

**Lines 1–59 (current)**

**Before (starter):**
```csharp
public class AStarGrid : MonoBehaviour
{
    [Header("Gizmo/Debug Visualization")]
    public bool showGridGizmos = true;
    public bool showTerrainGizmos = true;
    public bool showPathGizmos = true;
    [HideInInspector]
    public List<Vector2> lastPath;

    public enum TerrainType { Normal, Mud, Water, Grass }
    [System.Serializable]
    public struct TerrainCost { ... }
    public TerrainCost[] terrainCosts = new TerrainCost[] { ... };

    public LayerMask mudMask;
    public LayerMask waterMask;
    public LayerMask grassMask;
    public Vector2 gridWorldSize = new Vector2(20f, 20f);
    public float nodeRadius = 0.5f;
    public LayerMask obstacleMask;
    public bool allowDiagonal = true;

    public enum HeuristicType { Euclidean, Manhattan, Octile }
    [Header("A* Heuristic")]
    public HeuristicType heuristicType = HeuristicType.Euclidean;
```

**After:**
```csharp
public class AStarGrid : MonoBehaviour
{
    public bool displayGridGizmos;
    public bool displayTerrainGizmos;
    public bool displayPathGizmos;

    [Header("Obstacle Layers")]
    public LayerMask unwalkableMask;
    public LayerMask dynamicObstacleMask;

    [Header("Terrain Layers")]
    public LayerMask mudMask;
    public LayerMask waterMask;
    public LayerMask grassMask;

    [Header("Terrain Costs")]
    public float normalCost = 1f;
    public float mudCost = 3f;
    public float waterCost = 5f;
    public float grassCost = 2f;

    [Header("Heuristics")]
    public PathHeuristic heuristicType = PathHeuristic.Euclidean;

    [Header("Path Smoothing")]
    public bool enablePathSmoothing = true;

    [Header("Terrain Colors")]
    public Color normalColor = Color.white;
    public Color mudColor = new Color(0.4f, 0.25f, 0.1f);
    public Color waterColor = Color.cyan;
    public Color grassColor = Color.green;

    public Vector2 gridWorldSize;
    public float gridSize;
    public float overlapCircleRadius = 0.4f;

    public bool includeDiagonalNeighbours = true;

    [HideInInspector]
    public Vector2[] lastWorldPath;

    public enum PathHeuristic
    {
        Euclidean,
        Manhattan,
        Octile,
        Chebyshev
    }
```

**Why (each sub-change):**

- `obstacleMask` → `unwalkableMask`: Clearer name — this mask is for permanent static obstacles only.
- `dynamicObstacleMask` added: A second mask for moving obstacles (snake). Static and dynamic are intentionally separated — dynamic objects must NOT be baked into the grid, only checked at search time.
- `TerrainCost[]` struct array → individual `float` fields: The struct array was unnecessary complexity. Individual floats are editable directly in the Inspector without expanding an array element.
- `nodeRadius` → `gridSize`: The starter used radius but the grid creation used it as both radius and half-diameter inconsistently. Renaming to `gridSize` (which is used as the actual node radius in the overlap check) removes the confusion. `nodeDiameter = gridSize * 2`.
- `allowDiagonal` → `includeDiagonalNeighbours`: More descriptive name matching the spec language.
- `HeuristicType` enum → `PathHeuristic` enum: Renamed and a fourth heuristic (`Chebyshev`) added — the spec requires a custom admissible heuristic beyond standard ones.
- `List<Vector2> lastPath` → `Vector2[] lastWorldPath`: Changed to array to match the `Node[]` path type used throughout. Also renamed to make clear these are world-space positions.
- `enablePathSmoothing` added: A toggle so you can switch smoothing off for the demo video (required to show heuristic differences, since smoothing hides them on open maps).
- Terrain color fields extracted: Colors moved out of the struct array into named fields for easier Inspector editing.

---

### Change 2.2 — Private field storage

**Lines 62–65 (current)**

**Before (starter):**
```csharp
    private Node[,] grid;
    private float nodeDiameter;
    private int gridSizeX, gridSizeY;
    private Vector2 worldBottomLeft;
```

**After:**
```csharp
    Node[,] grid;
    float nodeDiameter;
    int gridSizeX, gridSizeY;
    Vector2 worldBottomLeft;
    bool warnedGridSize;
    bool warnedWorldSize;
    bool warnedOverlap;
```

**Why:** `worldBottomLeft` was already in the starter but recomputed inside `NodeFromWorldPoint()`. Moving it to a stored field means it is computed once in `CreateGrid()` and reused on every lookup — important since `NodeFromWorldPoint` is called every A* search per node. Three warning booleans are added to prevent the console from spamming the same warning every frame when Inspector values are invalid.

---

### Change 2.3 — Guard conditions in CreateGrid()

**Lines 93–128 (current)**

**Before (starter):**
```csharp
    public void CreateGrid()
    {
        nodeDiameter = nodeRadius * 2f;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
        grid = new Node[gridSizeX, gridSizeY];
        worldBottomLeft = (Vector2)transform.position - Vector2.right * (gridWorldSize.x / 2f)
                          - Vector2.up * (gridWorldSize.y / 2f);
```

**After:**
```csharp
    public void CreateGrid()
    {
        if (gridSize <= 0f)
        {
            if (!warnedGridSize) { Debug.LogWarning("AStarGrid.gridSize must be > 0. Auto-correcting to 0.5."); warnedGridSize = true; }
            gridSize = 0.5f;
        }

        if (gridWorldSize.x <= 0f || gridWorldSize.y <= 0f)
        {
            if (!warnedWorldSize) { Debug.LogWarning("AStarGrid.gridWorldSize must be positive. Auto-correcting invalid axes to 1."); warnedWorldSize = true; }
            gridWorldSize = new Vector2(Mathf.Max(1f, gridWorldSize.x), Mathf.Max(1f, gridWorldSize.y));
        }

        if (overlapCircleRadius <= 0f)
        {
            overlapCircleRadius = gridSize * 0.8f;
            if (!warnedOverlap) { Debug.LogWarning("AStarGrid.overlapCircleRadius must be > 0. Auto-correcting based on gridSize."); warnedOverlap = true; }
        }

        nodeDiameter = gridSize * 2f;
        gridSizeX = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.x / nodeDiameter));
        gridSizeY = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.y / nodeDiameter));
```

**Why:** If `gridSize` is 0 (forgotten in Inspector), the starter would divide by zero and crash Unity. The guards auto-correct to safe values and warn once. `Mathf.Max(1, ...)` on grid dimensions prevents creating a 0×0 array which throws an out-of-bounds exception on first use.

---

### Change 2.4 — Terrain-aware node creation inside CreateGrid()

**Lines 130–149 (current)**

**Before (starter):**
```csharp
        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector2 worldPoint = worldBottomLeft + new Vector2(x * nodeDiameter + nodeRadius, y * nodeDiameter + nodeRadius);
                bool walkable = Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, obstacleMask) == null;
                TerrainType terrain = TerrainType.Normal;
                if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, mudMask)) terrain = TerrainType.Mud;
                else if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, waterMask)) terrain = TerrainType.Water;
                else if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, grassMask)) terrain = TerrainType.Grass;
                float moveCost = 1f;
                foreach (var tc in terrainCosts)
                {
                    if (tc.type == terrain) { moveCost = tc.cost; break; }
                }
                grid[x, y] = new Node(walkable, worldPoint, x, y, terrain, moveCost);
            }
        }
```

**After:**
```csharp
        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector2 worldPoint = worldBottomLeft + Vector2.right * (x * nodeDiameter + gridSize)
                                     + Vector2.up * (y * nodeDiameter + gridSize);

                bool blockedByStatic = Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, unwalkableMask) != null;
                bool walkable = !blockedByStatic;

                Node.TerrainType terrainType = GetTerrainTypeAtPoint(worldPoint);
                float movementCost = GetTerrainCost(terrainType);

                grid[x, y] = new Node(walkable, worldPoint, x, y, terrainType, movementCost);
            }
        }
```

**Why:**

- `obstacleMask` → `unwalkableMask`: Matches the renamed field.
- Dynamic obstacles are intentionally **not** checked here. If the snake were baked into the grid, the frog could never path through that cell even after the snake moves away. Dynamic obstacle avoidance is done at A* search time, not grid-bake time.
- Terrain detection extracted into `GetTerrainTypeAtPoint()` and cost lookup into `GetTerrainCost()` — cleaner and easier to extend.
- `nodeRadius * 0.9f` → `overlapCircleRadius`: The 0.9 multiplier was a magic number. Using a named Inspector field makes it adjustable.

---

### Change 2.5 — Corner-cutting prevention in GetNeighbours()

**Lines 179–187 (current)**

**Before (starter):**
```csharp
                if (checkX >= 0 && checkX < gridSizeX && checkY >= 0 && checkY < gridSizeY)
                {
                    neighbours.Add(grid[checkX, checkY]);
                }
```

**After:**
```csharp
                if (!InBounds(checkX, checkY))
                {
                    continue;
                }

                // Prevent diagonal moves that clip an obstacle corner.
                // Both orthogonal neighbours of a diagonal step must be walkable.
                if (Mathf.Abs(x) == 1 && Mathf.Abs(y) == 1)
                {
                    bool hWalkable = InBounds(node.gridX + x, node.gridY) && grid[node.gridX + x, node.gridY].walkable;
                    bool vWalkable = InBounds(node.gridX, node.gridY + y) && grid[node.gridX, node.gridY + y].walkable;
                    if (!hWalkable || !vWalkable)
                    {
                        continue;
                    }
                }

                neighbours.Add(grid[checkX, checkY]);
```

**Why:** Without this check, a diagonal move (e.g. North-East) is allowed even when the North cell or East cell is an obstacle. The frog's circular physics body would then physically clip into the obstacle corner and get wedged, unable to continue. The fix is: for any diagonal step, both adjacent orthogonal cells must also be walkable. This is known as "corner-cutting prevention" and is required for physics-accurate movement.

---

### Change 2.6 — GetHeuristicDistance() using grid coordinates

**Lines 196–219 (current)**

**Before (starter):**
```csharp
    private float GetHeuristic(Node a, Node b, HeuristicType type)
    {
        float dx = Mathf.Abs(a.worldPosition.x - b.worldPosition.x);
        float dy = Mathf.Abs(a.worldPosition.y - b.worldPosition.y);
        switch (type)
        {
            case HeuristicType.Manhattan:
                return dx + dy;
            case HeuristicType.Octile:
                float F = Mathf.Sqrt(2f) - 1f;
                return (dx < dy) ? F * dx + dy : F * dy + dx;
            case HeuristicType.Euclidean:
            default:
                return Mathf.Sqrt(dx * dx + dy * dy);
        }
    }
```

**After:**
```csharp
    public float GetHeuristicDistance(Node from, Node to)
    {
        float dx = Mathf.Abs(from.gridX - to.gridX);
        float dy = Mathf.Abs(from.gridY - to.gridY);

        switch (heuristicType)
        {
            case PathHeuristic.Manhattan:
                return dx + dy;
            case PathHeuristic.Octile:
                float diagonal = Mathf.Min(dx, dy);
                float straight = Mathf.Max(dx, dy) - diagonal;
                return diagonal * Mathf.Sqrt(2f) + straight;
            case PathHeuristic.Chebyshev:
                return Mathf.Max(dx, dy);
            default:
                return Mathf.Sqrt(dx * dx + dy * dy);
        }
    }
```

**Why (each sub-change):**

- **Grid coordinates instead of world positions:** `dx` and `dy` in grid cells are integers and require no floating-point subtraction. The result is the same because all nodes are equally spaced, but grid-coordinate differences are faster to compute and perfectly consistent.
- **`heuristicType` read from field, not passed as parameter:** The caller (`Pathfinding.cs`) does not need to specify the heuristic — AStarGrid owns that Inspector setting.
- **Chebyshev heuristic added (spec requirement — custom admissible heuristic):**  
  `max(dx, dy)` returns the minimum number of moves needed if the agent could move freely in any direction. This is always ≤ actual path cost (so it is admissible — it never overestimates). It underestimates more than Euclidean, so A* expands a wider frontier. This is visually different in gizmos and provably different from all three built-in heuristics — satisfying the spec's "admissible heuristic of your own invention" requirement.

---

### Change 2.7 — GetStepCost() for terrain-aware g-cost

**Lines 221–225 (current)**

**Before (starter):** g-cost was computed inline inside `FindPath()`:
```csharp
float tentativeG = currentNode.gCost + Vector2.Distance(currentNode.worldPosition, neighbour.worldPosition) * neighbour.movementCost;
```

**After (extracted to named method):**
```csharp
    public float GetStepCost(Node from, Node to)
    {
        float baseStepCost = Vector2.Distance(from.worldPosition, to.worldPosition);
        return baseStepCost * to.movementCost;
    }
```

**Why:** Extracting this to a method means `Pathfinding.cs` calls `grid.GetStepCost()` — Pathfinding does not need to know anything about terrain. The step cost multiplies the euclidean distance (1.0 for orthogonal, ~1.41 for diagonal) by the destination node's movement cost. The destination node's cost is used (not the average) because the penalty is for entering the terrain, not leaving it.

---

### Change 2.8 — IsPathSegmentClear() for path smoothing

**Lines 227–231 (current)**

**Before (starter):**
```csharp
    private bool HasLineOfSight(Vector2 a, Vector2 b)
    {
        return !Physics2D.Linecast(a, b, obstacleMask);
    }
```

**After:**
```csharp
    public bool IsPathSegmentClear(Vector2 from, Vector2 to)
    {
        LayerMask blockingMask = unwalkableMask | dynamicObstacleMask;
        return Physics2D.Linecast(from, to, blockingMask) == false;
    }
```

**Why:**

- Made `public` so `Pathfinding.cs` can call it (the starter had it private).
- Now checks **both** `unwalkableMask` and `dynamicObstacleMask`. If path smoothing only checked static obstacles, the smoothed segment could pass through a moving snake. Both masks are OR-combined so a single linecast covers everything.

---

### Change 2.9 — IsPointBlockedByDynamicObstacle() (new — dynamic obstacles)

**Lines 233–236 (current)**

**Before (starter):** Did not exist.

**After:**
```csharp
    public bool IsPointBlockedByDynamicObstacle(Vector2 worldPoint)
    {
        return Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, dynamicObstacleMask) != null;
    }
```

**Why:** This is the core runtime query for dynamic obstacle avoidance. Unlike static walkability (baked at grid creation), this is called live during the A* search to check if a candidate node is currently occupied by a dynamic obstacle. Using the same `overlapCircleRadius` as grid baking ensures consistency. `Pathfinding.cs` calls this per-neighbour during the A* loop.

---

### Change 2.10 — RecordPath() stores Node array

**Lines 238–251 (current)**

**Before (starter):**
```csharp
    // Path stored as List<Vector2> lastPath, set inline inside FindPath()
    lastPath = result;
```

**After:**
```csharp
    public void RecordPath(Node[] path)
    {
        if (path == null || path.Length == 0)
        {
            lastWorldPath = null;
            return;
        }

        lastWorldPath = new Vector2[path.Length];
        for (int i = 0; i < path.Length; i++)
        {
            lastWorldPath[i] = path[i].worldPosition;
        }
    }
```

**Why:** The path is now stored as `Node[]` in Pathfinding.cs. RecordPath extracts just the world positions for the gizmo drawer so it only stores what it needs (world positions, not the full node objects). Called by Pathfinding.cs after every search, including when no path is found (passes null to clear the gizmo).

---

### Change 2.11 — ResetSearchData() resets node costs before each search

**Lines 270–283 (current)**

**Before (starter):** Did not exist. The starter re-created nodes on every search.

**After:**
```csharp
    public void ResetSearchData()
    {
        if (grid == null) return;

        foreach (Node n in grid)
        {
            n.gCost = float.PositiveInfinity;
            n.hCost = 0f;
            n.parent = null;
        }
    }
```

**Why:** The `Heap<Node>` implementation uses `node.gCost` for ordering. If a second A* search runs without resetting, nodes from the previous search still have their old g-costs. The Heap would then make wrong ordering decisions, producing incorrect or infinitely-looping paths. Resetting g-costs to `∞` before each search ensures every node starts as "not yet reached." This is only needed because we reuse the same node objects across searches (instead of creating new ones every time, which would be expensive).

---

### Change 2.12 — ClosestWalkableNode() properly implemented

**Lines 285–345 (current)**

**Before (starter):**
```csharp
    public Node ClosestWalkableNode(Node node)
    {
        // Not implemented, return input for now
        return node;
    }
```

**After:**
```csharp
    public Node ClosestWalkableNode(Node node)
    {
        int maxRadius = Mathf.Max(gridSizeX, gridSizeY) / 2;
        for (int i = 1; i < maxRadius; i++)
        {
            Node n = FindWalkableInRadius(node.gridX, node.gridY, i);
            if (n != null) return n;
        }
        return null;
    }

    Node FindWalkableInRadius(int centreX, int centreY, int radius)
    {
        for (int i = -radius; i <= radius; i++)
        {
            // Check top, bottom, right, left edges of expanding square
            int verticalSearchX = i + centreX;
            int horizontalSearchY = i + centreY;

            if (InBounds(verticalSearchX, centreY + radius) && grid[verticalSearchX, centreY + radius].walkable)
                return grid[verticalSearchX, centreY + radius];
            if (InBounds(verticalSearchX, centreY - radius) && grid[verticalSearchX, centreY - radius].walkable)
                return grid[verticalSearchX, centreY - radius];
            if (InBounds(centreX + radius, horizontalSearchY) && grid[centreX + radius, horizontalSearchY].walkable)
                return grid[centreX + radius, horizontalSearchY];
            if (InBounds(centreX - radius, horizontalSearchY) && grid[centreX - radius, horizontalSearchY].walkable)
                return grid[centreX - radius, horizontalSearchY];
        }
        return null;
    }
```

**Why:** The starter stub returned the unwalkable node itself, which meant clicking on an obstacle would pass an unwalkable start/target into A*, causing immediate failure. The real implementation searches outward in expanding squares from the blocked node until it finds a walkable neighbour. This allows clicking near (but not exactly on) an obstacle to still find a valid path.

---

### Change 2.13 — MaxSize property with overflow protection

**Lines 74–91 (current)**

**Before (starter):**
```csharp
    public int MaxSize
    {
        get { return (grid != null) ? grid.GetLength(0) * grid.GetLength(1) : 0; }
    }
```

**After:**
```csharp
    public int MaxSize
    {
        get
        {
            long size = (long)gridSizeX * gridSizeY;
            if (size <= 0) return 1;
            if (size > int.MaxValue) return int.MaxValue;
            return (int)size;
        }
    }
```

**Why:** On a large map, `gridSizeX * gridSizeY` can overflow `int` silently (e.g. 200×200 = 40,000 which is fine, but 2000×2000 = 4,000,000 which overflows as negative). The `Heap` constructor receives `MaxSize` and would allocate a negative-length array, crashing. Casting to `long` before multiplying prevents the overflow.

---

### Change 2.14 — Terrain helper methods extracted

**Lines 383–431 (current)**

**Before (starter):** Terrain detection and cost lookup were inline in the grid loop.

**After (three separate private methods):**
```csharp
    private Node.TerrainType GetTerrainTypeAtPoint(Vector2 worldPoint)
    {
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, mudMask) != null)
            return Node.TerrainType.Mud;
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, waterMask) != null)
            return Node.TerrainType.Water;
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, grassMask) != null)
            return Node.TerrainType.Grass;
        return Node.TerrainType.Normal;
    }

    private float GetTerrainCost(Node.TerrainType terrainType)
    {
        switch (terrainType)
        {
            case Node.TerrainType.Mud:   return mudCost;
            case Node.TerrainType.Water: return waterCost;
            case Node.TerrainType.Grass: return grassCost;
            default:                     return normalCost;
        }
    }

    private Color GetTerrainColor(Node.TerrainType terrainType)
    {
        switch (terrainType)
        {
            case Node.TerrainType.Mud:   return mudColor;
            case Node.TerrainType.Water: return waterColor;
            case Node.TerrainType.Grass: return grassColor;
            default:                     return normalColor;
        }
    }
```

**Why:** Extracted for readability and to allow `GetTerrainCost()` to be called from `GetStepCost()` if needed in future. Priority order in `GetTerrainTypeAtPoint()` matters: mud is checked first, so a cell that overlaps both a mud and a water collider is classified as mud (a deliberate design choice — change the order to change priority).

---

## 3. Pathfinding.cs

**File:** `Assets/Scripts/Pathfinding/Pathfinding.cs`

The starter `Pathfinding.cs` had every key section stubbed with `TODO` comments and returning `false`/empty values. This section documents every stub that was filled in.

---

### Change 3.1 — Replace instance pattern with EnsureInitialized()

**Lines 9–50 (current)**

**Before (starter):**
```csharp
public class Pathfinding : MonoBehaviour
{
    public static AStarGrid grid;
    static Pathfinding instance;

    void Awake()
    {
        grid = GetComponent<AStarGrid>();
        instance = this;
    }

    public static AStarGrid.Node[] RequestPath(Vector2 from, Vector2 to)
    {
        return instance.FindPath(from, to);
    }

    AStarGrid.Node[] FindPath(Vector2 from, Vector2 to)
    {
        // ... (instance method)
    }
```

**After:**
```csharp
public class Pathfinding : MonoBehaviour
{
    public static AStarGrid grid;
    static bool warnedNoGrid;

    void Awake()
    {
        grid = GetComponent<AStarGrid>();
    }

    public static Node[] RequestPath(Vector2 from, Vector2 to)
    {
        EnsureInitialized();

        if (grid == null)
        {
            if (!warnedNoGrid)
            {
                Debug.LogWarning("Pathfinding.RequestPath called but no AStarGrid was found in scene.");
                warnedNoGrid = true;
            }
            return new Node[0];
        }

        return FindPath(from, to);
    }

    private static void EnsureInitialized()
    {
        if (grid == null)
            grid = UnityEngine.Object.FindFirstObjectByType<AStarGrid>();
        if (grid != null)
            warnedNoGrid = false;
    }
```

**Why:**

- `instance` static removed: All methods are now `static`, so there is no need to store a reference to the MonoBehaviour instance. Static methods can be called from `Frog.cs` without needing a field reference to the Pathfinding object.
- `AStarGrid.Node[]` → `Node[]`: Since `Node` is now a standalone class (not an inner class of AStarGrid), the prefix is dropped.
- `EnsureInitialized()`: If Awake() hasn't run yet (e.g. call order issues) or the grid is destroyed and recreated, this fallback finds AStarGrid in the scene. Prevents a null-reference crash if `RequestPath` is called before `Awake`.
- Null guard + warning: Returns an empty array (not null) so callers never get a null-reference on the result.

---

### Change 3.2 — Call ResetSearchData() before each search

**Line 64 (current)**

**Before (starter):** Not called (nodes kept stale costs from previous search).

**After:**
```csharp
    static Node[] FindPath(Vector2 from, Vector2 to)
    {
        Node[] waypoints = new Node[0];

        if (grid == null) return waypoints;

        grid.ResetSearchData();   // ← THIS LINE

        bool pathSuccess = false;
        // ... rest of A*
```

**Why:** See Change 2.11. Without this, the Heap uses stale g-costs from the previous search, producing wrong paths or infinite loops on the second click. Must be the first thing called inside `FindPath`.

---

### Change 3.3 — Initialize startNode before opening the heap

**Lines 112–117 (current)**

**Before (starter):** Not present (start node added to heap with no cost set).

**After:**
```csharp
        startNode.gCost = 0f;
        startNode.hCost = Heuristic(startNode, targetNode);
        startNode.parent = startNode;

        openSet.Add(startNode);
```

**Why:** `gCost = 0` is required — the start node costs nothing to reach. `hCost` is set immediately so the first `fCost` comparison in the Heap is correct. `parent = startNode` is a sentinel used by `RetracePath()` to detect the start (when `current == startNode`, the loop stops).

---

### Change 3.4 — Fill in the A* main loop (all TODOs)

**Lines 121–183 (current)**

**Before (starter):** The entire loop body was stubs:
```csharp
        while (!pathSuccess && openSet.Count > 0)
        {
            // TODO: Get the node with the lowest F cost...
            

            // TODO: If we have reached the target node... (replace false)
            if (false)
            {
                pathSuccess = true;
            }
            else
            {
                Node[] neighbours = new Node[0];  // TODO
                foreach (Node node in neighbours)
                {
                    if (false)  // TODO
                    {
                        // TODO: Calculate G Cost
                        if (false)  // TODO
                        {
                            // TODO: Set costs, parent, add to heap
                            if (false) { } else { }
                        }
                    }
                }
            }
        }
```

**After (fully implemented):**
```csharp
        while (!pathSuccess && openSet.Count > 0)
        {
            Node currentNode = openSet.RemoveFirst();
            closedSet.Add(currentNode);

            if (currentNode == targetNode)
            {
                pathSuccess = true;
            }
            else
            {
                List<Node> neighbours = grid.GetNeighbours(currentNode);
                foreach (Node node in neighbours)
                {
                    // Skip nodes that are statically blocked, already visited,
                    // or currently occupied by a moving obstacle.
                    if (node.walkable && !closedSet.Contains(node)
                        && !grid.IsPointBlockedByDynamicObstacle(node.worldPosition))
                    {
                        float newCostToNeighbour = currentNode.gCost + GCost(currentNode, node);

                        if (!openSet.Contains(node) || newCostToNeighbour < node.gCost)
                        {
                            node.gCost   = newCostToNeighbour;
                            node.hCost   = Heuristic(node, targetNode);
                            node.parent  = currentNode;

                            if (!openSet.Contains(node))
                                openSet.Add(node);
                            else
                                openSet.UpdateItem(node);
                        }
                    }
                }
            }
        }
```

**Why (each line explained):**

- `openSet.RemoveFirst()`: The Heap keeps the lowest f-cost node at position 0. `RemoveFirst()` is O(log n) vs O(n) for the starter's `List` scan — critical for large grids.
- `closedSet.Add(currentNode)`: Mark as fully explored so we never re-expand it.
- `currentNode == targetNode`: Path found — stop the loop.
- `node.walkable && !closedSet.Contains(node)`: Skip unwalkable (static obstacle) and already-visited nodes.
- `!grid.IsPointBlockedByDynamicObstacle(node.worldPosition)`: **This is the dynamic obstacle check.** At search time (not grid-bake time), we query live physics. If the snake is currently sitting on this node, A* will route around it without needing to rebuild the grid. This line is the entire implementation of the Dynamic Obstacles enhancement.
- `GCost(currentNode, node)`: Calls `grid.GetStepCost()` which multiplies distance by terrain cost — this is the Varying Terrain enhancement in action.
- `newCostToNeighbour < node.gCost`: If we find a cheaper route to a node we already know about, update it.
- `openSet.UpdateItem(node)`: Re-heapify after changing a node's cost — the Heap must be told the cost changed so it can restore the heap property.

---

### Change 3.5 — Fill in RetracePath()

**Lines 207–236 (current)**

**Before (starter):**
```csharp
    AStarGrid.Node[] RetracePath(AStarGrid.Node startNode, AStarGrid.Node endNode)
    {
        List<AStarGrid.Node> path = new List<AStarGrid.Node>();

        // TODO: Commence retracing from end node

        // TODO: Loop while current node isn't start node (replace false)
        while (false)
        {
            // TODO: Add current node to path
            // TODO: Set current node to parent
        }

        AStarGrid.Node[] waypoints = path.ToArray();
        Array.Reverse(waypoints);
        return waypoints;
    }
```

**After:**
```csharp
    static Node[] RetracePath(Node startNode, Node endNode)
    {
        List<Node> path = new List<Node>();

        Node currentNode = endNode;

        while (currentNode != startNode)
        {
            path.Add(currentNode);
            currentNode = currentNode.parent;
            if (currentNode == null) break;
        }

        Node[] waypoints = path.ToArray();
        Array.Reverse(waypoints);
        return waypoints;
    }
```

**Why:** Start from the target and walk the `parent` chain back to the start. Each node's parent was set during the A* loop. `Array.Reverse` flips the result from [target→start] to [start→target]. The `currentNode == null` safety check prevents an infinite loop if the parent chain is somehow broken.

---

### Change 3.6 — GCost() delegates to terrain-aware GetStepCost()

**Lines 238–241 (current)**

**Before (starter):**
```csharp
    private float GCost(Node nodeA, Node nodeB)
    {
        return 1.0f;  // constant — ignores distance and terrain
    }
```

**After:**
```csharp
    static float GCost(Node nodeA, Node nodeB)
    {
        return grid.GetStepCost(nodeA, nodeB);
    }
```

**Why:** The starter returned a constant `1.0f`, meaning all steps had identical cost regardless of distance or terrain. This breaks both diagonal movement (diagonal steps are ~1.41x longer than orthogonal) and the Varying Terrain enhancement. `GetStepCost()` returns `euclidean_distance × to.movementCost`, correctly weighting both.

---

### Change 3.7 — Heuristic() delegates to GetHeuristicDistance()

**Lines 244–247 (current)**

**Before (starter):**
```csharp
    private float Heuristic(Node nodeA, Node nodeB)
    {
        return 0;  // constant zero — A* degenerates to Dijkstra
    }
```

**After:**
```csharp
    static float Heuristic(Node nodeA, Node nodeB)
    {
        return grid.GetHeuristicDistance(nodeA, nodeB);
    }
```

**Why:** A heuristic of `0` makes A* equivalent to Dijkstra's algorithm — it explores every reachable node before finding the goal. This is correct but maximally slow. Delegating to `GetHeuristicDistance()` on AStarGrid enables all four heuristics (Euclidean, Manhattan, Octile, Chebyshev) and lets the Inspector toggle control which one is active.

---

### Change 3.8 — Call SmoothPath() and RecordPath() after finding path

**Lines 188–202 (current)**

**Before (starter):**
```csharp
        if (pathSuccess)
        {
            waypoints = RetracePath(startNode, targetNode);
        }
        return waypoints;
```

**After:**
```csharp
        if (pathSuccess)
        {
            waypoints = RetracePath(startNode, targetNode);
            if (grid.enablePathSmoothing)
            {
                waypoints = SmoothPath(waypoints);
            }
            grid.RecordPath(waypoints);
        }
        else
        {
            grid.RecordPath(null);
        }
        return waypoints;
```

**Why:**

- `SmoothPath()` is conditionally applied — only when `enablePathSmoothing` is true in the Inspector. This allows toggling smoothing on/off for the demo video.
- `RecordPath()` stores the final path (or null) so the gizmo drawer in `OnDrawGizmos()` can visualize it. Called in both the success and failure cases so the gizmo clears when there is no path.

---

### Change 3.9 — SmoothPath() moved from AStarGrid to Pathfinding

**Lines 249–283 (current)**

**Before (starter):** `SmoothPath()` was private inside `AStarGrid` and returned `List<Vector2>`.

**After (in Pathfinding.cs, operating on Node[]):**
```csharp
    static Node[] SmoothPath(Node[] originalPath)
    {
        if (originalPath == null || originalPath.Length < 3)
            return originalPath;

        List<Node> smoothedPath = new List<Node>();
        int currentIndex = 0;
        smoothedPath.Add(originalPath[currentIndex]);

        while (currentIndex < originalPath.Length - 1)
        {
            int furthestVisible = currentIndex + 1;

            for (int candidate = originalPath.Length - 1; candidate > currentIndex; candidate--)
            {
                if (grid.IsPathSegmentClear(
                        originalPath[currentIndex].worldPosition,
                        originalPath[candidate].worldPosition))
                {
                    furthestVisible = candidate;
                    break;
                }
            }

            if (furthestVisible == currentIndex) break;

            currentIndex = furthestVisible;
            smoothedPath.Add(originalPath[currentIndex]);
        }

        return smoothedPath.ToArray();
    }
```

**Why:** Path smoothing is a post-processing step on the A* result — it belongs in Pathfinding.cs alongside the search, not in AStarGrid (which should only know about the grid). The algorithm: starting from waypoint 0, scan backward from the last waypoint and take the furthest one with a clear line-of-sight. This skips all intermediate waypoints that are visible from the current position, producing a straight-line path through open space. `IsPathSegmentClear()` is called back on AStarGrid which owns the Physics2D layer masks.

---

## 4. Frog.cs

**File:** `Assets/Scripts/Frog.cs`

---

### Change 4.1 — Replace AStarGrid direct reference with Pathfinding.RequestPath()

**Lines 49–58 and 103 (current)**

**Before (starter):**
```csharp
    // Pathfinding
    public AStarGrid Pathfinder;
    private List<Vector2> _currentPath;
    private int _pathIndex = 0;
    public float waypointTolerance = 0.2f;
```

And in `Start()`:
```csharp
        if (Pathfinder == null)
            Pathfinder = Object.FindFirstObjectByType<AStarGrid>();
        _currentPath = null;
        _pathIndex = 0;
```

And in `Update()`:
```csharp
            if (Pathfinder != null)
            {
                _currentPath = Pathfinder.FindPath(transform.position, clickPos, ...);
                _pathIndex = 0;
            }
```

**After:**
```csharp
    [Header("A* Movement")]
    public float waypointTolerance = 0.5f;
    public float dynamicRepathInterval = 0.3f;
    public bool drawPathDebugLines = true;
    public bool allowDirectFallbackWhenNoPath = false;

    private Node[] _currentPath;
    private int _pathIndex;
    private Vector2? _pathGoal;
    private float _nextDynamicRepathTime;
```

And in `Update()`:
```csharp
            RequestPathTo((Vector2)_lastClickPos);
```

**Why:**

- `AStarGrid Pathfinder` field removed: Frog no longer needs a direct Inspector reference to AStarGrid. `Pathfinding.RequestPath()` is a static method — call it directly without a field.
- `List<Vector2> _currentPath` → `Node[] _currentPath`: The path is now an array of Nodes (not just world positions). This allows `getVelocityAlongPath()` to check if the current waypoint is the final one (needed for the Seek/Arrive split — see Change 4.3).
- `_pathGoal` added: Stores the destination of the current path so `TryRecalculatePathForDynamicObstacles()` knows where to re-path to.
- `_nextDynamicRepathTime` added: Timestamp throttle for repath checks so they happen at most every `dynamicRepathInterval` seconds.
- `waypointTolerance = 0.5f` (was `0.2f`): See Change 4.5.
- `allowDirectFallbackWhenNoPath = false`: See Change 4.5.

---

### Change 4.2 — Add RequestPathTo() method

**Lines 255–275 (current)**

**Before (starter):** Path request logic was inline in `Update()` with no fallback handling.

**After:**
```csharp
    private void RequestPathTo(Vector2 destination)
    {
        Node[] path = Pathfinding.RequestPath(transform.position, destination);

        if (path != null && path.Length > 0)
        {
            _pathGoal = destination;
            _currentPath = path;
            _pathIndex = 0;
            _lastClickPos = null;
        }
        else
        {
            _pathGoal = null;
            _currentPath = null;
            _pathIndex = 0;
            _lastClickPos = allowDirectFallbackWhenNoPath ? destination : null;
            Debug.LogWarning("A* could not find a path to destination. Using direct fallback movement.");
        }
    }
```

**Why:** Extracted to a method because it is called from two places — on click (in `Update`) and on dynamic repath (in `TryRecalculatePathForDynamicObstacles`). The fallback branch: if A* returns no path, the old code would automatically try to move directly to the destination. With `allowDirectFallbackWhenNoPath = false`, the frog stays still instead of ramming into walls — which was the observed behaviour when clicking unreachable targets.

---

### Change 4.3 — Seek for intermediate waypoints, Arrive only for final

**Lines 249–252 (current)**

**Before (starter):**
```csharp
    private Vector2 getVelocityAlongPath()
    {
        Vector2 desiredVel = Vector2.zero;
        if (_currentPath == null || _pathIndex >= _currentPath.Count)
            return desiredVel;

        Vector2 waypoint = _currentPath[_pathIndex];
        if (((Vector2)transform.position - waypoint).magnitude > Mathf.Max(Constants.TARGET_REACHED_TOLERANCE, waypointTolerance))
        {
            desiredVel = Steering.ArriveDirect(gameObject.transform.position, waypoint, _arriveRadius, MaxSpeed);
        }
        ...
    }
```

**After:**
```csharp
        // Use Seek (full speed) for intermediate waypoints so the frog moves naturally.
        // Only slow down with Arrive on the final waypoint.
        if (isFinalWaypoint)
            return Steering.ArriveDirect(gameObject.transform.position, currentWaypoint, _arriveRadius, MaxSpeed);
        else
            return Steering.SeekDirect(gameObject.transform.position, currentWaypoint, MaxSpeed);
```

**Why:** `ArriveDirect` decelerates as the agent approaches the target. With `_arriveRadius = 3` and grid nodes only 1 unit apart, the frog was always inside the arrive radius and moved at roughly 33% speed toward every intermediate node — causing slow, jittery movement. The fix: use `SeekDirect` (full speed, no deceleration) for every node except the final destination. The frog now moves at full speed through intermediate waypoints and only decelerates when approaching the actual click target.

---

### Change 4.4 — arrivedAtFinal stuck prevention for last waypoint

**Lines 220–225 (current)**

**Before (starter):** Path completion only checked `magnitude > waypointTolerance`. No special handling for the final waypoint.

**After:**
```csharp
        bool isFinalWaypoint = (_pathIndex == _currentPath.Length - 1);
        float distanceToWaypoint = ((Vector2)transform.position - currentWaypoint).magnitude;

        // For the final waypoint, also accept arrival if the frog is very close —
        // physics against a wall can prevent reaching the exact node centre.
        bool arrivedAtFinal = isFinalWaypoint && distanceToWaypoint <= _arriveRadius * 0.15f;

        if (distanceToWaypoint <= waypointTolerance || arrivedAtFinal)
        {
            _pathIndex++;
            ...
        }
```

**Why:** When the last waypoint is adjacent to a wall, the frog's physics body presses against the wall and cannot reach the node centre (which may be inside or just beside the obstacle collider). The path would never complete — the frog would press into the wall forever. The `arrivedAtFinal` check accepts the path as complete if the frog is within 15% of the arrive radius from the final node, regardless of `waypointTolerance`. This is only applied to the final waypoint — intermediate nodes still require the full `waypointTolerance` to advance.

---

### Change 4.5 — Default value fixes

**Lines 50–53 (current)**

**Before (starter):**
```csharp
    public float waypointTolerance = 0.2f;
    // (no dynamicRepathInterval)
    // (no allowDirectFallbackWhenNoPath)
```

**After:**
```csharp
    public float waypointTolerance = 0.5f;
    public float dynamicRepathInterval = 0.3f;
    public bool drawPathDebugLines = true;
    public bool allowDirectFallbackWhenNoPath = false;
```

**Why:**

- `waypointTolerance 0.2f → 0.5f`: With nodes 1 unit apart, a 0.2 tolerance means the frog must reach within 0.2 units of the exact node centre. Physics colliders and floating-point jitter meant the frog often stopped 0.25–0.35 units short and got stuck. 0.5 units is reliable for 1-unit-spaced grids.
- `dynamicRepathInterval = 0.3f`: Controls how often the frog re-checks its current path for dynamic obstacles. 0.3 seconds gives responsive rerouting without performance overhead from calling A* every frame.
- `allowDirectFallbackWhenNoPath = false`: When A* fails (unreachable target), the old default `true` caused the frog to steer directly through obstacles until hitting a physics wall. `false` makes the frog stop and wait — safer and more correct.

---

### Change 4.6 — TryRecalculatePathForDynamicObstacles()

**Lines 277–299 (current)**

**Before (starter):** Did not exist.

**After:**
```csharp
    private void TryRecalculatePathForDynamicObstacles()
    {
        if (_currentPath == null || _pathGoal == null || Time.time < _nextDynamicRepathTime)
            return;

        _nextDynamicRepathTime = Time.time + dynamicRepathInterval;

        if (Pathfinding.grid == null) return;

        for (int i = _pathIndex; i < _currentPath.Length; i++)
        {
            if (Pathfinding.grid.IsPointBlockedByDynamicObstacle(_currentPath[i].worldPosition))
            {
                RequestPathTo((Vector2)_pathGoal);
                break;
            }
        }
    }
```

**Why:** This is the second half of the Dynamic Obstacles enhancement. The A* search already avoids dynamic obstacles at search time. But after a path is found, the snake keeps moving — it may walk onto a node that is on the frog's currently-stored path. This method scans ahead on the stored path every `dynamicRepathInterval` seconds. If any upcoming node is now occupied by the snake, it triggers a fresh A* search from the current position to the original goal. The scan only checks nodes from `_pathIndex` onward (already-passed nodes are irrelevant).

---

### Change 4.7 — decideMovement() fallback guard

**Lines 166–181 (current)**

**Before (starter):**
```csharp
    private Vector2 decideMovement()
    {
        if (_currentPath != null && _pathIndex < _currentPath.Count)
            return getVelocityAlongPath();

        if (_lastClickPos != null)
            return getVelocityTowardsFlag();

        return Vector2.zero;
    }
```

**After:**
```csharp
    private Vector2 decideMovement()
    {
        if (_currentPath != null && _pathIndex < _currentPath.Length)
            return getVelocityAlongPath();

        if (allowDirectFallbackWhenNoPath && _lastClickPos != null)
            return getVelocityTowardsFlag();

        else
            return Vector2.zero;
    }
```

**Why:** The fallback to `getVelocityTowardsFlag()` is now gated behind `allowDirectFallbackWhenNoPath`. With this flag `false` (the new default), the frog stops when A* has no path — it does not try to walk directly through obstacles. The `_currentPath.Count` → `_currentPath.Length` change is because `_currentPath` is now `Node[]` (array) not `List<Vector2>`.

---

## 5. Inspector Setup (required — code alone is not enough)

After making all the above code changes, these Inspector values must be set manually in the Unity Editor.

### On the Pathfinding / AStarGrid GameObject:

| Field | Value | Why |
|---|---|---|
| Unwalkable Mask | `Obstacle` layer | Rocks and trees must be on this layer. If left as "Nothing", A* sees no obstacles and draws straight-line paths through walls. |
| Dynamic Obstacle Mask | `DynamicObstacle` layer | Snake must be on this layer. See below. |
| Grid Size | `0.5` | Node radius = 0.5, so nodes are 1 unit apart. |
| Grid World Size | Match your scene size | Should cover the full playfield. |
| Overlap Circle Radius | `0.4` | Slightly smaller than node radius to avoid marking adjacent cells as blocked. |
| Heuristic Type | `Euclidean` (default) | Toggle to demo heuristic differences. |
| Enable Path Smoothing | `true` (default) | Toggle off to show raw A* paths for heuristic demo. |
| Include Diagonal Neighbours | `true` | Required for 8-direction movement. |
| Display Grid Gizmos | `true` | Shows the grid overlay in the Scene view. |
| Display Terrain Gizmos | `true` | Shows terrain color overlay — needed for the demo. |
| Display Path Gizmos | `true` | Shows the computed path in Scene view. |

### On the Snake1 GameObject:

| Field | Value |
|---|---|
| Layer | `DynamicObstacle` |

(Already confirmed set correctly — visible in Inspector screenshot.)

---

## 6. Scene Setup for Terrain Demo

The Varying Terrain enhancement requires physical GameObjects in the scene.

1. **Create layers:** Edit → Project Settings → Tags and Layers → add `Mud`, `Water`, `Grass`
2. **Set AStarGrid masks:** In Inspector, set `Mud Mask` → `Mud`, `Water Mask` → `Water`, `Grass Mask` → `Grass`
3. **Create a terrain patch:**
   - Hierarchy → Right-click → Create Empty → name it `TerrainPatch_Water`
   - Add Component → Box Collider 2D → tick **Is Trigger**
   - Set Layer → `Water`
   - Scale the Transform to cover a visible area (e.g. X=6, Y=2)
   - Optional: add a Sprite Renderer with a blue tint for visibility
   - Place it somewhere the frog's direct path will cross

4. **Verify in Play mode:** With Display Grid Gizmos + Display Terrain Gizmos both on, the water patch should show as cyan in the grid overlay. Click a target on the other side — A* should route around it rather than through it (water cost = 5).

---

## 7. Demo Video Checklist

| Feature | How to demonstrate |
|---|---|
| **8-direction A***| Show frog navigating diagonally around corners |
| **Only recalculates when needed** | Show path persisting until you click again or snake moves onto path |
| **Varying Terrain** | Show gizmo terrain colors. Click through water — frog routes around it. Lower `waterCost` to 1 at runtime — frog cuts through. |
| **Varying Heuristics** | Turn `enablePathSmoothing` OFF first. Switch between Manhattan and Chebyshev — different frontier widths visible in gizmos. |
| **Path Smoothing** | Toggle `enablePathSmoothing` on/off — show smooth vs jagged path in gizmos. |
| **Dynamic Obstacles** | Walk snake onto frog's path — frog reroutes within 0.3 seconds. |

> **Important for heuristic demo:** Always disable path smoothing first before switching heuristics. Smoothing eliminates the visual difference between heuristics on open terrain.

---

## 8. File Change Summary

| File | Changes |
|---|---|
| `Node.cs` | Added TerrainType enum, terrainType field, movementCost field, extended constructor and Clone() |
| `AStarGrid.cs` | Full rewrite: removed embedded A*, removed inner Node class, added dynamicObstacleMask, Chebyshev heuristic, GetStepCost, IsPointBlockedByDynamicObstacle, ResetSearchData, corner-cutting prevention, guard conditions, proper ClosestWalkableNode |
| `Pathfinding.cs` | Filled in all A* TODO stubs, added EnsureInitialized, dynamic obstacle check per-neighbour, terrain-aware GCost, heuristic delegation, SmoothPath, RecordPath calls |
| `Frog.cs` | Replaced AStarGrid direct call with Pathfinding.RequestPath static, added RequestPathTo, TryRecalculatePathForDynamicObstacles, Seek/Arrive split, arrivedAtFinal, fixed defaults |

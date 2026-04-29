# Assignment 2 – Pathfinding and MCTS: Complete Code Change Log & Development Guide

> **GAIT2610 / COSC2527 / COSC3144 — Semester 1 2026**
> Due: Friday 1 May 2026, 11:59 PM AEST | Weight: 30%
>
> This document is a **full A-to-Z audit** of every code change made from the starter code to the
> current codebase, with exact file paths, line numbers, the code that changed, and the justification
> for why it was done that way. It also flags what is still missing from the spec.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [How the Two Games Work](#2-how-the-two-games-work)
3. [Lab 5 vs Starter Code vs Current Code](#3-lab-5-vs-starter-code-vs-current-code)
4. [File-by-File Change Log (Starter → Current)](#4-file-by-file-change-log)
   - [Node.cs](#41-nodecs)
   - [AStarGrid.cs](#42-astargridcs)
   - [Pathfinding.cs](#43-pathfindingcs)
   - [Frog.cs](#44-frogcs)
   - [Snake.cs](#45-snakecs)
   - [Fly.cs](#46-flycs)
   - [Steering.cs](#47-steeringcs)
   - [DrawGUI.cs](#48-drawguics)
   - [Globals.cs / FlockSettings.cs](#49-globalcs--flocksettingscs)
   - [Connect4 Scripts](#410-connect4-scripts)
5. [What the Lab 5 Code Adds as Reference](#5-what-the-lab-5-code-adds-as-reference)
6. [Spec Compliance Audit — What Is Done, What Is Missing](#6-spec-compliance-audit)
7. [What Each Team Member Needs to Do to Finish the Project](#7-what-each-team-member-needs-to-do-to-finish-the-project)
8. [Unity Scene Setup Notes](#8-unity-scene-setup-notes)
9. [Demo Video Checklist](#9-demo-video-checklist)

---

## 1. Project Structure

```
Assets/
├── Scripts/
│   ├── Pathfinding/
│   │   ├── Node.cs           ← grid cell data + terrain type (CHANGED from starter)
│   │   ├── Heap.cs           ← priority queue (UNCHANGED from starter)
│   │   ├── AStarGrid.cs      ← grid creation, terrain, heuristics, smoothing (CHANGED)
│   │   └── Pathfinding.cs    ← A* algorithm implementation (CHANGED)
│   ├── Connect4/
│   │   ├── Agent.cs          ← abstract base (UNCHANGED)
│   │   ├── Connect4State.cs  ← board state + win detection (UNCHANGED)
│   │   ├── GameController.cs ← game loop + UI (UNCHANGED)
│   │   ├── MCTSAgent.cs      ← MCTS stub — TODO still random (UNCHANGED)
│   │   ├── MonteCarloAgent.cs← MCS stub — TODO still random (UNCHANGED)
│   │   ├── RandomAgent.cs    ← baseline random AI (UNCHANGED)
│   │   └── CameraSize.cs     ← camera scaler (UNCHANGED)
│   ├── Frog.cs               ← frog movement + A* path following (CHANGED)
│   ├── Snake.cs              ← FSM patrol/attack (UNCHANGED)
│   ├── Fly.cs                ← flocking FSM (UNCHANGED)
│   ├── Steering.cs           ← seek/arrive/flee/separation etc. (UNCHANGED)
│   ├── Globals.cs            ← constants (UNCHANGED)
│   ├── DrawGUI.cs            ← health hearts UI (UNCHANGED — still hardcoded)
│   └── FlockSettings.cs      ← flocking parameters (UNCHANGED)
├── Scenes/
│   ├── FrogGame.unity        ← Part 1 scene
│   └── Connect4.unity        ← Part 2 scene
```

---

## 2. How the Two Games Work

### Part 1 — Frog Game

- The **Frog** moves by A* pathfinding when the player right-clicks. The path is computed in
  `Pathfinding.cs` using nodes from `AStarGrid.cs`. The frog then follows waypoints in
  `Frog.cs`, using `Steering.SeekDirect` for intermediate waypoints and `Steering.ArriveDirect`
  for the final waypoint so it slows down naturally.
- **Snakes** patrol between a home and patrol point using a Finite State Machine (FSM). If the
  frog comes within `AggroRange`, the snake switches to Attack state and chases the frog. After
  biting the frog once, it goes Benign and retreats home.
- **Flies** flock together using separation, cohesion, and alignment forces. When the frog is
  close they flee. When eaten they respawn after `RespawnTime` seconds.
- The **A* grid** covers the scene, marks rocks and trees as unwalkable, detects terrain type
  (mud/water/grass) for movement cost weighting, and supports path smoothing and dynamic obstacle
  avoidance.

### Part 2 — Connect Four

- A 6×7 board. Yellow moves first (randomised in `Connect4State()`).
- **Agents** implement `GetMove(Connect4State state)`. The `GameController` calls this each turn.
- Three agents exist: `RandomAgent` (done), `MonteCarloAgent` (TODO), `MCTSAgent` (TODO).
- Game state is managed by `Connect4State`. Win-detection checks vertical, horizontal, and all
  four diagonal directions.

---

## 3. Lab 5 vs Starter Code vs Current Code

There are three code bases relevant to this project:

| Code base | Location | Purpose |
|---|---|---|
| **Lab 5** | `SEM 2/GAMES & AI/Lab/5/Assets/Scripts/` | Tutor's basic working A* with TODO gaps — use as a reference for what a minimal correct A* looks like |
| **Starter Code** | `SEM 2/GAMES & AI/starter Code/Assets/Scripts/` | The official GitHub Classroom starting point — what was handed to you |
| **Current code** | `SEM 2/GAMES & AI/Assignment 2/Assets/Scripts/` | What has been implemented so far on top of the starter |

The starter code and Lab 5 share the same skeleton for `AStarGrid.cs`, `Pathfinding.cs`, and `Node.cs` — both have the same TODO gaps. The starter code **adds** `Frog.cs` with steering, `Snake.cs`, `Fly.cs`, `Steering.cs`, and all the Connect4 scripts, which Lab 5 does not have.

---

## 4. File-by-File Change Log

---

### 4.1 Node.cs

**File:** `Assets/Scripts/Pathfinding/Node.cs`

#### What the starter had

```csharp
// Starter code Node.cs — lines 31-37
public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY)
{
    walkable = _walkable;
    worldPosition = _worldPos;
    gridX = _gridX;
    gridY = _gridY;
}

// Clone() — line 39-42
public Node Clone()
{
    return new Node(walkable, worldPosition, gridX, gridY);
}
```

No terrain fields at all.

#### What was added — Lines 9–51

```csharp
// Lines 9–15: New TerrainType enum
public enum TerrainType
{
    Normal,
    Mud,
    Water,
    Grass
}

// Lines 37–38: New terrain fields
public TerrainType terrainType;
public float movementCost;

// Lines 43–51: Updated constructor
public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY,
            TerrainType _terrainType = TerrainType.Normal, float _movementCost = 1f)
{
    walkable = _walkable;
    worldPosition = _worldPos;
    gridX = _gridX;
    gridY = _gridY;
    terrainType = _terrainType;
    movementCost = _movementCost;
}

// Lines 53–56: Updated Clone() to preserve terrain data
public Node Clone()
{
    return new Node(walkable, worldPosition, gridX, gridY, terrainType, movementCost);
}
```

**Why:** The spec requires "Varying Terrain" (2 marks) — different terrain types that slow or
speed up the frog. To make A* aware of terrain cost, each grid cell (Node) must store its terrain
type and the movement cost multiplier for that terrain. The `movementCost` is read by
`AStarGrid.GetStepCost()` and fed into the g(n) calculation in `Pathfinding.cs`, so paths through
cheap terrain are genuinely preferred. Default values (`TerrainType.Normal, 1f`) keep the starter
behaviour unchanged where no terrain layer is assigned.

---

### 4.2 AStarGrid.cs

**File:** `Assets/Scripts/Pathfinding/AStarGrid.cs`

This is the most heavily changed file. The starter was a minimal skeleton; the current version
adds terrain, heuristics, path smoothing, dynamic obstacle support, and robust gizmo debugging.

#### Change 1 — New Inspector fields (lines 8–44)

**Starter had only:**
```csharp
public bool displayGridGizmos;
public LayerMask unwalkableMask;
public Vector2 gridWorldSize;
public float gridSize;
public float overlapCircleRadius;
public bool includeDiagonalNeighbours; // unused — had TODO comment
```

**Current code adds (lines 8–44):**
```csharp
public bool displayGridGizmos;
public bool displayTerrainGizmos;   // NEW — toggle terrain colour in gizmos
public bool displayPathGizmos;      // NEW — show last computed path in Scene view

[Header("Obstacle Layers")]
public LayerMask unwalkableMask;
public LayerMask dynamicObstacleMask;   // NEW — for moving obstacles

[Header("Terrain Layers")]
public LayerMask mudMask;     // NEW
public LayerMask waterMask;   // NEW
public LayerMask grassMask;   // NEW

[Header("Terrain Costs")]
public float normalCost = 1f;   // NEW
public float mudCost = 3f;      // NEW — mud is 3× slower
public float waterCost = 5f;    // NEW — water is 5× slower
public float grassCost = 2f;    // NEW — grass is 2× slower

[Header("Heuristics")]
public PathHeuristic heuristicType = PathHeuristic.Euclidean;  // NEW

[Header("Path Smoothing")]
public bool enablePathSmoothing = true;   // NEW

[Header("Terrain Colors")]
public Color normalColor = Color.white;
public Color mudColor = new Color(0.4f, 0.25f, 0.1f);
public Color waterColor = Color.cyan;
public Color grassColor = Color.green;
```

**Why:** Every A* enhancement required by the spec (terrain, multiple heuristics, path smoothing,
dynamic obstacles) needs to be configurable from the Unity Inspector without code changes. Putting
them as serialized public fields means you can toggle them live in Play Mode to demonstrate each
feature in the demo video. The `Header` attributes group related settings cleanly.

#### Change 2 — PathHeuristic enum (lines 49–59)

```csharp
public enum PathHeuristic
{
    Euclidean,
    Manhattan,
    Octile,
    // Chebyshev: max(dx, dy) — always admissible because the cheapest possible step
    // costs 1.0 and we need at least max(dx,dy) steps, so it never overestimates.
    // It is LESS informed than Euclidean, so A* expands more nodes — visible in gizmos.
    Chebyshev
}
```

**Why:** The spec requires "Varying Heuristics" (2 marks) and asks for "admissible heuristics of
your own invention beyond just Manhattan or Euclidean." Chebyshev distance (`max(dx, dy)`) is the
custom admissible heuristic added here — it is provably admissible because no path of cost less
than `max(dx,dy)` can exist in 8-direction grid movement. Having a dropdown lets you toggle
between heuristics in the Inspector to show each one's effect in the demo.

#### Change 3 — MaxSize overflow fix (lines 74–91)

**Starter:**
```csharp
public int MaxSize
{
    get { return gridSizeX * gridSizeY; }
}
```

**Current:**
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

**Why:** If the grid is large (say 200×200 = 40,000 nodes) the multiplication can overflow a 32-bit
int and produce a negative number, which would crash the heap constructor with an
`IndexOutOfRangeException`. Casting to `long` first before clamping prevents this.

#### Change 4 — CreateGrid() rewrite with validation + terrain detection (lines 93–149)

**Starter:**
```csharp
void Awake()
{
    nodeDiameter = gridSize * 2;
    gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
    gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
    CreateGrid();
}

public void CreateGrid()
{
    grid = new Node[gridSizeX, gridSizeY];
    Vector2 worldBottomLeft = (Vector2)transform.position - ...;

    for (int x = 0; x < gridSizeX; x++)
    {
        for (int y = 0; y < gridSizeY; y++)
        {
            ...
            bool walkable = (Physics2D.OverlapCircle(..., unwalkableMask) == null);
            grid[x, y] = new Node(walkable, worldPoint, x, y);
        }
    }
}
```

**Current — lines 69–149:**
```csharp
void Awake()
{
    CreateGrid();   // nodeDiameter computed inside CreateGrid now
}

public void CreateGrid()
{
    // Guard: if gridSize <= 0, auto-correct to 0.5 (prevents division by zero)
    if (gridSize <= 0f) { ... gridSize = 0.5f; }
    if (gridWorldSize.x <= 0f || gridWorldSize.y <= 0f) { ... }
    if (overlapCircleRadius <= 0f) { ... }

    nodeDiameter = gridSize * 2f;
    gridSizeX = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.x / nodeDiameter));
    gridSizeY = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.y / nodeDiameter));

    grid = new Node[gridSizeX, gridSizeY];
    worldBottomLeft = (Vector2)transform.position - ...;   // stored as class field

    for (int x = 0; x < gridSizeX; x++)
    {
        for (int y = 0; y < gridSizeY; y++)
        {
            ...
            bool blockedByStatic = Physics2D.OverlapCircle(..., unwalkableMask) != null;
            bool walkable = !blockedByStatic;

            Node.TerrainType terrainType = GetTerrainTypeAtPoint(worldPoint);
            float movementCost = GetTerrainCost(terrainType);
            grid[x, y] = new Node(walkable, worldPoint, x, y, terrainType, movementCost);
        }
    }
}
```

**Why:**
- The guard clauses prevent Unity from throwing exceptions when a developer forgets to set grid
  parameters in the Inspector. This is defensive programming at system boundaries.
- `worldBottomLeft` is now a class field (not local) so `NodeFromWorldPoint()` can use it without
  recalculating — removing a subtle rounding bug present in the starter.
- Dynamic obstacles are deliberately NOT baked into walkability at grid-creation time (line 140
  comment). Dynamic obstacles block paths only at path-request time, via the
  `IsPointBlockedByDynamicObstacle()` check in `Pathfinding.cs`. This allows moving obstacles to
  become passable again once they move away.
- `GetTerrainTypeAtPoint()` / `GetTerrainCost()` store the terrain cost in each Node at
  creation time, so A* can read it cheaply at search time without repeating physics queries.

#### Change 5 — GetNeighbours() with 8-direction + corner clipping (lines 151–194)

**Starter:**
```csharp
public List<Node> GetNeighbours(Node node)
{
    // TODO: Update to include diagonals if includeDiagonalNeighbours == true
    List<Node> neighbours = new List<Node>();
    if (node.gridX - 1 > 0) neighbours.Add(grid[node.gridX - 1, node.gridY]);  // Left
    if (node.gridX + 1 < gridSizeX) neighbours.Add(grid[node.gridX + 1, node.gridY]);  // Right
    if (node.gridY - 1 > 0) neighbours.Add(grid[node.gridX, node.gridY - 1]);  // Up
    if (node.gridY + 1 < gridSizeY) neighbours.Add(grid[node.gridX, node.gridY + 1]);  // Down
    return neighbours;
}
```

**Current — lines 151–194:**
```csharp
public List<Node> GetNeighbours(Node node)
{
    List<Node> neighbours = new List<Node>();

    for (int x = -1; x <= 1; x++)
    {
        for (int y = -1; y <= 1; y++)
        {
            if (x == 0 && y == 0) continue;   // skip self

            if (!includeDiagonalNeighbours && Mathf.Abs(x) + Mathf.Abs(y) == 2)
                continue;   // skip diagonals if flag is off

            int checkX = node.gridX + x;
            int checkY = node.gridY + y;

            if (!InBounds(checkX, checkY)) continue;

            // Corner clipping prevention (lines 179–187):
            // A diagonal step (x==±1, y==±1) is only allowed if BOTH the horizontal
            // and vertical orthogonal neighbours are also walkable.
            // Without this, the frog could cut through a wall corner diagonally.
            if (Mathf.Abs(x) == 1 && Mathf.Abs(y) == 1)
            {
                bool hWalkable = InBounds(node.gridX + x, node.gridY) && grid[node.gridX + x, node.gridY].walkable;
                bool vWalkable = InBounds(node.gridX, node.gridY + y) && grid[node.gridX, node.gridY + y].walkable;
                if (!hWalkable || !vWalkable) continue;
            }

            neighbours.Add(grid[checkX, checkY]);
        }
    }
    return neighbours;
}
```

**Why:** The spec explicitly requires "both orthogonal and diagonal movement" and "should not cause
the frog to bump into corners." The starter's TODO was to add diagonal support. The nested loop
replaces the four explicit cases cleanly and also implements corner clipping — if a diagonal
neighbour would require squeezing through a gap between two unwalkable cells (one horizontal, one
vertical from the current position), it is excluded. Without this check the frog could teleport
through thin walls diagonally, which looks wrong and breaks gameplay.

Also note: the starter had a bug — `node.gridX - 1 > 0` should be `>= 0` (it misses column 0).
The current code uses `InBounds()` which checks `>= 0`, fixing this.

#### Change 6 — GetHeuristicDistance() (lines 196–219)

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
            return Mathf.Max(dx, dy);   // custom admissible heuristic
        default: // Euclidean
            return Mathf.Sqrt(dx * dx + dy * dy);
    }
}
```

**Why:** The starter `Heuristic()` returned `0` (uniform cost search, not A*). This method
implements all four required heuristic options. Each is admissible (never overestimates):
- **Euclidean**: straight-line distance — always <= actual grid path.
- **Manhattan**: `dx + dy` — admissible only for 4-direction grids. With 8 directions it slightly
  underestimates, so it's still valid but less informed, causing A* to explore more nodes.
- **Octile**: the best admissible heuristic for 8-direction grids — accounts for diagonal moves
  at cost √2 and straight moves at cost 1. Most informed, fewest nodes explored.
- **Chebyshev** (custom): `max(dx, dy)` — underestimates more than Euclidean, so A* is less
  informed and the search frontier is visibly wider in the gizmos. Included specifically because
  the spec asks for "admissible heuristics of your own invention beyond Manhattan or Euclidean."

#### Change 7 — GetStepCost() terrain-weighted (lines 221–225)

```csharp
public float GetStepCost(Node from, Node to)
{
    float baseStepCost = Vector2.Distance(from.worldPosition, to.worldPosition);
    return baseStepCost * to.movementCost;
}
```

**Why:** The starter `GCost()` returned `1.0f` regardless of terrain or distance. This meant
diagonal moves were not correctly penalised (diagonal distance ≈ 1.41, not 1.0). The current
version uses the actual Euclidean distance between node centres, then multiplies by the
destination node's `movementCost`. So a diagonal step through mud costs `1.41 × 3 = 4.23`
versus a straight step on normal terrain costing `1.0`. This is what makes the frog genuinely
prefer longer flat paths over shorter muddy ones — which the spec requires as the visible
demonstration of terrain-weighted A*.

#### Change 8 — IsPathSegmentClear() for path smoothing (lines 227–231)

```csharp
public bool IsPathSegmentClear(Vector2 from, Vector2 to)
{
    LayerMask blockingMask = unwalkableMask | dynamicObstacleMask;
    return Physics2D.Linecast(from, to, blockingMask) == false;
}
```

**Why:** Path smoothing works by checking if two non-adjacent waypoints have a clear line of sight
between them. If yes, the intermediate waypoints can be removed. `Physics2D.Linecast` is used (not
`Raycast`) because it returns true on ANY hit along the segment, which is exactly what is needed.
Both static and dynamic obstacles are included in the blocking mask so a smoothed path does not
walk straight through a moving obstacle.

#### Change 9 — IsPointBlockedByDynamicObstacle() (lines 233–236)

```csharp
public bool IsPointBlockedByDynamicObstacle(Vector2 worldPoint)
{
    return Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, dynamicObstacleMask) != null;
}
```

**Why:** During periodic dynamic repath checks (`Frog.TryRecalculatePathForDynamicObstacles()`),
each remaining waypoint on the current path is tested against this to see if a moving obstacle
has entered the path. This uses the same `overlapCircleRadius` as static grid creation so
obstacle detection is consistent.

#### Change 10 — RecordPath() and lastWorldPath gizmo (lines 238–251, 373–380)

```csharp
// Line 47: new field
[HideInInspector]
public Vector2[] lastWorldPath;

// Lines 238-251: new method
public void RecordPath(Node[] path)
{
    if (path == null || path.Length == 0) { lastWorldPath = null; return; }
    lastWorldPath = new Vector2[path.Length];
    for (int i = 0; i < path.Length; i++)
        lastWorldPath[i] = path[i].worldPosition;
}

// Lines 373-380 in OnDrawGizmos():
if (displayPathGizmos && lastWorldPath != null && lastWorldPath.Length > 1)
{
    Gizmos.color = Color.yellow;
    for (int i = 0; i < lastWorldPath.Length - 1; i++)
        Gizmos.DrawLine(lastWorldPath[i], lastWorldPath[i + 1]);
}
```

**Why:** The spec requires visual demonstration of pathfinding in the demo video. The gizmo path
overlay (yellow lines in the Scene view) shows exactly which nodes the last A* search chose,
including whether path smoothing removed intermediate waypoints. The `displayPathGizmos` toggle
lets you compare smoothed vs. unsmoothed paths visually.

#### Change 11 — NodeFromWorldPoint() fix (lines 253–268)

**Starter:**
```csharp
public Node NodeFromWorldPoint(Vector2 worldPosition)
{
    float percentX = (worldPosition.x + gridWorldSize.x / 2) / gridWorldSize.x;
    float percentY = (worldPosition.y + gridWorldSize.y / 2) / gridWorldSize.y;
    ...
}
```

**Current:**
```csharp
public Node NodeFromWorldPoint(Vector2 worldPosition)
{
    if (grid == null || gridSizeX <= 0 || gridSizeY <= 0) return null;

    float percentX = (worldPosition.x - worldBottomLeft.x) / gridWorldSize.x;
    float percentY = (worldPosition.y - worldBottomLeft.y) / gridWorldSize.y;
    percentX = Mathf.Clamp01(percentX);
    percentY = Mathf.Clamp01(percentY);
    ...
}
```

**Why:** The starter formula assumed the grid's centre was always at world origin `(0,0)`. The
current code subtracts the stored `worldBottomLeft` (which is the grid's actual bottom-left corner
relative to the grid's own `transform.position`), so the grid can be placed anywhere in the world.
The null guard prevents a crash if the grid has not finished initialising yet (e.g., when scripts
call `RequestPath` very early).

#### Change 12 — ResetSearchData() (lines 270–283)

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

**Why:** Because nodes persist between path searches (they live on the grid), `gCost`, `hCost`,
and `parent` from a previous search could interfere with the next search. `Pathfinding.FindPath()`
calls `grid.ResetSearchData()` at the start of every search. Setting gCost to `+Infinity` means
any newly found path to a node will always be cheaper, which is the correct initial condition for
A*.

#### Change 13 — Enhanced OnDrawGizmos() with terrain colors (lines 352–381)

**Starter:** only drew red (unwalkable) or white (walkable).

**Current (lines 352–381):**
```csharp
void OnDrawGizmos()
{
    Gizmos.DrawWireCube(transform.position, new Vector2(gridWorldSize.x, gridWorldSize.y));

    if (grid != null && displayGridGizmos)
    {
        foreach (Node n in grid)
        {
            if (!n.walkable)
                Gizmos.color = Color.red;
            else
                Gizmos.color = displayTerrainGizmos ? GetTerrainColor(n.terrainType) : Color.white;

            Gizmos.DrawCube(n.worldPosition, Vector3.one * (nodeDiameter - 0.1f));
        }
    }

    if (displayPathGizmos && lastWorldPath != null && lastWorldPath.Length > 1)
    {
        Gizmos.color = Color.yellow;
        for (int i = 0; i < lastWorldPath.Length - 1; i++)
            Gizmos.DrawLine(lastWorldPath[i], lastWorldPath[i + 1]);
    }
}
```

**Why:** The spec (Figure 2) explicitly shows what the gizmos should look like — red for
unwalkable, colour-coded for terrain type. `displayTerrainGizmos` toggles between terrain colours
and plain white, useful for showing the gizmo before/after terrain is added in the demo. The path
gizmo (yellow line) lets the assessor see the A* path without running the game.

#### Change 14 — Private helper methods for terrain (lines 383–431)

```csharp
private Node.TerrainType GetTerrainTypeAtPoint(Vector2 worldPoint)
{
    if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, mudMask) != null) return Node.TerrainType.Mud;
    if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, waterMask) != null) return Node.TerrainType.Water;
    if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, grassMask) != null) return Node.TerrainType.Grass;
    return Node.TerrainType.Normal;
}

private float GetTerrainCost(Node.TerrainType terrainType)
{
    switch (terrainType) {
        case Node.TerrainType.Mud: return mudCost;
        case Node.TerrainType.Water: return waterCost;
        case Node.TerrainType.Grass: return grassCost;
        default: return normalCost;
    }
}

private Color GetTerrainColor(Node.TerrainType terrainType) { ... }
```

**Why:** These are called once per node during `CreateGrid()`. They use `Physics2D.OverlapCircle`
to check which terrain layer each grid cell overlaps. Priority order matters: Mud is checked
first, then Water, then Grass — if a cell overlaps multiple layers (e.g., edge of mud and water),
the first match wins. This is deterministic and easy to reason about.

---

### 4.3 Pathfinding.cs

**File:** `Assets/Scripts/Pathfinding/Pathfinding.cs`

#### Change 1 — Static design + EnsureInitialized (lines 9–50)

**Starter:**
```csharp
public static AStarGrid grid;
static Pathfinding instance;

void Awake()
{
    grid = GetComponent<AStarGrid>();
    instance = this;
}

public static Node[] RequestPath(Vector2 from, Vector2 to)
{
    return instance.FindPath(from, to);  // crashes if instance is null
}
```

**Current:**
```csharp
public static AStarGrid grid;
static bool warnedNoGrid;

void Awake()
{
    grid = GetComponent<AStarGrid>();
    // instance removed — FindPath is now static
}

public static Node[] RequestPath(Vector2 from, Vector2 to)
{
    EnsureInitialized();   // safety: find grid if not set
    if (grid == null)
    {
        if (!warnedNoGrid) { Debug.LogWarning(...); warnedNoGrid = true; }
        return new Node[0];   // graceful failure
    }
    return FindPath(from, to);
}

private static void EnsureInitialized()
{
    if (grid == null)
        grid = UnityEngine.Object.FindFirstObjectByType<AStarGrid>();
    if (grid != null) warnedNoGrid = false;
}
```

**Why:** The starter used a singleton `instance` field which would throw a `NullReferenceException`
if `Pathfinding.RequestPath()` was called from another script's `Awake()` before Pathfinding's
own `Awake()` ran. `EnsureInitialized()` does a scene-wide fallback search (`FindFirstObjectByType`)
if the direct reference is missing. Making `FindPath` a static method removes the instance
dependency entirely. Returning `new Node[0]` on failure is safe — callers check for empty paths.

#### Change 2 — Complete A* implementation (lines 54–203)

The entire body of `FindPath()` was placeholder code (`if (false)`, `new Node[0]`). The current
code implements the full A* algorithm.

```csharp
// Line 64 — ADDED: reset g/h costs before each search
grid.ResetSearchData();

// Lines 112–117 — ADDED: initialise start node and add to open set
startNode.gCost = 0f;
startNode.hCost = Heuristic(startNode, targetNode);
startNode.parent = startNode;
openSet.Add(startNode);   // was empty TODO

// Lines 125–126 — ADDED: pop lowest-f node (was empty TODO)
Node currentNode = openSet.RemoveFirst();
closedSet.Add(currentNode);

// Lines 131–133 — ADDED: goal check (was `if (false)`)
if (currentNode == targetNode)
{
    pathSuccess = true;
}

// Lines 139 — ADDED: get actual neighbours (was `new Node[0]`)
List<Node> neighbours = grid.GetNeighbours(currentNode);

// Lines 143 — ADDED: real condition (was `if (false)`)
if (node.walkable && !closedSet.Contains(node) && !grid.IsPointBlockedByDynamicObstacle(node.worldPosition))

// Lines 146 — ADDED: terrain-aware g cost (was empty TODO)
float newCostToNeighbour = currentNode.gCost + GCost(currentNode, node);

// Lines 152 — ADDED: update condition (was `if (false)`)
if (!openSet.Contains(node) || newCostToNeighbour < node.gCost)

// Lines 155, 159, 163 — ADDED: set gCost, hCost, parent (were empty TODOs)
node.gCost = newCostToNeighbour;
node.hCost = Heuristic(node, targetNode);
node.parent = currentNode;

// Lines 169–178 — ADDED: heap management (was `if (false)`)
if (!openSet.Contains(node))
    openSet.Add(node);
else
    openSet.UpdateItem(node);

// Lines 190–196 — ADDED: path smoothing and recording
waypoints = RetracePath(startNode, targetNode);
if (grid.enablePathSmoothing)
    waypoints = SmoothPath(waypoints);
grid.RecordPath(waypoints);
```

**Why for each change:**
- `grid.ResetSearchData()` — described in AStarGrid changes.
- `openSet.Add(startNode)` — A* begins by putting the start in the open set with g=0.
- `openSet.RemoveFirst()` — extracts the node with the smallest f-cost (the heap maintains this).
- `closedSet.Add(currentNode)` — marks this node as fully explored; we never revisit it.
- `currentNode == targetNode` — terminates A* the moment we dequeue the goal node (not when we
  first encounter it as a neighbour). This is correct A* termination.
- `grid.GetNeighbours(currentNode)` — uses the new diagonal-aware neighbour method.
- Dynamic obstacle check in condition — if a dynamic obstacle now occupies a previously walkable
  node, we skip it, causing A* to route around the current obstacle position.
- `GCost(currentNode, node)` → `grid.GetStepCost()` — terrain-weighted cost.
- `openSet.UpdateItem(node)` — crucial: if a node is already in the open set but we found a
  cheaper path to it, we update its position in the heap. Without this call the heap ordering
  would become stale and A* would produce non-optimal paths.
- `SmoothPath()` after path found — applies line-of-sight smoothing before the path is returned.

#### Change 3 — RetracePath() full implementation (lines 207–236)

**Starter:**
```csharp
Node[] RetracePath(Node startNode, Node endNode)
{
    List<Node> path = new List<Node>();
    // TODO: begin from endNode
    while (false)  // TODO: loop until startNode
    {
        // TODO: add current, move to parent
    }
    Node[] waypoints = path.ToArray();
    Array.Reverse(waypoints);
    return waypoints;
}
```

**Current:**
```csharp
static Node[] RetracePath(Node startNode, Node endNode)
{
    List<Node> path = new List<Node>();
    Node currentNode = endNode;

    while (currentNode != startNode)
    {
        path.Add(currentNode);
        currentNode = currentNode.parent;
        if (currentNode == null) break;   // safety guard
    }

    Node[] waypoints = path.ToArray();
    Array.Reverse(waypoints);
    return waypoints;
}
```

**Why:** Retrace follows `parent` pointers from the goal back to the start — the path that A*
built up during exploration. Reversing gives start→goal order. The null guard on `currentNode`
prevents an infinite loop if the parent chain is broken (defensive coding). The `startNode` itself
is deliberately NOT added because the frog is already at the start position.

#### Change 4 — GCost and Heuristic delegates (lines 238–247)

**Starter:**
```csharp
private float GCost(Node nodeA, Node nodeB) { return 1.0f; }
private float Heuristic(Node nodeA, Node nodeB) { return 0; }
```

**Current:**
```csharp
static float GCost(Node nodeA, Node nodeB)    { return grid.GetStepCost(nodeA, nodeB); }
static float Heuristic(Node nodeA, Node nodeB) { return grid.GetHeuristicDistance(nodeA, nodeB); }
```

**Why:** Centralising cost functions in `AStarGrid` keeps all A* behaviour configurable from the
Inspector (terrain costs, heuristic type). The `Pathfinding` class is now just the algorithm;
the `AStarGrid` is the knowledge base.

#### Change 5 — SmoothPath() (lines 249–283)

```csharp
static Node[] SmoothPath(Node[] originalPath)
{
    if (originalPath == null || originalPath.Length < 3) return originalPath;

    List<Node> smoothedPath = new List<Node>();
    int currentIndex = 0;
    smoothedPath.Add(originalPath[currentIndex]);

    while (currentIndex < originalPath.Length - 1)
    {
        int furthestVisible = currentIndex + 1;

        // Scan backward from end of path
        for (int candidate = originalPath.Length - 1; candidate > currentIndex; candidate--)
        {
            if (grid.IsPathSegmentClear(originalPath[currentIndex].worldPosition,
                                        originalPath[candidate].worldPosition))
            {
                furthestVisible = candidate;
                break;
            }
        }

        if (furthestVisible == currentIndex) break;  // safety
        currentIndex = furthestVisible;
        smoothedPath.Add(originalPath[currentIndex]);
    }

    return smoothedPath.ToArray();
}
```

**Why:** Path smoothing collapses a zig-zag A* path (which must follow the grid) into a smoother
path that goes directly from any waypoint to the furthest visible one. Scanning backward from the
end of the path (then stopping at the first clear segment) ensures we always jump as far as
possible, minimising waypoint count. `IsPathSegmentClear()` uses a linecast against both static
and dynamic obstacles, so a smoothed path never shortcuts through a wall or over a moving
obstacle. The result is that the frog appears to walk "naturally" rather than weaving through
grid cells — matching the spec requirement.

---

### 4.4 Frog.cs

**File:** `Assets/Scripts/Frog.cs`

#### Change 1 — A* path-following fields (lines 49–58)

**Starter:** No pathfinding fields at all.

**Current:**
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

**Why:** Following a path requires knowing the current path, which waypoint the frog is heading
to, and when to advance to the next one. `waypointTolerance` is the arrival distance — if the
frog is within this radius of the current waypoint it moves to the next. `dynamicRepathInterval`
controls how often the path is checked for dynamic obstacles (every 0.3 s avoids running physics
every frame). `_pathGoal` stores the original destination so re-paths target the same point.
`allowDirectFallbackWhenNoPath` is off by default — when on, the frog moves directly toward the
destination if A* fails, but this can cause it to walk through walls.

#### Change 2 — Start() initialises A* fields (lines 81–86)

```csharp
_lastClickPos = null;
_arriveRadius = MinArriveRadius;
_currentPath = null;    // ADDED
_pathIndex = 0;          // ADDED
_pathGoal = null;        // ADDED
_nextDynamicRepathTime = 0f;  // ADDED
```

**Why:** Unity does not zero-initialise class fields for reference types. Explicitly setting these
avoids stale path data if the scene is reloaded without a full restart.

#### Change 3 — Update() calls RequestPathTo + dynamic repath (lines 89–114)

**Starter:**
```csharp
void Update()
{
    if (ClickMoveAction.WasPressedThisFrame())
    {
        _lastClickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
        _arriveRadius = Mathf.Clamp(...);
        _flag.position = ...;
        _flagSr.enabled = true;
        // NO path request — frog moved directly via steering
    }
    else
    {
        if (closestFly != null) Debug.DrawLine(...);
        if (closestSnake != null) Debug.DrawLine(...);
    }
}
```

**Current (lines 89–114):**
```csharp
void Update()
{
    if (ClickMoveAction.WasPressedThisFrame())
    {
        _lastClickPos = ...;
        _arriveRadius = Mathf.Clamp(...);
        _flag.position = ...;
        _flagSr.enabled = true;
        RequestPathTo((Vector2)_lastClickPos);   // ADDED: triggers A* path computation
    }
    else
    {
        TryRecalculatePathForDynamicObstacles();   // ADDED: periodic repath check
        if (closestFly != null) Debug.DrawLine(...);
        if (closestSnake != null) Debug.DrawLine(...);
    }
}
```

**Why:** `RequestPathTo()` is called once per click (not every frame) — this satisfies the spec's
requirement "Only recalculate paths when needed (not every frame)." Sebastian Lague's approach of
refreshing every frame has "a needlessly high computational burden" which the spec explicitly warns
to avoid. `TryRecalculatePathForDynamicObstacles()` handles the dynamic obstacle case separately,
at a controlled interval.

#### Change 4 — decideMovement() with path following (lines 166–182)

**Starter:**
```csharp
private Vector2 decideMovement()
{
    if (_lastClickPos != null)
        return (getVelocityTowardsFlag());
    else
        return (Vector2.zero);
}
```

**Current:**
```csharp
private Vector2 decideMovement()
{
    if (_currentPath != null && _pathIndex < _currentPath.Length)
        return getVelocityAlongPath();   // A* path following

    if (allowDirectFallbackWhenNoPath && _lastClickPos != null)
        return (getVelocityTowardsFlag());   // direct steering fallback

    else
        return (Vector2.zero);
}
```

**Why:** The starter moved the frog directly toward the click via steering — it ignored obstacles.
The current code prioritises A* path following when a path exists. Direct steering is only used as
a fallback (and is off by default). This means the frog navigates around rocks, trees, and dynamic
obstacles via the computed waypoints.

#### Change 5 — getVelocityAlongPath() (lines 207–253)

```csharp
private Vector2 getVelocityAlongPath()
{
    if (_currentPath == null || _pathIndex >= _currentPath.Length) return Vector2.zero;

    Vector2 currentWaypoint = _currentPath[_pathIndex].worldPosition;

    if (drawPathDebugLines)
        Debug.DrawLine(transform.position, currentWaypoint, Color.yellow);

    bool isFinalWaypoint = (_pathIndex == _currentPath.Length - 1);
    float distanceToWaypoint = ((Vector2)transform.position - currentWaypoint).magnitude;

    // Lines 225–226: extra arrival check for final waypoint when physics slows the frog
    bool arrivedAtFinal = isFinalWaypoint && distanceToWaypoint <= _arriveRadius * 0.15f;

    if (distanceToWaypoint <= waypointTolerance || arrivedAtFinal)
    {
        _pathIndex++;
        if (_pathIndex >= _currentPath.Length)
        {
            _currentPath = null;
            _pathIndex = 0;
            _pathGoal = null;
            if (HideFlagOnceReached) _flagSr.enabled = false;
            return Vector2.zero;
        }
        currentWaypoint = _currentPath[_pathIndex].worldPosition;
    }

    // Lines 248–252: Seek for intermediate waypoints, Arrive for final
    if (isFinalWaypoint)
        return Steering.ArriveDirect(gameObject.transform.position, currentWaypoint, _arriveRadius, MaxSpeed);
    else
        return Steering.SeekDirect(gameObject.transform.position, currentWaypoint, MaxSpeed);
}
```

**Why:**
- **Seek for intermediates, Arrive for final** — using Arrive at every waypoint would make the
  frog slow down at every grid cell, producing jerky motion. Using Seek at intermediates keeps the
  frog moving at full speed through the path. Only at the final destination does Arrive slow it
  down gracefully. This makes the movement look natural.
- **`waypointTolerance`** — the frog is considered to have reached a waypoint when it is within
  0.5 units. This prevents the frog from stopping exactly at a grid-cell centre (hard due to
  physics inertia) and allows it to flow smoothly through the path.
- **`arrivedAtFinal`** — a secondary check for the last waypoint using `_arriveRadius * 0.15f`.
  When the frog arrives near the destination and physics friction slows it, it might never cross
  the `waypointTolerance` radius exactly. This extra check prevents the frog from hovering
  indefinitely near the goal.
- **Debug line** — yellow `DrawLine` shows which waypoint the frog is heading toward in the Game
  view during Play Mode, useful for the demo video.

#### Change 6 — RequestPathTo() (lines 255–275)

```csharp
private void RequestPathTo(Vector2 destination)
{
    Node[] path = Pathfinding.RequestPath(transform.position, destination);

    if (path != null && path.Length > 0)
    {
        _pathGoal = destination;
        _currentPath = path;
        _pathIndex = 0;
        _lastClickPos = null;   // clear direct steering target
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

**Why:** Centralises all path-request logic. `_lastClickPos = null` when a path is found because
the frog should now follow waypoints, not steer directly. Setting `_pathIndex = 0` resets to the
first waypoint each time a new path arrives.

#### Change 7 — TryRecalculatePathForDynamicObstacles() (lines 277–299)

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

**Why:** This implements dynamic obstacle avoidance. Every `dynamicRepathInterval` seconds (0.3 s
by default), the frog checks all remaining waypoints in its path against the dynamic obstacle mask.
If any waypoint is now blocked by a moving obstacle, the frog requests a fresh path from its
current position. The key design decisions:
- Only remaining waypoints are checked (from `_pathIndex` forward) — no point checking waypoints
  already passed.
- We repath to `_pathGoal` (the original destination), not to the next waypoint — this gives A*
  the full context to plan around the obstacle.
- The `dynamicRepathInterval` prevents this from running every frame. 0.3 s is a balance between
  responsiveness and performance.

---

### 4.5 Snake.cs

**No changes from starter.** The file is identical between the starter code and the current code.

The Snake has a complete FSM with PatrolAway → PatrolHome → Attack → Benign states. There is one
TODO comment on line 189: `//TODO update so that the snake attack only alive frogs`. This is a
minor polish point — currently the snake attacks the frog object regardless of whether the frog
is "dead" (health == 0).

---

### 4.6 Fly.cs

**No changes from starter.** The file is identical.

The Fly has a complete flocking FSM with Flocking, Alone, Fleeing, Dead, and Respawn states.
Flocking behaviour uses separation, cohesion, alignment, and anchor forces. Respawning happens
at a random angle 20 units from origin.

---

### 4.7 Steering.cs

**No changes from starter.** All methods were already implemented in the starter code:
- `SeekDirect()`, `ArriveDirect()`, `FleeDirect()` — basic steering
- `GetAvoidanceTarget()` — circle cast obstacle avoidance with angle deviation fallback
- `GetSeparation()`, `GetCohesion()`, `GetAlignment()` — flocking behaviours
- `GetAnchor()`, `DesiredVelToForce()`, `rotate()` — helpers

---

### 4.8 DrawGUI.cs

**No changes from starter, but contains a known issue.**

```csharp
// DrawGUI.cs line 27 — hardcoded to always show 3 hearts
for (int i = 0; i < 3; i++)
{
    GUI.DrawTexture(...);
}
```

The comment on line 25 acknowledges this: "the GUI is hardcoded to 3 health. The counts are wrong,
and don't change as the frog takes damage."

This needs to be fixed to satisfy the spec (health system should be visible). See missing items.

---

### 4.9 Globals.cs / FlockSettings.cs

**No changes from starter.**

`Globals.cs` defines two constants used throughout the project:
- `MIN_SPEED_TO_ANIMATE = 1.0f` — velocity threshold for triggering walk animation
- `TARGET_REACHED_TOLERANCE = 1.0f` — distance at which a target is considered reached

`FlockSettings.cs` holds serializable flocking parameters attached to the Flock game object.

---

### 4.10 Connect4 Scripts

**All Connect4 scripts are IDENTICAL between starter and current code.**

| File | Status | Notes |
|---|---|---|
| `Agent.cs` | Unchanged | Abstract base with `GetMove()`, `argMin()`, `argMax()` |
| `Connect4State.cs` | Unchanged | Full board state, `MakeMove()`, `GetResult()`, `Clone()` |
| `GameController.cs` | Unchanged | Game loop, piece drop animation, agent integration |
| `RandomAgent.cs` | Unchanged | Baseline random AI |
| `CameraSize.cs` | Unchanged | Orthographic size setter |
| `MCTSAgent.cs` | **TODO** | Currently returns random move — MCTS not implemented |
| `MonteCarloAgent.cs` | **TODO** | Currently returns random move — MCS not implemented |

---

## 5. What the Lab 5 Code Adds as Reference

The Lab 5 code (`SEM 2/GAMES & AI/Lab/5/`) is the tutor's basic A* reference implementation.
Compare it to the current code to understand what was added:

| Feature | Lab 5 | Current Assignment 2 |
|---|---|---|
| Grid creation | Basic, no validation | Input validation, terrain detection |
| Neighbours | 4-direction only, off-by-one bug | 8-direction, diagonal with corner clipping |
| A* algorithm | All TODOs empty (shell) | Fully implemented |
| G cost | Returns 1.0f (always) | Terrain-weighted Euclidean distance |
| Heuristic | Returns 0 (uniform cost) | 4 options: Euclidean/Manhattan/Octile/Chebyshev |
| Path smoothing | None | Line-of-sight smoothing |
| Dynamic obstacles | None | Runtime obstacle detection + periodic repath |
| Frog movement | Just draws path, no following | Waypoint following with Seek/Arrive |

The Lab 5 `FindWalkableInRadius()` has a bug — it passes arguments in wrong order to `InBounds()`
for the Right and Left searches (checks `centreY ± radius` but passes it as the x argument).
The starter and current code have the same bug copied in. It typically does not cause a crash
because `InBounds` rejects out-of-range indices, but the walkable search may miss some cells.
This is a minor issue unlikely to affect gameplay.

---

## 6. Spec Compliance Audit

### ✅ DONE — Part 1 A* Pathfinding

| Requirement | Marks | Status | Where |
|---|---|---|---|
| Frog follows A* path (8-direction, non-constant heuristic) | 2 | ✅ Done | `Pathfinding.cs`, `Frog.cs` |
| Only recalculate path when needed | Implicit | ✅ Done | `Frog.Update()` — on click only |
| Varying terrain (different walkable terrain types, modify g(n)) | 2 | ✅ Done | `Node.cs`, `AStarGrid.cs`, `Pathfinding.cs` |
| Gizmo shows terrain type (red=unwalkable, colour=terrain) | Implicit | ✅ Done | `AStarGrid.OnDrawGizmos()` |
| Varying heuristics (multiple, admissible custom heuristic) | 2 | ✅ Done | `AStarGrid.GetHeuristicDistance()` |
| Path smoothing (line-of-sight, doesn't cross avoided terrain) | 2 | ✅ Done | `Pathfinding.SmoothPath()`, `AStarGrid.IsPathSegmentClear()` |
| Dynamic obstacle avoidance with repath | 2 | ✅ Done | `Frog.TryRecalculatePathForDynamicObstacles()` |

### ❌ MISSING — Part 1 Decision Tree

| Requirement | Marks | Status | Action Needed |
|---|---|---|---|
| Decision Tree chooses where to send frog | 4 | ❌ NOT DONE | Implement `decideMovement()` DT logic |
| DT calls A* to move frog (not direct steering) | Implicit | ❌ NOT DONE | Connect DT output to `RequestPathTo()` |
| `findClosestSnake()` implemented | — | ❌ Empty | Fill in on `Snake.cs` lines 323–325 |
| `isOutOfScreen()` implemented | — | ❌ Returns false | Use Camera bounds check |
| Human/AI toggle for frog | Suggested | ❌ Missing | Add `public bool aiControlled` bool |
| Information Gain demonstration (10 training examples) | Required | ❌ Missing | Record 10 play examples, compute IG by hand |

**To implement the basic Decision Tree in `Frog.cs`:**

The spec's suggested DT structure (replace the body of `decideMovement()` or add it as an AI path
decision called from `Update()`):

```
IF health <= 0 THEN stop (return zero velocity, turn red)
ELSE IF frog is outside screen bounds THEN RequestPathTo(screen centre)
ELSE IF closest snake is within scaredRange AND snake is in Attack state
         THEN RequestPathTo(position far from snake, still on screen)
ELSE IF closest fly is within huntRange AND fly is not Dead
         THEN RequestPathTo(closestFly.transform.position)
ELSE RequestPathTo(screen centre)
```

For the DT to work you also need to call `findClosestFly()` and `findClosestSnake()` each update.

**Implementing `findClosestSnake()` (fill in `Frog.cs` lines 323–325):**
```csharp
private void findClosestSnake()
{
    distanceToClosestSnake = Mathf.Infinity;
    foreach (Snake snake in (Snake[])GameObject.FindObjectsByType(typeof(Snake), FindObjectsSortMode.None))
    {
        float d = (snake.transform.position - transform.position).magnitude;
        if (d < distanceToClosestSnake)
        {
            closestSnake = snake;
            distanceToClosestSnake = d;
        }
    }
}
```

**Implementing `isOutOfScreen()` (fill in `Frog.cs` lines 328–331):**
```csharp
private bool isOutOfScreen(Transform t)
{
    Vector3 vp = Camera.main.WorldToViewportPoint(t.position);
    return vp.x < 0 || vp.x > 1 || vp.y < 0 || vp.y > 1;
}
```

### ❌ MISSING — Part 2 Connect Four AI

| Requirement | Marks | Status | Action Needed |
|---|---|---|---|
| MonteCarloAgent — MCS implementation | Part of Part 2 | ❌ Returns random | Implement MCS |
| MCTSAgent — MCTS implementation | Part of Part 2 | ❌ Returns random | Implement MCTS with UCB |

**How to implement MonteCarloAgent:**
For each possible column, run `totalSims / numMoves` random simulations starting from
`state.Clone()` with that move applied. Track win/draw/loss counts. Return the column with
the best win rate.

```csharp
public override int GetMove(Connect4State state)
{
    List<int> moves = state.GetPossibleMoves();
    float[] scores = new float[GameController.numColumns];
    int simsPerMove = totalSims / moves.Count;

    foreach (int col in moves)
    {
        float wins = 0f;
        for (int i = 0; i < simsPerMove; i++)
        {
            Connect4State sim = state.Clone();
            sim.MakeMove(col);
            Connect4State.Result result = Simulate(sim);
            wins += Connect4State.ResultToFloat(result);
        }
        scores[col] = wins / simsPerMove;
    }
    return playerIdx == 0 ? argMin(scores) : argMax(scores);
}

private Connect4State.Result Simulate(Connect4State sim)
{
    Connect4State.Result result = sim.GetResult();
    while (result == Connect4State.Result.Undecided)
    {
        List<int> moves = sim.GetPossibleMoves();
        sim.MakeMove(moves[Random.Range(0, moves.Count)]);
        result = sim.GetResult();
    }
    return result;
}
```

**How to implement MCTSAgent:**
MCTS has four phases per simulation: Selection (UCB), Expansion, Simulation (random playout),
Backpropagation (update wins/visits up the tree). Needs a tree node class:

```csharp
private class MCTSNode
{
    public Connect4State state;
    public MCTSNode parent;
    public List<MCTSNode> children = new List<MCTSNode>();
    public float wins = 0f;
    public int visits = 0;
    public int moveFromParent;

    public float UCB(float c)
    {
        if (visits == 0) return float.MaxValue;
        return wins / visits + c * Mathf.Sqrt(Mathf.Log(parent.visits) / visits);
    }
}
```

### ❌ MISSING — Gameplay / Polish

| Item | Status | Notes |
|---|---|---|
| `DrawGUI.cs` shows actual frog health | ❌ Hardcoded 3 | Read `Frog.Health` dynamically |
| Snake attacks only alive frogs | ❌ TODO in Snake.cs | Check if `Frog.Health > 0` before attacking |
| Human/AI frog toggle | ❌ Not present | Add `public bool aiControlled` in `Frog.cs` |
| README.md filled in | ❌ Still placeholder | Add student IDs and names |

**Fixing DrawGUI.cs** — change line 27:
```csharp
// Get health from frog
Frog frog = FindFirstObjectByType<Frog>();
int health = frog != null ? frog.Health : 0;
for (int i = 0; i < health; i++)
{
    GUI.DrawTexture(new Rect(20 + (_iconSize + _iconSeparation) * i, 20, _iconSize, _iconSize), _heartTex, ScaleMode.ScaleToFit, true, 0.0f);
}
```

---

## 7. What Each Team Member Needs to Do to Finish the Project

### Member 1 — A* Pathfinding Specialist (already mostly done)

**Done:**
- A* movement with 8-direction support
- Non-constant heuristic (4 options)
- Recalculate only on click + periodic for dynamic obstacles
- Varying terrain integrated into g(n)
- Gizmo visualisation with terrain colours and path overlay
- Path smoothing (toggleable, line-of-sight based)
- Dynamic obstacle avoidance with periodic repath

**Still needed for demo:**
- Add at least one moving obstacle to the scene that uses the `dynamicObstacleMask` layer, so the
  frog visibly re-routes around it.
- Demonstrate in the video: toggle heuristics in Inspector, show wider search with Chebyshev vs
  Euclidean, show before/after path smoothing, show frog taking longer path around mud/water.
- Set up terrain tile objects with correct layer assignments (Mud layer, Water layer, Grass layer)
  in the Unity scene so `AStarGrid.CreateGrid()` can detect them.

### Member 2 — Decision Tree Specialist

**To implement:**
1. Fill in `findClosestSnake()` in `Frog.cs` (lines 323–325).
2. Fill in `isOutOfScreen()` in `Frog.cs` (lines 328–331).
3. Add `public bool aiControlled = false;` field to `Frog.cs`.
4. Add DT logic in `Update()` — when `aiControlled == true`, call `findClosestFly()`,
   `findClosestSnake()`, then evaluate the decision tree and call `RequestPathTo()` with the chosen
   destination.
5. Record 10 gameplay examples as a training set and compute Information Gain manually to
   demonstrate the first attribute split. Prepare a diagram of the DT that matches your code.
6. Create a diagram for the demo video showing the decision tree structure.
7. Fix `DrawGUI.cs` to show actual frog health.

### Member 3 — Connect4 / MCTS Specialist

**To implement:**
1. Implement `MonteCarloAgent.GetMove()` — pure Monte Carlo with random playouts.
2. Implement `MCTSAgent.GetMove()` — full MCTS with Selection (UCB), Expansion, Simulation,
   Backpropagation.
3. In the demo, show: MCS vs Random (MCS should win often), MCTS vs MCS (MCTS should win more),
   vary `totalSims` to show impact on play quality.

---

## 8. Unity Scene Setup Notes

### FrogGame Scene — Layer Setup Required for Terrain

The terrain system uses Unity Physics layers. You must:

1. Create layers in Unity: **Mud**, **Water**, **Grass** (Project Settings → Tags and Layers).
2. Create terrain tile prefabs — coloured sprites with a collider — assigned to those layers.
3. In the Inspector on the `AStarGrid` component (on the same GameObject as `Pathfinding`), assign:
   - `Mud Mask` → Mud layer
   - `Water Mask` → Water layer
   - `Grass Mask` → Grass layer
4. Place terrain tiles in the scene overlapping the walkable grid area.
5. Set `displayTerrainGizmos = true` to verify the grid picks up terrain colours.

### Dynamic Obstacle Setup

1. Create a layer called **DynamicObstacle**.
2. Create a moving obstacle prefab (e.g., a moving platform/snake/projectile) with a collider
   assigned to the **DynamicObstacle** layer.
3. On `AStarGrid`, assign `Dynamic Obstacle Mask` → DynamicObstacle layer.
4. The frog will automatically repath around this every `dynamicRepathInterval` seconds (default 0.3s).

### Connect4 Scene

Both scenes are in `Assets/Scenes/`. To switch agents in the Connect4 scene:
- Select the `GameController` GameObject.
- Drag the desired agent prefabs (`RandomAgent`, `MonteCarloAgent`, `MCTSAgent`, `HumanAgent`)
  into the `Yellow Agent` and `Red Agent` slots.

---

## 9. Demo Video Checklist

Use this in your recording — each item must be visible on screen to receive marks.

### Part 1 — A* and Decision Trees (18 marks)

**A* Base (2 marks)**
- [ ] Show frog right-clicking and following an A* path that avoids rocks and trees
- [ ] Show the path gizmo (yellow line in Scene view) updating when you click

**Varying Terrain (2 marks)**
- [ ] Show terrain gizmos (brown/cyan/green tiles)
- [ ] Show frog choosing a longer path on low-cost terrain instead of a shorter muddy/watery path

**Varying Heuristics (2 marks)**
- [ ] Switch heuristic in Inspector during Play Mode
- [ ] Show Chebyshev expanding more nodes (wider search frontier visible in gizmos)
- [ ] Show Octile being most efficient
- [ ] Explain admissibility of Chebyshev in voice-over

**Path Smoothing (2 marks)**
- [ ] Toggle `enablePathSmoothing` off — show zig-zag grid path
- [ ] Toggle on — show smoother diagonal path
- [ ] Show that smoothing does NOT cut through obstacles

**Dynamic Obstacles (2 marks)**
- [ ] Show a moving obstacle blocking the frog's path
- [ ] Show frog automatically repaths around it
- [ ] Explain the 0.3 s interval decision in voice-over

**Decision Tree (4 marks)**
- [ ] Show human toggle vs AI toggle
- [ ] Show DT diagram matching your code
- [ ] Show AI frog catching flies and fleeing snakes
- [ ] Show Information Gain calculation from 10 training examples (slide or whiteboard)

**Gameplay (4 marks)**
- [ ] At least 2 gameplay enhancement features demonstrated
- [ ] Natural-looking movement
- [ ] Stable game that doesn't crash during the demo

### Part 2 — Connect Four (remaining marks)

- [ ] Show MCS agent playing vs Random — MCS should win more
- [ ] Show MCTS agent playing vs MCS — MCTS should win more
- [ ] Vary `totalSims` and show its impact on play strength and thinking time
- [ ] Explain UCB formula in voice-over for MCTS

---

## References

- A* Implementation adapted from: Sebastian Lague — https://github.com/SebLague/Pathfinding-2D
- Connect Four Starter Kit by Eikester (Assets/Connect Four/readme.txt)
- Course slides: Weeks 5, 6, 7 — GAIT2610, RMIT University, Semester 1 2026
- Unity Documentation: Physics2D.Linecast, Physics2D.CircleCast, Physics2D.OverlapCircle
- Assignment 2 Specifications: GAIT2610_A2_specifications_part1.pdf, part2.pdf

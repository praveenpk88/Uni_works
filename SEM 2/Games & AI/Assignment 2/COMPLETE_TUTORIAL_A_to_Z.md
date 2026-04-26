# Member 1 Validation and Checklist - A* Pathfinding Specialist

Last updated: 2026-04-26

This document is a strict validation guide against the Member 1 checklist you provided.

## 1. Core Responsibilities Validation

### 1.1 A* Movement for Frog
Status: PASS

Implemented:
- Frog movement requests A* paths and follows waypoints.
- Static obstacles are avoided through unwalkable layer checks.

Where:
- Assets/Scripts/Frog.cs
- Assets/Scripts/Pathfinding/Pathfinding.cs
- Assets/Scripts/Pathfinding/AStarGrid.cs

### 1.2 8-Direction A*
Status: PASS

Implemented:
- Neighbor generation supports diagonal neighbors when includeDiagonalNeighbours is enabled.
- This is now true 8-directional A* behavior.

Where:
- Assets/Scripts/Pathfinding/AStarGrid.cs (GetNeighbours)

### 1.3 Non-Constant Heuristic
Status: PASS

Implemented:
- Heuristic options: Euclidean, Manhattan, Octile.
- Heuristic selected from AStarGrid inspector via heuristicType.

Where:
- Assets/Scripts/Pathfinding/AStarGrid.cs (PathHeuristic, GetHeuristicDistance)
- Assets/Scripts/Pathfinding/Pathfinding.cs (Heuristic)

### 1.4 Recalculate Paths Only When Needed
Status: PASS

Implemented:
- Repath on click target change.
- Repath at controlled interval when dynamic obstacles block remaining waypoints.
- No every-frame full path recomputation.

Where:
- Assets/Scripts/Frog.cs (RequestPathTo, TryRecalculatePathForDynamicObstacles, dynamicRepathInterval)

## 2. A* Enhancement Checks

### 2.1 Varying Terrain (2 marks)
Status: PASS

Implemented:
- Terrain types: Normal, Mud, Water, Grass.
- Terrain movement costs are applied in G-cost via GetStepCost.

Where:
- Assets/Scripts/Pathfinding/Node.cs
- Assets/Scripts/Pathfinding/AStarGrid.cs (terrain masks and costs)
- Assets/Scripts/Pathfinding/Pathfinding.cs (GCost)

### 2.2 Terrain Visualization with Distinct Gizmo Colors
Status: PASS

Implemented:
- Distinct colors for terrain categories and red for blocked cells.
- Toggle with displayTerrainGizmos.

Where:
- Assets/Scripts/Pathfinding/AStarGrid.cs (OnDrawGizmos, GetTerrainColor)

### 2.3 Varying Heuristics with Toggle (2 marks)
Status: PASS

Implemented:
- heuristicType enum in AStarGrid inspector.
- Supports multiple choices for demonstration.

Where:
- Assets/Scripts/Pathfinding/AStarGrid.cs

### 2.4 Path Smoothing (2 marks)
Status: PASS

Implemented:
- Optional smoothing removes unnecessary intermediate nodes when line-of-sight is clear.
- Toggle with enablePathSmoothing.

Where:
- Assets/Scripts/Pathfinding/Pathfinding.cs (SmoothPath)
- Assets/Scripts/Pathfinding/AStarGrid.cs (IsPathSegmentClear)

### 2.5 Dynamic Obstacles (2 marks)
Status: PASS

Implemented:
- Dynamic obstacle layer support in grid and runtime checks.
- Frog recalculates path when moving obstacles block planned nodes.

Where:
- Assets/Scripts/Pathfinding/AStarGrid.cs (dynamicObstacleMask, IsPointBlockedByDynamicObstacle)
- Assets/Scripts/Frog.cs (TryRecalculatePathForDynamicObstacles)

## 3. Demonstration Checklist (Video)

Use this exact sequence to make each feature visually evident.

1. Baseline A* path around static obstacles.
2. Turn includeDiagonalNeighbours off, click target, show orthogonal path.
3. Turn includeDiagonalNeighbours on, click same target, show diagonal path.
4. Switch heuristicType between Manhattan and Euclidean/Octile and show path differences.
5. Show terrain map colors by enabling displayTerrainGizmos.
6. Increase waterCost/mudCost and show path rerouting to lower-cost terrain.
7. Toggle enablePathSmoothing off then on to show waypoint reduction.
8. Move/animate dynamic obstacles and show automatic repath.
9. Keep displayPathGizmos enabled so route changes are clearly visible.

## 4. Inspector Setup Required

On AStarGrid object:
- includeDiagonalNeighbours: On
- heuristicType: choose one for each demo segment
- enablePathSmoothing: toggle during demo
- displayGridGizmos: On
- displayTerrainGizmos: On
- displayPathGizmos: On
- unwalkableMask: static obstacle layer
- dynamicObstacleMask: moving obstacle layer
- mudMask/waterMask/grassMask: terrain layers
- normalCost/mudCost/waterCost/grassCost: set distinct values

On Frog object:
- waypointTolerance: keep small (example 0.2)
- dynamicRepathInterval: moderate (example 0.2)

## 5. Strictness Notes

- This implementation is now checklist-oriented for the full Member 1 specification you shared.
- It is not restricted to skeleton-only minimum anymore.
- If your marker asks for strict skeleton style only, keep this version but explain why each enhancement maps directly to your rubric checklist.

## 6. Implementation Evidence Report

This section is the line-by-line change report you asked for. It ties each change to the exact file, the reason it was changed, and a small code quote so you can explain it in review or video.

### 6.1 Node.cs - terrain-aware node data

Why it changed:
- The grid nodes needed to remember which terrain they belong to and how expensive that terrain is.
- This lets A* prefer cheaper terrain instead of treating every cell the same.

Exact file:
- [Assets/Scripts/Pathfinding/Node.cs](Assets/Scripts/Pathfinding/Node.cs)

Relevant lines:
- [Terrain type enum](Assets/Scripts/Pathfinding/Node.cs#L9)
- [Movement cost field](Assets/Scripts/Pathfinding/Node.cs#L38)
- [Constructor update](Assets/Scripts/Pathfinding/Node.cs#L43)
- [Clone preserves terrain](Assets/Scripts/Pathfinding/Node.cs#L53)

Code quote:
```csharp
public enum TerrainType
{
	Normal,
	Mud,
	Water,
	Grass
}
```

```csharp
public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY, TerrainType _terrainType = TerrainType.Normal, float _movementCost = 1f)
```

What it implements:
- Terrain classification for each node.
- Movement cost storage for weighted pathfinding.

### 6.2 AStarGrid.cs - terrain, heuristics, smoothing, and gizmos

Why it changed:
- This file now creates the grid, assigns terrain, detects static and dynamic obstacles, calculates heuristics, and draws the visual debug view.
- It is the main configuration surface for the Member 1 features.

Exact file:
- [Assets/Scripts/Pathfinding/AStarGrid.cs](Assets/Scripts/Pathfinding/AStarGrid.cs)

Relevant lines:
- [Terrain and path gizmo toggles](Assets/Scripts/Pathfinding/AStarGrid.cs#L9)
- [Dynamic obstacle mask](Assets/Scripts/Pathfinding/AStarGrid.cs#L14)
- [Heuristic selection](Assets/Scripts/Pathfinding/AStarGrid.cs#L28)
- [Path smoothing toggle](Assets/Scripts/Pathfinding/AStarGrid.cs#L31)
- [8-direction toggle](Assets/Scripts/Pathfinding/AStarGrid.cs#L44)
- [Neighbour generation](Assets/Scripts/Pathfinding/AStarGrid.cs#L100)
- [Heuristic calculation](Assets/Scripts/Pathfinding/AStarGrid.cs#L131)
- [Step cost calculation](Assets/Scripts/Pathfinding/AStarGrid.cs#L149)
- [Line-of-sight test](Assets/Scripts/Pathfinding/AStarGrid.cs#L155)
- [Dynamic obstacle overlap test](Assets/Scripts/Pathfinding/AStarGrid.cs#L161)
- [Terrain and path gizmos](Assets/Scripts/Pathfinding/AStarGrid.cs#L260)

Code quote:
```csharp
public bool displayTerrainGizmos;
public bool displayPathGizmos;
public LayerMask dynamicObstacleMask;
public enum PathHeuristic
{
	Euclidean,
	Manhattan,
	Octile
}
```

```csharp
if (!includeDiagonalNeighbours && Mathf.Abs(x) + Mathf.Abs(y) == 2)
{
	continue;
}
```

```csharp
case PathHeuristic.Manhattan:
	return dx + dy;
case PathHeuristic.Octile:
	float diagonal = Mathf.Min(dx, dy);
	float straight = Mathf.Max(dx, dy) - diagonal;
	return diagonal * Mathf.Sqrt(2f) + straight;
```

What it implements:
- 8-direction neighbor support.
- Multiple heuristic choices.
- Terrain movement costs.
- Static and dynamic obstacle detection.
- Terrain and path visualization.
- Path smoothing support through line-of-sight checks.

### 6.3 Pathfinding.cs - A* algorithm and smoothing logic

Why it changed:
- This file now performs the actual A* search using the grid data.
- It is the control logic that decides which node to expand, when to stop, and how to rebuild the path.

Exact file:
- [Assets/Scripts/Pathfinding/Pathfinding.cs](Assets/Scripts/Pathfinding/Pathfinding.cs)

Relevant lines:
- [Start node setup](Assets/Scripts/Pathfinding/Pathfinding.cs#L82)
- [Open set initialization](Assets/Scripts/Pathfinding/Pathfinding.cs#L86)
- [Lowest-cost node removal](Assets/Scripts/Pathfinding/Pathfinding.cs#L94)
- [Neighbour exploration](Assets/Scripts/Pathfinding/Pathfinding.cs#L108)
- [Terrain-aware G-cost](Assets/Scripts/Pathfinding/Pathfinding.cs#L115)
- [Heuristic update](Assets/Scripts/Pathfinding/Pathfinding.cs#L128)
- [Path smoothing toggle](Assets/Scripts/Pathfinding/Pathfinding.cs#L159)
- [Path recording for gizmos](Assets/Scripts/Pathfinding/Pathfinding.cs#L164)
- [Fallback clear path reset](Assets/Scripts/Pathfinding/Pathfinding.cs#L168)
- [G-cost function](Assets/Scripts/Pathfinding/Pathfinding.cs#L207)
- [Heuristic function](Assets/Scripts/Pathfinding/Pathfinding.cs#L213)
- [Smoothing function](Assets/Scripts/Pathfinding/Pathfinding.cs#L218)

Code quote:
```csharp
openSet.Add(startNode);
Node currentNode = openSet.RemoveFirst();
```

```csharp
float newCostToNeighbour = currentNode.gCost + GCost(currentNode, node);
node.hCost = Heuristic(node, targetNode);
node.parent = currentNode;
```

```csharp
if (grid.enablePathSmoothing)
{
	waypoints = SmoothPath(waypoints);
}
```

What it implements:
- A* open-set and closed-set search.
- Goal detection.
- Weighted terrain movement cost.
- Heuristic-driven path choice.
- Optional smoothing when the path is unobstructed.
- Gizmo path recording for visual verification.

### 6.4 Frog.cs - click-to-path movement and dynamic repath

Why it changed:
- The Frog now requests a path when the user clicks and follows the returned waypoints.
- It also rechecks the remaining route if dynamic obstacles block the path.

Exact file:
- [Assets/Scripts/Frog.cs](Assets/Scripts/Frog.cs)

Relevant lines:
- [Repath interval field](Assets/Scripts/Frog.cs#L51)
- [Path request on click](Assets/Scripts/Frog.cs#L102)
- [Dynamic obstacle path check](Assets/Scripts/Frog.cs#L106)
- [Path-following movement branch](Assets/Scripts/Frog.cs#L169)
- [Waypoint movement method](Assets/Scripts/Frog.cs#L206)
- [RequestPath helper](Assets/Scripts/Frog.cs#L243)
- [Path recalculation helper](Assets/Scripts/Frog.cs#L261)
- [Dynamic repath timing](Assets/Scripts/Frog.cs#L268)
- [Re-request after block detection](Assets/Scripts/Frog.cs#L280)

Code quote:
```csharp
RequestPathTo((Vector2)_lastClickPos);
```

```csharp
if (_currentPath != null && _pathIndex < _currentPath.Length)
{
	return getVelocityAlongPath();
}
```

```csharp
if (Pathfinding.grid.IsPointBlockedByDynamicObstacle(_currentPath[i].worldPosition))
{
	Pathfinding.grid.CreateGrid();
	RequestPathTo((Vector2)_pathGoal);
}
```

What it implements:
- Mouse-click path requests.
- Waypoint-by-waypoint frog movement.
- On-demand path recalculation when moving obstacles interfere.
- Controlled timing so the path is not recomputed every frame.

### 6.5 How to describe the reason for each change

Use this sentence pattern in your explanation:

1. "I changed [file] because [problem or requirement]."
2. "This implements [feature] by [specific mechanism]."
3. "You can see it in [line reference]."

Example:
- "I changed [Pathfinding.cs](Assets/Scripts/Pathfinding/Pathfinding.cs) because the starter file only had TODOs for the A* search loop. This implements the full open-set/closed-set algorithm by removing the lowest-cost node, expanding neighbors, and reconstructing the path. You can see it at [line 86](Assets/Scripts/Pathfinding/Pathfinding.cs#L86), [line 94](Assets/Scripts/Pathfinding/Pathfinding.cs#L94), and [line 218](Assets/Scripts/Pathfinding/Pathfinding.cs#L218)."

## 7. Short Submission Summary

If you need a very short summary for your submission notes, use this:

- Node.cs now stores terrain type and movement cost.
- AStarGrid.cs now supports 8-direction neighbors, terrain colors, heuristic toggles, smoothing checks, and dynamic obstacle detection.
- Pathfinding.cs now runs the A* algorithm, applies weighted terrain costs, and optionally smooths paths.
- Frog.cs now requests paths on click and only recalculates when the path becomes blocked.

# Assignment 1: Complete A* Pathfinding Implementation Tutorial
## Year 2 Level - A to Z Guide for Complete Beginners

**Last Updated:** April 26, 2026  
**Purpose:** Learn to implement complete A* pathfinding system from scratch  
**Level:** Beginner-Friendly with Code Examples

---

## TABLE OF CONTENTS

1. [What You're Building](#what-youre-building)
2. [Starter Code Overview](#starter-code-overview)
3. [Understanding A* Algorithm](#understanding-a-algorithm)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Complete Code Reference](#complete-code-reference)
6. [Testing & Validation](#testing--validation)
7. [Troubleshooting](#troubleshooting)

---

## What You're Building

### The Goal
Transform a Frog character in a Unity game to move intelligently around obstacles using A* pathfinding. The Frog should:
- Find optimal paths around obstacles
- Respect terrain difficulty (mud is slower)
- Adapt to moving obstacles in real-time
- Show its path visually for debugging

### What You Start With (Starter Code)
- **AStarGrid.cs**: Basic grid structure with TODO comments
- **Pathfinding.cs**: Incomplete A* algorithm skeleton
- **Node.cs**: Data structure for grid nodes (working)
- **Frog.cs**: Character controller without pathfinding
- **Heap.cs**: Priority queue implementation (working)

### What You Need to Add/Change
1. Complete A* algorithm implementation
2. Terrain cost system
3. Multiple heuristic options
4. Pathfinding integration with Frog
5. Dynamic obstacle handling
6. Visualization system
7. Path smoothing

---

## Starter Code Overview

### Starting Point: AStarGrid.cs (Starter Code)

```csharp
public class AStarGrid : MonoBehaviour
{
    public bool displayGridGizmos;
    public LayerMask unwalkableMask;
    public Vector2 gridWorldSize;
    public float gridSize;          // <-- Used to create nodes
    public float overlapCircleRadius;
    public bool includeDiagonalNeighbours;

    Node[,] grid;
    float nodeDiameter;
    int gridSizeX, gridSizeY;

    public void CreateGrid()
    {
        // Creates a grid of nodes
        // Checks if each node is walkable using unwalkableMask
        // Only 4-directional movement (up, down, left, right)
    }

    public List<Node> GetNeighbours(Node node)
    {
        // Returns up to 4 adjacent nodes (no diagonals)
    }
}
```

**What's Missing:**
- ❌ No terrain types support
- ❌ No A* algorithm implementation
- ❌ No heuristic options
- ❌ No visualization
- ❌ No path smoothing

---

### Starting Point: Pathfinding.cs (Starter Code - INCOMPLETE)

```csharp
Node[] FindPath(Vector2 from, Vector2 to)
{
    // Setup nodes and validation
    Node startNode = grid.NodeFromWorldPoint(from);
    Node targetNode = grid.NodeFromWorldPoint(to);
    
    if (startNode.walkable && targetNode.walkable)
    {
        Heap<Node> openSet = new Heap<Node>(grid.MaxSize);
        HashSet<Node> closedSet = new HashSet<Node>();

        // TODO: Add start node to openSet
        // TODO: While openSet has nodes:
        //   TODO: Get lowest F-cost node
        //   TODO: If reached target, return path
        //   TODO: Explore neighbors
        //   TODO: Update costs if better path found

        // The algorithm is completely empty - just TODOs!
    }

    return waypoints;  // Always empty array!
}
```

**What's Missing:**
- ❌ Algorithm body is all TODOs
- ❌ Never adds start node
- ❌ Main loop doesn't execute
- ❌ Returns empty array

---

### Starting Point: Frog.cs (Starter Code - NO PATHFINDING)

```csharp
public class Frog : MonoBehaviour
{
    // Has steering, animation, health
    // But NO pathfinding!
    
    void Update()
    {
        if (ClickMoveAction.WasPressedThisFrame())
        {
            _lastClickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
            _flag.position = (Vector2)_lastClickPos + new Vector2(0.55f, 0.55f);
            _flagSr.enabled = true;
            // Only sets flag position, doesn't calculate path!
        }
    }

    private Vector2 decideMovement()
    {
        // Just returns zero - no movement logic!
        return Vector2.zero;
    }
}
```

**What's Missing:**
- ❌ No Pathfinder reference
- ❌ No path calculation on click
- ❌ No waypoint following logic
- ❌ No dynamic obstacle handling

---

## Understanding A* Algorithm

### What is A*?

A* is a pathfinding algorithm that finds the shortest path from point A to point B while avoiding obstacles. It works by:

1. **Keeping Track of Two Sets:**
   - **Open Set**: Nodes to explore next
   - **Closed Set**: Nodes already explored

2. **Using Two Costs:**
   - **G Cost**: Distance traveled from start to current node
   - **H Cost**: Estimated distance from current node to goal
   - **F Cost**: G + H (total estimated cost)

3. **Always Picking the Best Node:**
   - Always explores the node with lowest F cost
   - This keeps the search efficient and accurate

### Visual Example

```
Start (S) ──── Normal Grid ──── Goal (G)
         \                     /
          \    Obstacles      /
           \    (RED CELLS)   /
            \                /

Without Pathfinding:
S → runs straight into wall

With A*:
S → goes around obstacles → G (optimal path)
```

### The Three Heuristics

**Heuristic** = Estimation of distance to goal

```
3 Options:

1. EUCLIDEAN (Most Realistic)
   - Straight-line distance
   - Best for natural-looking paths
   - Slightly slower

2. MANHATTAN (Grid-Based)
   - Distance if you can only move up/down/left/right
   - Good for grid systems
   - Faster computation

3. OCTILE (Optimized for Diagonals)
   - Accounts for diagonal movement
   - Balanced performance
   - Most efficient for 2D grids

Which to use?
→ Euclidean for natural paths (default)
→ Manhattan for pure grid movement
→ Octile for balanced performance
```

---

## Step-by-Step Implementation

### STEP 1: Enhance Node.cs - Add Terrain Support

**What to Add:**
The starter Node.cs is good but needs terrain tracking.

**Changes:**

```csharp
// IN: public class Node : IHeapItem<Node>
// ADD these new fields after existing fields:

public enum TerrainType { Normal, Mud, Water, Grass }  // <-- NEW

public TerrainType terrainType;         // <-- NEW
public float movementCost;              // <-- NEW

// MODIFY: Constructor to accept terrain
// FROM:
public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY)
{
    walkable = _walkable;
    worldPosition = _worldPos;
    gridX = _gridX;
    gridY = _gridY;
}

// TO:
public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY, 
            TerrainType _terrainType = TerrainType.Normal, 
            float _movementCost = 1f)  // <-- NEW PARAMETERS
{
    walkable = _walkable;
    worldPosition = _worldPos;
    gridX = _gridX;
    gridY = _gridY;
    terrainType = _terrainType;         // <-- NEW
    movementCost = _movementCost;       // <-- NEW
}
```

**Why:**
- Nodes need to know what terrain they are on
- Movement cost allows paths to prefer easy terrain
- Mud (cost=3) is slower than normal (cost=1)

---

### STEP 2: Replace AStarGrid.cs - Complete Rewrite

**What to Replace:**
The starter AStarGrid.cs is too basic. Replace entire file with new version.

**Key Changes from Starter to New:**

| Starter Feature | New Feature | Why |
|---|---|---|
| `gridSize` | `nodeRadius` | Better for 2D representation |
| Only `unwalkableMask` | Terrain + obstacle layers | Support different terrain types |
| No heuristic system | Multiple heuristics (Euclidean, Manhattan, Octile) | Different path qualities |
| `GetNeighbours()` with 4 directions | 8-directional with `allowDiagonal` | More flexibility |
| No terrain costs | Full terrain cost system | Respect terrain difficulty |
| No visualization | Complete gizmo system | Debug support |
| Returns `Node[]` | Returns `List<Vector2>` | Easier to use waypoints |

**Complete New AStarGrid.cs:**

```csharp
using System.Collections.Generic;
using UnityEngine;

public class AStarGrid : MonoBehaviour
{
    // ============ VISUALIZATION & DEBUG ============
    [Header("Gizmo/Debug Visualization")]
    public bool showGridGizmos = true;
    public bool showTerrainGizmos = true;
    public bool showPathGizmos = true;
    [HideInInspector]
    public List<Vector2> lastPath;

    // ============ TERRAIN SYSTEM ============
    public enum TerrainType { Normal, Mud, Water, Grass }
    
    [System.Serializable]
    public struct TerrainCost
    {
        public TerrainType type;
        public float cost;
        public Color color;
    }
    
    public TerrainCost[] terrainCosts = new TerrainCost[] {
        new TerrainCost { type = TerrainType.Normal, cost = 1f, color = Color.white },
        new TerrainCost { type = TerrainType.Mud, cost = 3f, color = new Color(0.5f,0.25f,0f) },
        new TerrainCost { type = TerrainType.Water, cost = 5f, color = Color.blue },
        new TerrainCost { type = TerrainType.Grass, cost = 2f, color = Color.green }
    };

    // ============ TERRAIN DETECTION (Use Unity Layers) ============
    public LayerMask mudMask;
    public LayerMask waterMask;
    public LayerMask grassMask;
    public LayerMask obstacleMask;
    [Header("Dynamic Obstacles")]
    public LayerMask dynamicObstacleMask;

    // ============ GRID SETTINGS ============
    public Vector2 gridWorldSize = new Vector2(20f, 20f);
    public float nodeRadius = 0.5f;
    public bool allowDiagonal = true;

    // ============ HEURISTIC OPTIONS ============
    public enum HeuristicType { Euclidean, Manhattan, Octile }
    [Header("A* Heuristic")]
    public HeuristicType heuristicType = HeuristicType.Euclidean;

    // ============ INTERNAL GRID ============
    private Node[,] grid;
    private float nodeDiameter;
    private int gridSizeX, gridSizeY;
    private Vector2 worldBottomLeft;

    // ============ INITIALIZATION ============
    private void Awake()
    {
        CreateGrid();
    }

    // ============ GRID CREATION ============
    public void CreateGrid()
    {
        // Calculate grid dimensions
        nodeDiameter = nodeRadius * 2f;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
        grid = new Node[gridSizeX, gridSizeY];
        
        // Calculate bottom-left corner of grid
        worldBottomLeft = (Vector2)transform.position - 
                          Vector2.right * (gridWorldSize.x / 2f) - 
                          Vector2.up * (gridWorldSize.y / 2f);

        // Create each node
        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                // Calculate world position of this node
                Vector2 worldPoint = worldBottomLeft + 
                                    new Vector2(x * nodeDiameter + nodeRadius, 
                                              y * nodeDiameter + nodeRadius);

                // Check if walkable (no obstacles)
                bool walkable = Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, obstacleMask) == null
                                 && Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, dynamicObstacleMask) == null;

                // Detect terrain type
                TerrainType terrain = TerrainType.Normal;
                if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, mudMask)) 
                    terrain = TerrainType.Mud;
                else if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, waterMask)) 
                    terrain = TerrainType.Water;
                else if (Physics2D.OverlapCircle(worldPoint, nodeRadius * 0.9f, grassMask)) 
                    terrain = TerrainType.Grass;

                // Get movement cost for this terrain
                float moveCost = 1f;
                foreach (var tc in terrainCosts)
                {
                    if (tc.type == terrain) { moveCost = tc.cost; break; }
                }

                // Create the node
                grid[x, y] = new Node(walkable, worldPoint, x, y, terrain, moveCost);
            }
        }
    }

    // ============ MAIN PATHFINDING METHOD ============
    public List<Vector2> FindPath(Vector2 startWorldPos, Vector2 targetWorldPos, 
                                   HeuristicType? heuristicOverride = null, 
                                   bool smoothPath = true, 
                                   bool recordForGizmos = false)
    {
        if (grid == null) CreateGrid();

        // Convert world positions to grid nodes
        Node startNode = NodeFromWorldPoint(startWorldPos);
        Node targetNode = NodeFromWorldPoint(targetWorldPos);

        if (startNode == null || targetNode == null)
            return null;

        // Use override or default heuristic
        HeuristicType heuristic = heuristicOverride ?? heuristicType;

        // ============ A* ALGORITHM STARTS HERE ============
        List<Node> openSet = new List<Node>();
        HashSet<Node> closedSet = new HashSet<Node>();
        
        // Initialize start node
        startNode.gCost = 0;
        startNode.hCost = GetHeuristic(startNode, targetNode, heuristic);
        openSet.Add(startNode);

        // Main A* loop
        while (openSet.Count > 0)
        {
            // STEP 1: Find node with lowest F cost
            Node currentNode = openSet[0];
            for (int i = 1; i < openSet.Count; i++)
            {
                // Better F cost, or same F but better H cost (tiebreaker)
                if (openSet[i].fCost < currentNode.fCost || 
                    (Mathf.Approximately(openSet[i].fCost, currentNode.fCost) && 
                     openSet[i].hCost < currentNode.hCost))
                {
                    currentNode = openSet[i];
                }
            }

            // STEP 2: Move from open to closed
            openSet.Remove(currentNode);
            closedSet.Add(currentNode);

            // STEP 3: SUCCESS! - Reached goal
            if (currentNode == targetNode)
            {
                var rawPath = RetracePath(startNode, targetNode);
                var result = smoothPath ? SmoothPath(rawPath) : rawPath;
                if (recordForGizmos)
                    lastPath = result;
                return result;
            }

            // STEP 4: Explore neighbors
            foreach (Node neighbour in GetNeighbours(currentNode))
            {
                // Skip if not walkable or already explored
                if (!neighbour.walkable || closedSet.Contains(neighbour))
                    continue;

                // Calculate distance cost including terrain
                float tentativeG = currentNode.gCost + 
                                  Vector2.Distance(currentNode.worldPosition, 
                                                  neighbour.worldPosition) * 
                                  neighbour.movementCost;  // <-- TERRAIN COST APPLIED HERE

                // If new path is better, update neighbor
                if (tentativeG < neighbour.gCost || !openSet.Contains(neighbour))
                {
                    neighbour.gCost = tentativeG;
                    neighbour.hCost = GetHeuristic(neighbour, targetNode, heuristic);
                    neighbour.parent = currentNode;

                    if (!openSet.Contains(neighbour))
                        openSet.Add(neighbour);
                }
            }
        }

        // No path found
        return null;
    }

    // ============ RECONSTRUCT PATH ============
    private List<Vector2> RetracePath(Node startNode, Node endNode)
    {
        List<Vector2> path = new List<Vector2>();
        Node current = endNode;
        
        // Follow parent links backwards
        while (current != startNode)
        {
            path.Add(current.worldPosition);
            current = current.parent;
            if (current == null) break;
        }
        
        // Reverse to get start → goal order
        path.Reverse();
        return path;
    }

    // ============ PATH SMOOTHING ============
    private List<Vector2> SmoothPath(List<Vector2> path)
    {
        if (path == null || path.Count < 3) return path;
        
        List<Vector2> smoothed = new List<Vector2>();
        int i = 0;
        
        while (i < path.Count)
        {
            smoothed.Add(path[i]);
            int next = i + 1;
            
            // Try to skip waypoints if line-of-sight is clear
            for (int j = path.Count - 1; j > next; j--)
            {
                if (HasLineOfSight(path[i], path[j]))
                {
                    next = j;  // Skip intermediate points
                    break;
                }
            }
            i = next;
        }
        
        // Ensure final waypoint is included
        if (smoothed[smoothed.Count - 1] != path[path.Count - 1])
            smoothed.Add(path[path.Count - 1]);
        
        return smoothed;
    }

    private bool HasLineOfSight(Vector2 a, Vector2 b)
    {
        return !Physics2D.Linecast(a, b, obstacleMask);
    }

    // ============ HEURISTIC CALCULATIONS ============
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

    // ============ COORDINATE CONVERSION ============
    public Node NodeFromWorldPoint(Vector2 worldPoint)
    {
        if (grid == null) return null;
        
        float percentX = (worldPoint.x - worldBottomLeft.x) / (gridWorldSize.x);
        float percentY = (worldPoint.y - worldBottomLeft.y) / (gridWorldSize.y);
        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.Clamp(Mathf.RoundToInt((gridSizeX - 1) * percentX), 0, gridSizeX - 1);
        int y = Mathf.Clamp(Mathf.RoundToInt((gridSizeY - 1) * percentY), 0, gridSizeY - 1);
        return grid[x, y];
    }

    public Node ClosestWalkableNode(Node node)
    {
        return node;  // Stub for compatibility
    }

    public int MaxSize
    {
        get { return (grid != null) ? grid.GetLength(0) * grid.GetLength(1) : 0; }
    }

    // ============ NEIGHBOR FINDING ============
    private List<Node> GetNeighbours(Node node)
    {
        List<Node> neighbours = new List<Node>();

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0) continue;
                if (!allowDiagonal && Mathf.Abs(x) + Mathf.Abs(y) == 2) continue;

                int checkX = node.gridX + x;
                int checkY = node.gridY + y;

                if (checkX >= 0 && checkX < gridSizeX && checkY >= 0 && checkY < gridSizeY)
                {
                    neighbours.Add(grid[checkX, checkY]);
                }
            }
        }

        return neighbours;
    }

    // ============ VISUALIZATION (Gizmos) ============
    private void OnDrawGizmos()
    {
        // Draw grid wireframe
        if (showGridGizmos)
        {
            Gizmos.color = Color.gray;
            Gizmos.DrawWireCube(transform.position, 
                               new Vector3(gridWorldSize.x, gridWorldSize.y, 1f));
        }

        if (grid != null)
        {
            // Draw terrain cells
            if (showTerrainGizmos)
            {
                foreach (Node n in grid)
                {
                    if (!n.walkable)
                        Gizmos.color = Color.red;  // Obstacles
                    else
                        Gizmos.color = GetTerrainColor(n.terrainType);  // Terrain
                    
                    Gizmos.DrawCube(n.worldPosition, 
                                   Vector3.one * (nodeRadius * 1.5f));
                }
            }

            // Draw computed path
            if (showPathGizmos && lastPath != null && lastPath.Count > 1)
            {
                Gizmos.color = Color.yellow;
                for (int i = 0; i < lastPath.Count - 1; i++)
                {
                    Gizmos.DrawLine(lastPath[i], lastPath[i + 1]);
                }
                Gizmos.DrawSphere(lastPath[lastPath.Count - 1], nodeRadius * 0.7f);
            }
        }
    }

    private Color GetTerrainColor(TerrainType type)
    {
        foreach (var tc in terrainCosts)
        {
            if (tc.type == type) return tc.color;
        }
        return Color.white;
    }

    // ============ NODE CLASS (EMBEDDED) ============
    public class Node : IHeapItem<Node>
    {
        public TerrainType terrainType;
        public float movementCost;
        public bool walkable;
        public Vector2 worldPosition;
        public int gridX;
        public int gridY;
        public float gCost = float.MaxValue;
        public float hCost = 0f;
        public Node parent = null;
        public float fCost { get { return gCost + hCost; } }
        
        private int heapIndex;
        
        public int HeapIndex
        {
            get { return heapIndex; }
            set { heapIndex = value; }
        }

        public int CompareTo(Node other)
        {
            int compare = fCost.CompareTo(other.fCost);
            if (compare == 0)
            {
                compare = hCost.CompareTo(other.hCost);
            }
            return -compare;
        }

        public Node(bool walkable, Vector2 worldPos, int x, int y, 
                   TerrainType terrainType = TerrainType.Normal, 
                   float movementCost = 1f)
        {
            this.walkable = walkable;
            this.worldPosition = worldPos;
            this.gridX = x;
            this.gridY = y;
            this.terrainType = terrainType;
            this.movementCost = movementCost;
        }
    }
}
```

**Why This Works:**
- Complete A* implementation in main loop
- Terrain costs multiply movement distance
- Multiple heuristics allow path variation
- Visualization helps debug
- Path smoothing removes unnecessary waypoints

---

### STEP 3: Enhance Frog.cs - Add Pathfinding Integration

**Changes to Frog.cs:**

```csharp
// ADD these new fields after existing fields:
public AStarGrid Pathfinder;           // <-- NEW
private List<Vector2> _currentPath;    // <-- NEW
private int _pathIndex = 0;            // <-- NEW
public float waypointTolerance = 0.2f; // <-- NEW

// MODIFY: Start() method - ADD these lines at the end:
if (Pathfinder == null)
    Pathfinder = Object.FindFirstObjectByType<AStarGrid>();
_currentPath = null;
_pathIndex = 0;

// MODIFY: Update() method - REPLACE entire section:
// FROM:
void Update()
{
    if (ClickMoveAction.WasPressedThisFrame())
    {
        _lastClickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
        _arriveRadius = Mathf.Clamp(...);
        _flag.position = (Vector2)_lastClickPos + new Vector2(0.55f, 0.55f);
        _flagSr.enabled = true;
    }
    else
    {
        if (closestFly != null)
            Debug.DrawLine(...);
        if (closestSnake != null)
            Debug.DrawLine(...);
    }
}

// TO:
void Update()
{
    if (ClickMoveAction.WasPressedThisFrame())
    {
        Vector2 clickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
        _arriveRadius = Mathf.Clamp(ArrivePct * (clickPos - (Vector2)transform.position).magnitude, 
                                   MinArriveRadius, MaxArriveRadius);

        _flag.position = clickPos + new Vector2(0.55f, 0.55f);
        _flagSr.enabled = true;

        // NEW: Request pathfinding!
        if (Pathfinder != null)
        {
            _currentPath = Pathfinder.FindPath(transform.position, clickPos, 
                                              Pathfinder.heuristicType, false, true);
            _pathIndex = 0;
            if (_currentPath == null || _currentPath.Count == 0)
            {
                _lastClickPos = clickPos;
            }
            else
            {
                _lastClickPos = null;
            }
        }
        else
        {
            _lastClickPos = clickPos;
        }
    }
    else
    {
        // NEW: Check if path is blocked by obstacles
        if (_currentPath != null && _currentPath.Count > 0 && Pathfinder != null)
        {
            foreach (var point in _currentPath)
            {
                if (Physics2D.OverlapCircle(point, Pathfinder.nodeRadius * 0.9f, 
                                           Pathfinder.dynamicObstacleMask))
                {
                    Pathfinder.CreateGrid();
                    _currentPath = Pathfinder.FindPath(transform.position, 
                                                     _currentPath[_currentPath.Count - 1],
                                                     Pathfinder.heuristicType, false, true);
                    _pathIndex = 0;
                    break;
                }
            }
        }
        if (closestFly != null)
            Debug.DrawLine(transform.position, closestFly.transform.position, Color.black);
        if (closestSnake != null)
            Debug.DrawLine(transform.position, closestSnake.transform.position, Color.red);
    }
}

// MODIFY: decideMovement() method - REPLACE body:
// FROM:
private Vector2 decideMovement()
{
    // ... (existing code)
    return Vector2.zero;
}

// TO:
private Vector2 decideMovement()
{
    // PRIORITY 1: Follow computed path
    if (_currentPath != null && _pathIndex < _currentPath.Count)
    {
        return getVelocityAlongPath();
    }

    // PRIORITY 2: Go to fallback click position
    if (_lastClickPos != null)
    {
        return getVelocityTowardsFlag();
    }

    return Vector2.zero;
}

// ADD these new methods:
private Vector2 getVelocityAlongPath()
{
    Vector2 desiredVel = Vector2.zero;
    if (_currentPath == null || _pathIndex >= _currentPath.Count)
        return desiredVel;

    Vector2 waypoint = _currentPath[_pathIndex];
    
    // Check if reached current waypoint
    if (((Vector2)transform.position - waypoint).magnitude > 
        Mathf.Max(Constants.TARGET_REACHED_TOLERANCE, waypointTolerance))
    {
        // Move toward waypoint
        desiredVel = Steering.ArriveDirect(gameObject.transform.position, waypoint, 
                                          _arriveRadius, MaxSpeed);
    }
    else
    {
        // Waypoint reached, advance to next
        _pathIndex++;
        if (_pathIndex >= _currentPath.Count)
        {
            // Entire path complete
            _currentPath = null;
            _pathIndex = 0;
            if (HideFlagOnceReached)
                _flagSr.enabled = false;
        }
    }

    return desiredVel;
}

private Vector2 getVelocityTowardsFlag()
{
    Vector2 desiredVel = Vector2.zero;
    if (_lastClickPos != null)
    {
        if (((Vector2)_lastClickPos - (Vector2)gameObject.transform.position).magnitude > 
            Constants.TARGET_REACHED_TOLERANCE)
        {
            desiredVel = Steering.ArriveDirect(gameObject.transform.position, 
                                              (Vector2)_lastClickPos, _arriveRadius, MaxSpeed);
        }
        else
        {
            _lastClickPos = null;
            if (HideFlagOnceReached)
                _flagSr.enabled = false;
        }
    }
    return desiredVel;
}
```

**Why These Changes:**
- On click: request path from Pathfinder
- Every frame: check if path is blocked, recalculate if needed
- Follow waypoints in order using steering
- Dynamic obstacle detection keeps Frog adaptive

---

## Complete Code Reference

### All Files Needed

**1. Node.cs** (Minimal changes from starter)
- Add `terrainType` field
- Add `movementCost` field
- Update constructor to accept these parameters

**2. AStarGrid.cs** (Complete replacement)
- Full A* algorithm implementation
- Terrain cost system
- Multiple heuristics
- Visualization system

**3. Frog.cs** (Enhanced with pathfinding)
- Add Pathfinder reference
- Add path following logic
- Dynamic obstacle detection

**4. Pathfinding.cs** (Delete or leave unused)
- No longer needed - AStarGrid.cs replaces it

**5. Heap.cs** (No changes)
- Already works perfectly

---

## Testing & Validation

### Setup Checklist

```
□ Create AStarGrid GameObject in scene
□ Attach AStarGrid.cs script
□ Create Layers: Mud, Water, Grass, Obstacle
□ Assign terrain GameObjects to correct layers
□ Set layer masks in AStarGrid Inspector:
  □ Mud Mask → Mud layer
  □ Water Mask → Water layer
  □ Grass Mask → Grass layer
  □ Obstacle Mask → Obstacle layer
  □ Dynamic Obstacle Mask → Obstacle layer (or another layer)
□ Set Frog's Pathfinder reference to AStarGrid
□ Adjust grid size and node radius for your level
```

### Test Cases

**Test 1: Basic Pathfinding**
1. Enter Play mode
2. Right-click on screen
3. ✅ Frog computes path (yellow line in Scene view)
4. ✅ Frog moves along path
5. ✅ Frog stops at target

**Test 2: Obstacle Avoidance**
1. Right-click near obstacle
2. ✅ Yellow path goes around obstacle (not through it)
3. ✅ Frog follows around path

**Test 3: Terrain Preference**
1. Place different terrain types in scene
2. Right-click creating path through mud and grass
3. ✅ Path should prefer grass (lower cost) when available
4. ✅ Grid cells show correct colors

**Test 4: Heuristic Switching**
1. In Inspector, change HeuristicType
2. Set new target
3. ✅ Path changes shape based on heuristic
4. ✅ Different heuristics show different paths

**Test 5: Dynamic Obstacles**
1. Move an obstacle into Frog's path during movement
2. ✅ Path recalculates automatically
3. ✅ Frog adapts to new path

### Verification in Scene View

When you play:
- Gray wireframe cube = Grid boundary (if showGridGizmos enabled)
- Colored squares = Terrain cells (if showTerrainGizmos enabled)
  - White = Normal
  - Brown = Mud
  - Blue = Water
  - Green = Grass
  - Red = Obstacles
- Yellow line = Computed path (if showPathGizmos enabled)

---

## Troubleshooting

### Problem: Frog Gets Stuck on Obstacles

**Cause:** Obstacle GameObjects not on correct layer

**Solution:**
1. Select obstacle GameObject
2. In Inspector, set Layer to "Obstacle"
3. Click "Yes, change children" if it has children
4. Verify obstacle cells are RED in Scene view

---

### Problem: Path Goes Through Obstacles

**Cause:** Obstacle layer not properly assigned to layer mask

**Solution:**
1. Select AStarGrid GameObject
2. In Inspector, find "Obstacle Mask"
3. Click dropdown and select "Obstacle" layer
4. Verify grid was recreated (usually automatic)

---

### Problem: Grid Not Visible

**Cause:** Gizmos disabled or grid visualization off

**Solution:**
1. In Scene view top-right, ensure "Gizmos" button is ON
2. Select AStarGrid GameObject
3. In Inspector, enable `showGridGizmos` checkbox

---

### Problem: Frog Doesn't Move at All

**Cause:** Pathfinder reference not set in Frog

**Solution:**
1. Select Frog GameObject
2. In Inspector, find "Pathfinder" field
3. Drag AStarGrid GameObject into field
4. Or leave blank and let auto-detect in Start()

---

### Problem: Path Looks Jagged/Unsmooth

**Cause:** Path smoothing disabled

**Solution:**
- This is intentional for visualization clarity
- To enable smoothing, in Frog.cs FindPath call:
  ```csharp
  _currentPath = Pathfinder.FindPath(..., true, ...);  // Changed to true
  ```

---

## Summary of Changes

### From Starter Code to Implementation

| Aspect | Starter | Implementation | Why |
|--------|---------|---------------|----|
| A* Algorithm | 100% TODO | 100% Complete | Need working algorithm |
| Terrain Support | No | Full system | Add gameplay strategy |
| Heuristics | None | 3 options | Performance tuning |
| Visualization | Basic | Full gizmo system | Debug support |
| Pathfinding Integration | No | Complete | Core requirement |
| Dynamic Obstacles | No | Yes | Realistic adaptation |
| Path Smoothing | N/A | Yes | Natural movement |

### Key Concepts to Remember

1. **A* Uses Two Costs:**
   - G Cost = how far we've traveled
   - H Cost = estimated distance to goal
   - Always picks node with lowest F = G + H

2. **Terrain Costs Multiply:**
   - Normal (cost 1) = base movement
   - Grass (cost 2) = 2x slower
   - Mud (cost 3) = 3x slower
   - Water (cost 5) = very slow

3. **Three Heuristics:**
   - Euclidean = realistic (default)
   - Manhattan = grid-based
   - Octile = optimized for diagonals

4. **Dynamic Obstacles:**
   - Check each waypoint for collisions
   - If blocked, recreate grid and recalculate
   - Allows real-time adaptation

5. **Visualization Helps:**
   - Grid shows what AI "sees"
   - Colors show terrain types
   - Yellow line shows computed path

---

## How to Explain to Your Tutor

**Opening:**
"I implemented A* pathfinding for the Frog character. The starter code provided an incomplete skeleton, so I created a complete algorithm that finds optimal paths while respecting terrain difficulty."

**Key Points:**
1. "A* is efficient because it uses two costs - distance traveled and estimated distance to goal."
2. "Terrain costs make paths realistic - the Frog avoids mud when possible."
3. "Multiple heuristics show different path qualities and performance tradeoffs."
4. "Dynamic obstacles are detected and paths recalculate automatically."
5. "Visualization in Scene view helps verify the system works correctly."

**Show Proof:**
1. Play the scene
2. Click to set target
3. Point out:
   - Yellow path appears
   - Frog follows path
   - Path avoids obstacles
   - Grid shows terrain colors
4. Change heuristic - path changes
5. Move obstacle - path recalculates

---

**Document Version:** 2.0 (Complete Tutorial)  
**For:** COSC2527/COSC3144 - Assignment 1  
**Last Updated:** April 26, 2026

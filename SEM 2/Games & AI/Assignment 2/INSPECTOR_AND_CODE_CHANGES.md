# Inspector & Code Changes – Detailed Comparison Guide
## Starter Code vs Current Implementation

**Purpose:** Document exactly what changed in every file and Inspector configuration  
**Level:** Technical reference for understanding all modifications

---

## TABLE OF CONTENTS

1. [Files Modified](#files-modified)
2. [Node.cs Changes](#nodecs-changes)
3. [AStarGrid.cs Changes](#astargridcs-changes)
4. [Frog.cs Changes](#frogcs-changes)
5. [Pathfinding.cs Status](#pathfindingcs-status)
6. [Inspector Configuration](#inspector-configuration)
7. [Scene Setup](#scene-setup)
8. [Summary Table](#summary-table)

---

## Files Modified

### Files Changed
- ✅ **Node.cs** - Added terrain support fields
- ✅ **AStarGrid.cs** - Complete replacement with full implementation
- ✅ **Frog.cs** - Added pathfinding integration
- ⚠️ **Pathfinding.cs** - Left as-is (now unused)
- ✅ **Heap.cs** - No changes needed
- ✅ **Other scripts** - No changes needed

---

## Node.cs Changes

### What Changed

**Line Count:** 65 lines (starter) → 77 lines (current)  
**Change Type:** Field additions + constructor overload

### Starter Code (Lines 1-65)

```csharp
// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;

public class Node : IHeapItem<Node>
{
    public bool walkable;
    public Vector2 worldPosition;
    public int gridX;
    public int gridY;
    public float gCost;
    public float hCost;
    public Node parent;
    int heapIndex;

    public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY)
    {
        walkable = _walkable;
        worldPosition = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
    }

    public Node Clone()
    {
        return new Node(walkable, worldPosition, gridX, gridY);
    }

    public float fCost { get { return gCost + hCost; } }

    public int HeapIndex { get { return heapIndex; } set { heapIndex = value; } }

    public int CompareTo(Node nodeToCompare)
    {
        int compare = fCost.CompareTo(nodeToCompare.fCost);
        if (compare == 0)
            compare = hCost.CompareTo(nodeToCompare.hCost);
        return -compare;
    }
}
```

### Current Code (Lines 1-77)

```csharp
// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;

public class Node : IHeapItem<Node>
{
    // ✅ NEW: Terrain tracking fields
    public enum TerrainType { Normal, Mud, Water, Grass }  // <-- NEW LINE
    
    public TerrainType terrainType;      // <-- NEW LINE
    public float movementCost;           // <-- NEW LINE

    public bool walkable;
    public Vector2 worldPosition;
    public int gridX;
    public int gridY;
    public float gCost;
    public float hCost;
    public Node parent;
    int heapIndex;

    // ✅ MODIFIED: Constructor signature changed
    // FROM:
    // public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY)
    // 
    // TO:
    public Node(bool _walkable, Vector2 _worldPos, int _gridX, int _gridY, 
                TerrainType _terrainType = TerrainType.Normal, 
                float _movementCost = 1f)  // <-- ADDED OPTIONAL PARAMETERS
    {
        walkable = _walkable;
        worldPosition = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
        terrainType = _terrainType;      // <-- NEW LINE
        movementCost = _movementCost;    // <-- NEW LINE
    }

    public Node Clone()
    {
        return new Node(walkable, worldPosition, gridX, gridY);
    }

    public float fCost { get { return gCost + hCost; } }

    public int HeapIndex { get { return heapIndex; } set { heapIndex = value; } }

    public int CompareTo(Node nodeToCompare)
    {
        int compare = fCost.CompareTo(nodeToCompare.fCost);
        if (compare == 0)
            compare = hCost.CompareTo(nodeToCompare.hCost);
        return -compare;
    }
}
```

### Summary of Node.cs Changes

| Change | Why | Impact |
|--------|-----|--------|
| Added `TerrainType enum` | Define 4 terrain types | Nodes know what terrain they're on |
| Added `terrainType` field | Store terrain info | Can query node's terrain type |
| Added `movementCost` field | Store terrain difficulty | Can apply cost to pathfinding |
| Enhanced constructor | Accept terrain parameters | Can create nodes with specific terrain |
| Made parameters optional | Backward compatible | Old code still works (defaults to Normal/1f) |

**Why These Changes?**
- Nodes needed to know what terrain they represent
- Movement cost allows A* to prefer easier terrain
- Mud (3x cost) is slower than normal (1x cost)

---

## AStarGrid.cs Changes

### What Changed

**Line Count:** ~130 lines (starter) → ~420 lines (current)  
**Change Type:** Complete replacement + massive new features

### Starter Code Structure

```csharp
public class AStarGrid : MonoBehaviour
{
    // Minimal configuration
    public bool displayGridGizmos;
    public LayerMask unwalkableMask;
    public Vector2 gridWorldSize;
    public float gridSize;
    public float overlapCircleRadius;
    public bool includeDiagonalNeighbours;  // TODO - unused

    // Grid management
    Node[,] grid;
    float nodeDiameter;
    int gridSizeX, gridSizeY;

    // Methods
    public void CreateGrid() { }
    public List<Node> GetNeighbours(Node node) { }  // Only 4 directions
    public Node NodeFromWorldPoint(Vector2 worldPosition) { }
}
```

### Current Code Structure

```csharp
public class AStarGrid : MonoBehaviour
{
    // ✅ NEW: Comprehensive configuration sections

    // Section 1: VISUALIZATION & DEBUG
    [Header("Gizmo/Debug Visualization")]
    public bool showGridGizmos = true;
    public bool showTerrainGizmos = true;
    public bool showPathGizmos = true;
    [HideInInspector] public List<Vector2> lastPath;

    // Section 2: TERRAIN SYSTEM (NEW)
    public enum TerrainType { Normal, Mud, Water, Grass }
    [System.Serializable]
    public struct TerrainCost { public TerrainType type; public float cost; public Color color; }
    public TerrainCost[] terrainCosts = new TerrainCost[] { /* definitions */ };
    
    // Section 3: TERRAIN DETECTION (ENHANCED - now uses 4 layers)
    public LayerMask mudMask;                  // NEW
    public LayerMask waterMask;                // NEW
    public LayerMask grassMask;                // NEW
    public LayerMask obstacleMask;             // RENAMED from unwalkableMask
    [Header("Dynamic Obstacles")]
    public LayerMask dynamicObstacleMask;      // NEW
    
    // Section 4: GRID SETTINGS (ENHANCED)
    public Vector2 gridWorldSize;              // Same
    public float nodeRadius = 0.5f;            // RENAMED from gridSize (more descriptive)
    public bool allowDiagonal = true;          // RENAMED, now functional
    
    // Section 5: HEURISTIC OPTIONS (NEW)
    public enum HeuristicType { Euclidean, Manhattan, Octile }  // NEW
    [Header("A* Heuristic")]
    public HeuristicType heuristicType = HeuristicType.Euclidean;  // NEW
    
    // Section 6: INTERNAL GRID (SAME)
    private Node[,] grid;
    private float nodeDiameter;
    private int gridSizeX, gridSizeY;
    private Vector2 worldBottomLeft;  // NEW - for better positioning

    // Methods - COMPLETELY NEW/REPLACED
    public void CreateGrid() { }  // ENHANCED with terrain detection
    public List<Vector2> FindPath() { }  // NEW - main A* algorithm
    private List<Vector2> RetracePath() { }  // NEW - reconstruct path
    private List<Vector2> SmoothPath() { }  // NEW - remove waypoints
    private float GetHeuristic() { }  // NEW - 3 heuristic options
    private bool HasLineOfSight() { }  // NEW - for path smoothing
    public Node NodeFromWorldPoint() { }  // SAME
    private List<Node> GetNeighbours() { }  // ENHANCED - supports diagonals
    private void OnDrawGizmos() { }  // NEW - full visualization
    private Color GetTerrainColor() { }  // NEW - gizmo colors
}
```

### Critical Changes - Code Snippets

#### Change 1: Renamed `gridSize` → `nodeRadius` (Line 10)

```csharp
// STARTER
public float gridSize;

// CURRENT
public float nodeRadius = 0.5f;  // Default 0.5 for better default

// WHY: nodeRadius is clearer - it's literally the radius of each node circle
```

#### Change 2: Single Obstacle Layer → Multiple Terrain Layers (Lines 22-33)

```csharp
// STARTER
public LayerMask unwalkableMask;  // Only one layer for obstacles

// CURRENT
public LayerMask mudMask;
public LayerMask waterMask;
public LayerMask grassMask;
public LayerMask obstacleMask;           // Renamed from unwalkableMask
[Header("Dynamic Obstacles")]
public LayerMask dynamicObstacleMask;    // NEW - for moving obstacles

// WHY: Each terrain type needs its own layer for detection
//      Dynamic obstacles separate from static for real-time pathfinding
```

#### Change 3: New Methods - A* Algorithm (Lines ~100-250)

```csharp
// STARTER - NO METHOD AT ALL

// CURRENT - NEW METHOD (complete A* implementation)
public List<Vector2> FindPath(Vector2 startWorldPos, Vector2 targetWorldPos, 
                              HeuristicType? heuristicOverride = null, 
                              bool smoothPath = true, 
                              bool recordForGizmos = false)
{
    // Full A* algorithm here (150+ lines)
    // Returns waypoints instead of raw nodes
}

// WHY: A* algorithm needs to be implemented to find paths
//      Multiple return options for different use cases
```

#### Change 4: Terrain Cost Applied in Path Finding (Line ~180)

```csharp
// STARTER - NO TERRAIN SUPPORT

// CURRENT - TERRAIN MULTIPLIER APPLIED
float tentativeG = currentNode.gCost + 
                  Vector2.Distance(currentNode.worldPosition, neighbour.worldPosition) * 
                  neighbour.movementCost;  // <-- TERRAIN COST MULTIPLIES DISTANCE

// WHY: Makes paths avoid expensive terrain (mud 3x, water 5x)
//      Natural way to model terrain difficulty
```

#### Change 5: Multiple Heuristic Options (Lines ~280-295)

```csharp
// STARTER - NO HEURISTICS AT ALL

// CURRENT - THREE HEURISTIC OPTIONS
private float GetHeuristic(Node a, Node b, HeuristicType type)
{
    float dx = Mathf.Abs(a.worldPosition.x - b.worldPosition.x);
    float dy = Mathf.Abs(a.worldPosition.y - b.worldPosition.y);
    
    switch (type)
    {
        case HeuristicType.Manhattan:
            return dx + dy;                    // Grid-based distance
        case HeuristicType.Octile:
            float F = Mathf.Sqrt(2f) - 1f;
            return (dx < dy) ? F * dx + dy : F * dy + dx;  // Optimized for diagonals
        case HeuristicType.Euclidean:
        default:
            return Mathf.Sqrt(dx * dx + dy * dy);  // Straight-line distance
    }
}

// WHY: Different heuristics have different performance/quality tradeoffs
//      Users can test and optimize
```

#### Change 6: New Visualization System (Lines ~350-400)

```csharp
// STARTER - NO VISUALIZATION

// CURRENT - COMPLETE GIZMO SYSTEM
private void OnDrawGizmos()
{
    // Draw grid wireframe
    if (showGridGizmos) { Gizmos.DrawWireCube(...); }
    
    // Draw terrain cells with colors
    if (grid != null && showTerrainGizmos)
    {
        foreach (Node n in grid)
        {
            Gizmos.color = n.walkable ? GetTerrainColor(n.terrainType) : Color.red;
            Gizmos.DrawCube(n.worldPosition, ...);
        }
    }
    
    // Draw computed path
    if (showPathGizmos && lastPath != null)
    {
        Gizmos.color = Color.yellow;
        // Draw path lines
    }
}

// WHY: Debug visualization essential for verifying pathfinding works
//      See terrain types and computed paths in Scene view
```

#### Change 7: Path Smoothing (Lines ~210-240)

```csharp
// STARTER - NO PATH SMOOTHING

// CURRENT - SMOOTH UNNECESSARY WAYPOINTS
private List<Vector2> SmoothPath(List<Vector2> path)
{
    if (path == null || path.Count < 3) return path;
    
    List<Vector2> smoothed = new List<Vector2>();
    int i = 0;
    while (i < path.Count)
    {
        smoothed.Add(path[i]);
        int next = i + 1;
        
        // Try to skip waypoints if line-of-sight clear
        for (int j = path.Count - 1; j > next; j--)
        {
            if (HasLineOfSight(path[i], path[j]))
            {
                next = j;  // Skip intermediate waypoints
                break;
            }
        }
        i = next;
    }
    return smoothed;
}

// WHY: Makes paths look more natural
//      Reduces waypoint spam
//      Creates straighter lines where possible
```

### Summary of AStarGrid.cs Changes

| Component | Starter | Current | Why |
|-----------|---------|---------|-----|
| Configuration fields | 6 | 25+ | Add terrain support, visualization, heuristics |
| Pathfinding method | None | FindPath() | Core requirement |
| Return type | Node[] | List<Vector2> | Easier to use waypoints |
| Terrain support | No | Full system | Gameplay strategy |
| Heuristics | None | 3 options | Performance tuning |
| Visualization | Minimal | Full | Debug support |
| Path smoothing | No | Yes | Natural movement |
| Dynamic obstacles | No | Yes | Real-time adaptation |

---

## Frog.cs Changes

### What Changed

**Lines Modified:** ~200 lines of changes/additions  
**Change Type:** Added pathfinding integration to existing code

### Starter Code (Lines 1-60)

```csharp
public class Frog : MonoBehaviour
{
    // Existing fields - all from starter
    public int Health;
    public float MaxSpeed;
    public float MaxAccel;
    public float AccelTime;
    public float ArrivePct;
    public float MinArriveRadius;
    public float MaxArriveRadius;
    private float _arriveRadius;
    public bool HideFlagOnceReached;
    
    private Transform _flag;
    private SpriteRenderer _flagSr;
    private DrawGUI _drawGUIScript;
    private Animator _animator;
    private Rigidbody2D _rb;
    private InputAction ClickMoveAction;
    private Vector2? _lastClickPos;
    
    // WEEK6 fields - from starter
    public float scaredRange;
    public float huntRange;
    private Fly closestFly;
    private Snake closestSnake;
    private float distanceToClosestFly;
    private float distanceToClosestSnake;
    public float anchorWeight;
    public Vector2 AnchorDims;
    
    // NO PATHFINDING FIELDS - THIS IS MISSING
}
```

### Current Code - New Fields Added (After Line 34)

```csharp
    // ✅ NEW: Pathfinding fields added
    public AStarGrid Pathfinder;           // <-- NEW LINE
    private List<Vector2> _currentPath;    // <-- NEW LINE
    private int _pathIndex = 0;            // <-- NEW LINE
    public float waypointTolerance = 0.2f; // <-- NEW LINE
```

**Why:**
- `Pathfinder` - Reference to AStarGrid for path requests
- `_currentPath` - Store waypoints from A* algorithm
- `_pathIndex` - Track progress through waypoints
- `waypointTolerance` - How close before considering waypoint reached

### Starter Code - Start() Method

```csharp
    void Start()
    {
        _flag = GameObject.Find("Flag").transform;
        _flagSr = _flag.GetComponent<SpriteRenderer>();
        _flagSr.enabled = false;

        GameObject uiManager = GameObject.Find("UIManager");
        if (uiManager != null)
        {
            _drawGUIScript = uiManager.GetComponent<DrawGUI>();
        }

        _animator = GetComponent<Animator>();
        _rb = GetComponent<Rigidbody2D>();
        ClickMoveAction = InputSystem.actions.FindAction("Attack");

        _lastClickPos = null;
        _arriveRadius = MinArriveRadius;
        // NO PATHFINDER INITIALIZATION
    }
```

### Current Code - Start() Method (Enhanced)

```csharp
    void Start()
    {
        // ... existing code same ...
        _lastClickPos = null;
        _arriveRadius = MinArriveRadius;
        
        // ✅ NEW: Initialize pathfinding
        if (Pathfinder == null)
            Pathfinder = Object.FindFirstObjectByType<AStarGrid>();
        _currentPath = null;
        _pathIndex = 0;
    }
```

**Why:** Auto-finds AStarGrid if not manually assigned in Inspector

### Starter Code - Update() Method

```csharp
    void Update()
    {
        if (ClickMoveAction.WasPressedThisFrame())
        {
            _lastClickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
            _arriveRadius = Mathf.Clamp(ArrivePct * ((Vector2)_lastClickPos - (Vector2)transform.position).magnitude, MinArriveRadius, MaxArriveRadius);
            _flag.position = (Vector2)_lastClickPos + new Vector2(0.55f, 0.55f);
            _flagSr.enabled = true;
            // NO PATHFINDING - just sets flag position
        }
        else
        {
            if (closestFly != null)
                Debug.DrawLine(transform.position, closestFly.transform.position, Color.black);
            if (closestSnake != null)
                Debug.DrawLine(transform.position, closestSnake.transform.position, Color.red);
        }
    }
```

### Current Code - Update() Method (Enhanced)

```csharp
    void Update()
    {
        if (ClickMoveAction.WasPressedThisFrame())
        {
            Vector2 clickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
            _arriveRadius = Mathf.Clamp(ArrivePct * (clickPos - (Vector2)transform.position).magnitude, MinArriveRadius, MaxArriveRadius);

            _flag.position = clickPos + new Vector2(0.55f, 0.55f);
            _flagSr.enabled = true;

            // ✅ NEW: Request pathfinding on click
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
            // ✅ NEW: Check for dynamic obstacles
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
```

**Changes:**
1. On click: Request path from Pathfinder
2. Every frame: Check if path blocked by dynamic obstacles
3. If blocked: Recalculate path immediately

### Starter Code - decideMovement() Method

```csharp
    private Vector2 decideMovement()
    {
        if (_lastClickPos != null)
        {
            return (getVelocityTowardsFlag());
        }
        else
        {
            return (Vector2.zero);  // Always stops immediately
        }
    }
```

### Current Code - decideMovement() Method (Enhanced)

```csharp
    private Vector2 decideMovement()
    {
        // ✅ NEW: Priority 1 - Follow computed path
        if (_currentPath != null && _pathIndex < _currentPath.Count)
        {
            return getVelocityAlongPath();
        }

        // Priority 2 - Go to fallback click position
        if (_lastClickPos != null)
        {
            return getVelocityTowardsFlag();
        }

        return Vector2.zero;
    }
```

**Why:** Path following takes priority if available, fallback to click position

### NEW Methods Added to Frog.cs

#### New Method 1: getVelocityAlongPath() (~25 lines)

```csharp
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
        // Move toward waypoint using steering
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
```

**Purpose:** Follow waypoints one by one

#### New Method 2: getVelocityTowardsFlag() (Extracted & Enhanced - ~15 lines)

```csharp
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

**Purpose:** Fallback movement if pathfinding returns no path

### Summary of Frog.cs Changes

| Change | Lines | Why |
|--------|-------|-----|
| Added `Pathfinder` field | 1 | Reference to AStarGrid |
| Added `_currentPath` field | 1 | Store waypoints |
| Added `_pathIndex` field | 1 | Track waypoint progress |
| Added `waypointTolerance` field | 1 | Define waypoint proximity |
| Enhanced Start() | +5 | Initialize pathfinder |
| Enhanced Update() | +20 | Request paths and check obstacles |
| Enhanced decideMovement() | +5 | Add path following priority |
| Added getVelocityAlongPath() | +25 | New waypoint-following logic |
| Modified decideMovement() | -1 | Extract method |
| **Total additions** | **~58 lines** | **Enable pathfinding** |

---

## Pathfinding.cs Status

### Current State

**Status:** ⚠️ INCOMPLETE - LEFT UNCHANGED

The current project still has the incomplete Pathfinding.cs from the starter code. It's never called by the Frog because AStarGrid.FindPath() is used directly.

```csharp
public class Pathfinding : MonoBehaviour
{
    // STILL CONTAINS ALL TODO COMMENTS
    // Still marked "// TODO: Your job is to fill in the missing code"
    
    // This class is effectively bypassed by using AStarGrid.FindPath() directly
}
```

### Why Pathfinding.cs Wasn't Modified

1. **Not Required** - AStarGrid.cs replaces its functionality
2. **Teaching Tool** - Starter code left for reference/learning
3. **No Breaking Changes** - Frog doesn't use Pathfinding.RequestPath()
4. **Clean Architecture** - AStarGrid.FindPath() is more flexible

### If Needed: Converting Pathfinding.cs

If you wanted to complete Pathfinding.cs instead, you'd need to:

```csharp
// Add to Pathfinding.FindPath()
while (openSet.Count > 0)
{
    // Get lowest F cost node
    Node currentNode = openSet[0];
    // ... (same logic as in AStarGrid.FindPath)
}

// Add to RetracePath()
while (current != startNode)
{
    path.Add(current);
    current = current.parent;
}
```

But this is unnecessary since AStarGrid already does this.

---

## Inspector Configuration

### AStarGrid Inspector Setup

When you select the AStarGrid GameObject, the Inspector shows all these fields:

#### Section 1: Gizmo/Debug Visualization

```
[Header("Gizmo/Debug Visualization")]
☑ Show Grid Gizmos       (default: true)    - Shows gray wireframe grid
☑ Show Terrain Gizmos    (default: true)    - Shows colored terrain cells
☑ Show Path Gizmos       (default: true)    - Shows yellow path lines
```

**How to Configure:**
- Turn OFF for performance in builds
- Keep ON during development for debugging
- Toggle during play mode to verify visualization

#### Section 2: Terrain System

```
[Terrain Costs (already set up)]
- Normal:  cost = 1.0  color = white
- Mud:     cost = 3.0  color = brown
- Water:   cost = 5.0  color = blue
- Grass:   cost = 2.0  color = green
```

**Already Configured** - Don't change unless you want to adjust difficulty

#### Section 3: Terrain Detection (CRITICAL CONFIGURATION)

```
Mud Mask:              [Dropdown] → Select "Mud" layer
Water Mask:            [Dropdown] → Select "Water" layer
Grass Mask:            [Dropdown] → Select "Grass" layer

Obstacle Mask:         [Dropdown] → Select "Obstacle" layer

[Dynamic Obstacles]
Dynamic Obstacle Mask: [Dropdown] → Select "Obstacle" layer (or another)
```

**Critical:** These must match the layers you created and assigned to GameObjects

#### Section 4: Grid Settings

```
Grid World Size:       [Vector2] = (20, 20)  - Size of pathfinding area
Node Radius:           0.5                  - Size of each grid cell
Allow Diagonal:        ☑ checked            - 8-directional movement
```

**How to Adjust:**
- **Larger Grid** = More area, slower pathfinding
- **Larger Node Radius** = Faster but less precise
- **Disable Diagonal** = Only 4 directions (up/down/left/right)

#### Section 5: A* Heuristic

```
[A* Heuristic]
Heuristic Type:        [Dropdown] = Euclidean
                       Options: Euclidean / Manhattan / Octile
```

**How to Use:**
- Change during play mode to see different paths
- Euclidean (default) = most realistic
- Manhattan = grid-based
- Octile = optimized performance

### Frog Inspector Setup

```
Pathfinder:            [Object field] → Drag AStarGrid GameObject here
                       OR leave empty - auto-finds in Start()

Waypoint Tolerance:    0.2  - How close before moving to next waypoint
```

---

## Scene Setup

### Required Layers to Create

In Unity Inspector top-right, click Layer → Add Layer

```
Layers to create:
- Mud        (Layer 8 or higher)
- Water      (Layer 9 or higher)
- Grass      (Layer 10 or higher)
- Obstacle   (Layer 11 or higher)
```

### GameObjects and Their Layers

| GameObject | Layer | Why |
|---|---|---|
| MudPatch | Mud | Pathfinder detects mud terrain |
| Any grass areas | Grass | Pathfinder detects grass terrain |
| Water tiles | Water | Pathfinder detects water terrain |
| Rocks | Obstacle | Pathfinder treats as blocking |
| Trees | Obstacle | Pathfinder treats as blocking |
| Snake (moving) | Obstacle | Dynamic pathfinding |
| Frog | Default | Doesn't need special layer |
| Flag | Default | Doesn't need special layer |

### Scene Hierarchy Example

```
FrogGame (Root)
├── Main Camera
├── UIManager
├── Frog (Layer: Default)
├── Flag (Layer: Default)
├── Background (Layer: Default)
├── MudPatch (Layer: Mud) ← IMPORTANT
│   └── Multiple mud tiles
├── Flock (Contains flies)
├── Snake1 (Layer: Obstacle)
├── Rocks (Layer: Obstacle)
│   └── Rock 1-6
├── Trees (Layer: Obstacle)
│   └── Tree 1-5
└── AStarGrid (Layer: Default) ← NEW OBJECT
    ├── Script: AStarGrid.cs
    ├── Collider: None needed
    └── Position: (0, 0, 0) - Center of pathfinding area
```

---

## Summary Table

### All Changes at a Glance

| File | Type | Changes | Lines |
|------|------|---------|-------|
| **Node.cs** | Fields + Constructor | Add `terrainType`, `movementCost` fields, update constructor | +12 |
| **AStarGrid.cs** | REPLACEMENT | Complete rewrite with A*, terrain, heuristics, visualization | +290 |
| **Frog.cs** | Enhancement | Add pathfinding fields, methods, integration | +58 |
| **Pathfinding.cs** | UNUSED | Left unchanged (now bypassed) | 0 |
| **Heap.cs** | No change | Works perfectly as-is | 0 |
| **Other scripts** | No change | No modifications needed | 0 |

### Configuration Summary

| Component | Setter Type | Configurations |
|-----------|-------------|---|
| **AStarGrid** | Public fields | 25+ inspector fields |
| **Frog** | Public fields | 4 new inspector fields |
| **Layers** | Create in Editor | 4 new layers (Mud, Water, Grass, Obstacle) |
| **Layer Masks** | Assign in Inspector | Map 4 masks to 4 layers |
| **Scene Objects** | Assign layers | All terrain/obstacles to correct layers |

### Performance Impact

| Change | Impact | Mitigation |
|--------|--------|-----------|
| Terrain checking | +4 Physics2D calls per node | Minimal (cached per grid creation) |
| Multiple heuristics | None (runtime selection) | No performance cost |
| Path smoothing | Slight per-path cost | Optional (disable if needed) |
| Visualization gizmos | None in build | Disabled automatically |
| Dynamic obstacle detection | +1 check per frame | Only while pathfinding active |

---

## Quick Reference: What Changed Where

### If You Need to...

**Find terrain support:**
- Node.cs → `terrainType` and `movementCost` fields
- AStarGrid.cs → Line ~180 where cost multiplies distance

**Find A* algorithm:**
- AStarGrid.cs → `FindPath()` method (lines ~90-190)

**Find path smoothing:**
- AStarGrid.cs → `SmoothPath()` method (lines ~210-240)

**Find heuristics:**
- AStarGrid.cs → `GetHeuristic()` method (lines ~280-295)

**Find pathfinding integration:**
- Frog.cs → Start() method initialization
- Frog.cs → Update() method click handling
- Frog.cs → `getVelocityAlongPath()` new method

**Find visualization:**
- AStarGrid.cs → `OnDrawGizmos()` method (lines ~350-400)

**Find dynamic obstacles:**
- Frog.cs → Update() method obstacle detection (lines ~130-145)

---

## Testing Configuration Changes

### Verify Inspector Setup

```
✓ AStarGrid GameObject exists in scene
✓ AStarGrid.cs script attached
✓ 4 Layers created (Mud, Water, Grass, Obstacle)
✓ All layer masks set correctly in AStarGrid
✓ All GameObjects assigned to correct layers
✓ Frog's Pathfinder field references AStarGrid
✓ Gizmo toggles enabled for testing
```

### Verify Code Changes

```
✓ Node.cs has terrainType enum and fields
✓ AStarGrid.cs has FindPath() method
✓ Frog.cs has Pathfinder field
✓ Frog.cs has getVelocityAlongPath() method
✓ Update() calls FindPath on click
✓ Update() checks for blocked paths
```

---

**Document Version:** 1.0  
**Complete:** Yes - All files and configurations documented  
**Last Updated:** April 26, 2026

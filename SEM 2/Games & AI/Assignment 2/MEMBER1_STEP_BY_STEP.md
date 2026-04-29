# Member 1 – A* Pathfinding: Complete Step-by-Step Guide
### Start from the starter code and follow every step in order.

---

## OVERVIEW — What you are building

You need to make the frog move using A* pathfinding instead of going directly to the click.
The frog must avoid rocks and trees, handle different terrain speeds, smooth its path, and
reroute when a moving obstacle blocks its way.

There are **4 phases**:
1. Code changes (edit C# scripts)
2. Unity layer setup (create layers in Unity)
3. Scene setup (place objects in the scene)
4. Inspector wiring (connect everything in the Inspector)

---

## PHASE 1 — CODE CHANGES

Do these in order. Each step tells you the file, what to replace, and what to put instead.

---

### STEP 1 — Add terrain data to Node.cs

**Open:** `Assets/Scripts/Pathfinding/Node.cs`

**Find this (around line 7):**
```csharp
public class Node : IHeapItem<Node>
{
    // Can the node be reached (ie, no obstacle)
    public bool walkable;
```

**Replace the entire file with this:**
```csharp
// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;

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
    public Vector2 worldPosition;
    public int gridX;
    public int gridY;
    public float gCost;
    public float hCost;
    public Node parent;
    public TerrainType terrainType;
    public float movementCost;

    int heapIndex;

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

    public Node Clone()
    {
        return new Node(walkable, worldPosition, gridX, gridY, terrainType, movementCost);
    }

    public float fCost
    {
        get { return gCost + hCost; }
    }

    public int HeapIndex
    {
        get { return heapIndex; }
        set { heapIndex = value; }
    }

    public int CompareTo(Node nodeToCompare)
    {
        int compare = fCost.CompareTo(nodeToCompare.fCost);
        if (compare == 0)
            compare = hCost.CompareTo(nodeToCompare.hCost);
        return -compare;
    }
}
```

**Why:** The starter Node has no terrain info. We add `TerrainType` (what kind of ground this cell is) and `movementCost` (how expensive it is to walk through). A* will multiply the step cost by this when calculating g(n).

---

### STEP 2 — Replace AStarGrid.cs completely

**Open:** `Assets/Scripts/Pathfinding/AStarGrid.cs`

**Replace the entire file with this:**
```csharp
// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;
using System.Collections.Generic;

public class AStarGrid : MonoBehaviour
{
    [Header("Gizmo Display")]
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

    [Header("Terrain Gizmo Colors")]
    public Color normalColor = Color.white;
    public Color mudColor = new Color(0.4f, 0.25f, 0.1f);
    public Color waterColor = Color.cyan;
    public Color grassColor = Color.green;

    [Header("Grid Settings")]
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

    Node[,] grid;
    float nodeDiameter;
    int gridSizeX, gridSizeY;
    Vector2 worldBottomLeft;

    void Awake()
    {
        CreateGrid();
    }

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

    public void CreateGrid()
    {
        if (gridSize <= 0f) gridSize = 0.5f;
        if (gridWorldSize.x <= 0f || gridWorldSize.y <= 0f)
            gridWorldSize = new Vector2(Mathf.Max(1f, gridWorldSize.x), Mathf.Max(1f, gridWorldSize.y));
        if (overlapCircleRadius <= 0f)
            overlapCircleRadius = gridSize * 0.8f;

        nodeDiameter = gridSize * 2f;
        gridSizeX = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.x / nodeDiameter));
        gridSizeY = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.y / nodeDiameter));

        grid = new Node[gridSizeX, gridSizeY];
        worldBottomLeft = (Vector2)transform.position
                          - Vector2.right * gridWorldSize.x / 2
                          - Vector2.up   * gridWorldSize.y / 2;

        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector2 worldPoint = worldBottomLeft
                    + Vector2.right * (x * nodeDiameter + gridSize)
                    + Vector2.up   * (y * nodeDiameter + gridSize);

                bool walkable = Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, unwalkableMask) == null;

                Node.TerrainType terrainType = GetTerrainTypeAtPoint(worldPoint);
                float movementCost = GetTerrainCost(terrainType);

                grid[x, y] = new Node(walkable, worldPoint, x, y, terrainType, movementCost);
            }
        }
    }

    public List<Node> GetNeighbours(Node node)
    {
        List<Node> neighbours = new List<Node>();

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0) continue;

                if (!includeDiagonalNeighbours && Mathf.Abs(x) + Mathf.Abs(y) == 2)
                    continue;

                int checkX = node.gridX + x;
                int checkY = node.gridY + y;

                if (!InBounds(checkX, checkY)) continue;

                // Prevent cutting through wall corners diagonally
                if (Mathf.Abs(x) == 1 && Mathf.Abs(y) == 1)
                {
                    bool hOk = InBounds(node.gridX + x, node.gridY) && grid[node.gridX + x, node.gridY].walkable;
                    bool vOk = InBounds(node.gridX, node.gridY + y) && grid[node.gridX, node.gridY + y].walkable;
                    if (!hOk || !vOk) continue;
                }

                neighbours.Add(grid[checkX, checkY]);
            }
        }

        return neighbours;
    }

    public float GetHeuristicDistance(Node from, Node to)
    {
        float dx = Mathf.Abs(from.gridX - to.gridX);
        float dy = Mathf.Abs(from.gridY - to.gridY);

        switch (heuristicType)
        {
            case PathHeuristic.Manhattan:
                return dx + dy;
            case PathHeuristic.Octile:
                float diag = Mathf.Min(dx, dy);
                float straight = Mathf.Max(dx, dy) - diag;
                return diag * Mathf.Sqrt(2f) + straight;
            case PathHeuristic.Chebyshev:
                return Mathf.Max(dx, dy);
            default: // Euclidean
                return Mathf.Sqrt(dx * dx + dy * dy);
        }
    }

    public float GetStepCost(Node from, Node to)
    {
        float baseCost = Vector2.Distance(from.worldPosition, to.worldPosition);
        return baseCost * to.movementCost;
    }

    public bool IsPathSegmentClear(Vector2 from, Vector2 to)
    {
        // Also block smoothing through expensive terrain (mud, water)
        // so the smoother doesn't shortcut through terrain A* deliberately routed around.
        LayerMask blockingMask = unwalkableMask | dynamicObstacleMask | mudMask | waterMask;
        return Physics2D.Linecast(from, to, blockingMask) == false;
    }

    public bool IsPointBlockedByDynamicObstacle(Vector2 worldPoint)
    {
        return Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, dynamicObstacleMask) != null;
    }

    public void RecordPath(Node[] path)
    {
        if (path == null || path.Length == 0) { lastWorldPath = null; return; }
        lastWorldPath = new Vector2[path.Length];
        for (int i = 0; i < path.Length; i++)
            lastWorldPath[i] = path[i].worldPosition;
    }

    public Node NodeFromWorldPoint(Vector2 worldPosition)
    {
        if (grid == null || gridSizeX <= 0 || gridSizeY <= 0) return null;

        float percentX = (worldPosition.x - worldBottomLeft.x) / gridWorldSize.x;
        float percentY = (worldPosition.y - worldBottomLeft.y) / gridWorldSize.y;
        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.RoundToInt((gridSizeX - 1) * percentX);
        int y = Mathf.RoundToInt((gridSizeY - 1) * percentY);
        return grid[x, y];
    }

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
            int vx = i + centreX;
            int hy = i + centreY;

            if (InBounds(vx, centreY + radius) && grid[vx, centreY + radius].walkable)
                return grid[vx, centreY + radius];
            if (InBounds(vx, centreY - radius) && grid[vx, centreY - radius].walkable)
                return grid[vx, centreY - radius];
            if (InBounds(centreX + radius, hy) && grid[centreX + radius, hy].walkable)
                return grid[centreX + radius, hy];
            if (InBounds(centreX - radius, hy) && grid[centreX - radius, hy].walkable)
                return grid[centreX - radius, hy];
        }
        return null;
    }

    bool InBounds(int x, int y)
    {
        return x >= 0 && x < gridSizeX && y >= 0 && y < gridSizeY;
    }

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

    private Node.TerrainType GetTerrainTypeAtPoint(Vector2 worldPoint)
    {
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, mudMask)   != null) return Node.TerrainType.Mud;
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, waterMask) != null) return Node.TerrainType.Water;
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, grassMask) != null) return Node.TerrainType.Grass;
        return Node.TerrainType.Normal;
    }

    private float GetTerrainCost(Node.TerrainType t)
    {
        switch (t)
        {
            case Node.TerrainType.Mud:   return mudCost;
            case Node.TerrainType.Water: return waterCost;
            case Node.TerrainType.Grass: return grassCost;
            default:                     return normalCost;
        }
    }

    private Color GetTerrainColor(Node.TerrainType t)
    {
        switch (t)
        {
            case Node.TerrainType.Mud:   return mudColor;
            case Node.TerrainType.Water: return waterColor;
            case Node.TerrainType.Grass: return grassColor;
            default:                     return normalColor;
        }
    }
}
```

**Why:** This replaces the basic starter grid with one that handles terrain, 8-direction movement with corner clipping, 4 heuristics, path smoothing support, and dynamic obstacle detection. The `IsPathSegmentClear` includes mud and water in its linecast so the smoother cannot shortcut through expensive terrain.

---

### STEP 3 — Replace Pathfinding.cs completely

**Open:** `Assets/Scripts/Pathfinding/Pathfinding.cs`

**Replace the entire file with this:**
```csharp
// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;
using System.Collections.Generic;
using System;

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
                Debug.LogWarning("Pathfinding: No AStarGrid found.");
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

    static Node[] FindPath(Vector2 from, Vector2 to)
    {
        Node[] waypoints = new Node[0];
        if (grid == null) return waypoints;

        grid.ResetSearchData();

        bool pathSuccess = false;

        Node startNode  = grid.NodeFromWorldPoint(from);
        Node targetNode = grid.NodeFromWorldPoint(to);

        if (startNode == null || targetNode == null) return waypoints;

        startNode.parent = startNode;

        if (!startNode.walkable)  startNode  = grid.ClosestWalkableNode(startNode);
        if (!targetNode.walkable) targetNode = grid.ClosestWalkableNode(targetNode);

        if (startNode == null || targetNode == null) return waypoints;

        if (startNode.walkable && targetNode.walkable)
        {
            Heap<Node>     openSet   = new Heap<Node>(grid.MaxSize);
            HashSet<Node>  closedSet = new HashSet<Node>();

            startNode.gCost = 0f;
            startNode.hCost = Heuristic(startNode, targetNode);
            startNode.parent = startNode;
            openSet.Add(startNode);

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
                        if (!node.walkable
                            || closedSet.Contains(node)
                            || grid.IsPointBlockedByDynamicObstacle(node.worldPosition))
                            continue;

                        float newCost = currentNode.gCost + GCost(currentNode, node);

                        if (!openSet.Contains(node) || newCost < node.gCost)
                        {
                            node.gCost  = newCost;
                            node.hCost  = Heuristic(node, targetNode);
                            node.parent = currentNode;

                            if (!openSet.Contains(node))
                                openSet.Add(node);
                            else
                                openSet.UpdateItem(node);
                        }
                    }
                }
            }
        }

        if (pathSuccess)
        {
            waypoints = RetracePath(startNode, targetNode);
            if (grid.enablePathSmoothing)
                waypoints = SmoothPath(waypoints);
            grid.RecordPath(waypoints);
        }
        else
        {
            grid.RecordPath(null);
        }

        return waypoints;
    }

    static Node[] RetracePath(Node startNode, Node endNode)
    {
        List<Node> path = new List<Node>();
        Node current = endNode;

        while (current != startNode)
        {
            path.Add(current);
            current = current.parent;
            if (current == null) break;
        }

        Node[] waypoints = path.ToArray();
        Array.Reverse(waypoints);
        return waypoints;
    }

    static float GCost(Node a, Node b)      { return grid.GetStepCost(a, b); }
    static float Heuristic(Node a, Node b)  { return grid.GetHeuristicDistance(a, b); }

    static Node[] SmoothPath(Node[] path)
    {
        if (path == null || path.Length < 3) return path;

        List<Node> smoothed = new List<Node>();
        int current = 0;
        smoothed.Add(path[current]);

        while (current < path.Length - 1)
        {
            int furthest = current + 1;

            for (int candidate = path.Length - 1; candidate > current; candidate--)
            {
                if (grid.IsPathSegmentClear(path[current].worldPosition, path[candidate].worldPosition))
                {
                    furthest = candidate;
                    break;
                }
            }

            if (furthest == current) break;
            current = furthest;
            smoothed.Add(path[current]);
        }

        return smoothed.ToArray();
    }
}
```

**Why:** The starter had all A* logic replaced with empty `if (false)` placeholders. This implements the complete algorithm: open/closed sets, terrain-weighted g cost, configurable heuristic, dynamic obstacle skipping, path retracing, and line-of-sight smoothing.

---

### STEP 4 — Replace Frog.cs completely

**Open:** `Assets/Scripts/Frog.cs`

**Replace the entire file with this:**
```csharp
using UnityEngine;
using UnityEngine.InputSystem;
using System.Collections.Generic;
using SteeringCalcs;
using Globals;

public class Frog : MonoBehaviour
{
    // Frog status
    public int Health;

    // Steering parameters
    public float MaxSpeed;
    public float MaxAccel;
    public float AccelTime;

    public float ArrivePct;
    public float MinArriveRadius;
    public float MaxArriveRadius;
    private float _arriveRadius;

    public bool HideFlagOnceReached;

    // Scene references
    private Transform _flag;
    private SpriteRenderer _flagSr;
    private DrawGUI _drawGUIScript;
    private Animator _animator;
    private Rigidbody2D _rb;
    private InputAction ClickMoveAction;
    private Vector2? _lastClickPos;

    // Decision Tree fields (used by Members 2/3 later)
    public float scaredRange;
    public float huntRange;
    private Fly closestFly;
    private Snake closestSnake;
    private float distanceToClosestFly;
    private float distanceToClosestSnake;
    public float anchorWeight;
    public Vector2 AnchorDims;

    [Header("A* Movement")]
    public float waypointTolerance = 0.5f;
    public float dynamicRepathInterval = 0.3f;
    public bool drawPathDebugLines = true;
    public bool allowDirectFallbackWhenNoPath = false;

    private Node[] _currentPath;
    private int _pathIndex;
    private Vector2? _pathGoal;
    private float _nextDynamicRepathTime;

    void Start()
    {
        _flag   = GameObject.Find("Flag").transform;
        _flagSr = _flag.GetComponent<SpriteRenderer>();
        _flagSr.enabled = false;

        GameObject ui = GameObject.Find("UIManager");
        if (ui != null) _drawGUIScript = ui.GetComponent<DrawGUI>();

        _animator = GetComponent<Animator>();
        _rb       = GetComponent<Rigidbody2D>();

        ClickMoveAction = InputSystem.actions.FindAction("Attack");

        _lastClickPos          = null;
        _arriveRadius          = MinArriveRadius;
        _currentPath           = null;
        _pathIndex             = 0;
        _pathGoal              = null;
        _nextDynamicRepathTime = 0f;
    }

    void Update()
    {
        if (ClickMoveAction.WasPressedThisFrame())
        {
            _lastClickPos = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());

            _arriveRadius = Mathf.Clamp(
                ArrivePct * ((Vector2)_lastClickPos - (Vector2)transform.position).magnitude,
                MinArriveRadius, MaxArriveRadius);

            _flag.position  = (Vector2)_lastClickPos + new Vector2(0.55f, 0.55f);
            _flagSr.enabled = true;

            RequestPathTo((Vector2)_lastClickPos);
        }
        else
        {
            TryRecalculatePathForDynamicObstacles();

            if (closestFly   != null) Debug.DrawLine(transform.position, closestFly.transform.position,   Color.black);
            if (closestSnake != null) Debug.DrawLine(transform.position, closestSnake.transform.position, Color.red);
        }
    }

    void FixedUpdate()
    {
        Vector2 desiredVel = decideMovement();
        Debug.DrawLine((Vector2)transform.position, (Vector2)transform.position + desiredVel, Color.blue);
        Vector2 steering = Steering.DesiredVelToForce(desiredVel, _rb, AccelTime, MaxAccel);
        _rb.AddForce(steering);
        UpdateAppearance();
    }

    private void UpdateAppearance()
    {
        if (_rb.linearVelocity.magnitude > Constants.MIN_SPEED_TO_ANIMATE)
        {
            _animator.SetBool("Walking", true);
            transform.up = _rb.linearVelocity;
        }
        else
        {
            _animator.SetBool("Walking", false);
        }
    }

    public void TakeDamage()
    {
        if (Health > 0) Health--;
    }

    // ── Movement decision ──────────────────────────────────────────────────

    private Vector2 decideMovement()
    {
        if (_currentPath != null && _pathIndex < _currentPath.Length)
            return getVelocityAlongPath();

        if (allowDirectFallbackWhenNoPath && _lastClickPos != null)
            return getVelocityTowardsFlag();

        return Vector2.zero;
    }

    private Vector2 getVelocityTowardsFlag()
    {
        if (_lastClickPos == null) return Vector2.zero;

        if (((Vector2)_lastClickPos - (Vector2)transform.position).magnitude > Constants.TARGET_REACHED_TOLERANCE)
        {
            return Steering.ArriveDirect(transform.position, (Vector2)_lastClickPos, _arriveRadius, MaxSpeed);
        }
        else
        {
            _lastClickPos = null;
            if (HideFlagOnceReached) _flagSr.enabled = false;
            return Vector2.zero;
        }
    }

    private Vector2 getVelocityAlongPath()
    {
        if (_currentPath == null || _pathIndex >= _currentPath.Length)
            return Vector2.zero;

        Vector2 currentWaypoint = _currentPath[_pathIndex].worldPosition;

        if (drawPathDebugLines)
            Debug.DrawLine(transform.position, currentWaypoint, Color.yellow);

        bool  isFinalWaypoint  = (_pathIndex == _currentPath.Length - 1);
        float distToWaypoint   = ((Vector2)transform.position - currentWaypoint).magnitude;
        bool  arrivedAtFinal   = isFinalWaypoint && distToWaypoint <= _arriveRadius * 0.15f;

        if (distToWaypoint <= waypointTolerance || arrivedAtFinal)
        {
            _pathIndex++;
            if (_pathIndex >= _currentPath.Length)
            {
                _currentPath = null;
                _pathIndex   = 0;
                _pathGoal    = null;
                if (HideFlagOnceReached) _flagSr.enabled = false;
                return Vector2.zero;
            }
            currentWaypoint = _currentPath[_pathIndex].worldPosition;
        }

        // Seek at full speed through intermediate waypoints; slow down with Arrive at the end
        if (isFinalWaypoint)
            return Steering.ArriveDirect(transform.position, currentWaypoint, _arriveRadius, MaxSpeed);
        else
            return Steering.SeekDirect(transform.position, currentWaypoint, MaxSpeed);
    }

    // ── Path requests ──────────────────────────────────────────────────────

    private void RequestPathTo(Vector2 destination)
    {
        Node[] path = Pathfinding.RequestPath(transform.position, destination);

        if (path != null && path.Length > 0)
        {
            _pathGoal    = destination;
            _currentPath = path;
            _pathIndex   = 0;
            _lastClickPos = null;
        }
        else
        {
            _pathGoal    = null;
            _currentPath = null;
            _pathIndex   = 0;
            _lastClickPos = allowDirectFallbackWhenNoPath ? destination : (Vector2?)null;
            Debug.LogWarning("A* found no path. Direct fallback: " + allowDirectFallbackWhenNoPath);
        }
    }

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

    // ── Helper finders (used by Decision Tree later) ───────────────────────

    private void findClosestFly()
    {
        distanceToClosestFly = Mathf.Infinity;
        foreach (Fly fly in (Fly[])GameObject.FindObjectsByType(typeof(Fly), FindObjectsSortMode.None))
        {
            float d = (fly.transform.position - transform.position).magnitude;
            if (fly.State != Fly.FlyState.Dead && d < distanceToClosestFly)
            {
                closestFly           = fly;
                distanceToClosestFly = d;
            }
        }
    }

    private void findClosestSnake()
    {
        distanceToClosestSnake = Mathf.Infinity;
        foreach (Snake snake in (Snake[])GameObject.FindObjectsByType(typeof(Snake), FindObjectsSortMode.None))
        {
            float d = (snake.transform.position - transform.position).magnitude;
            if (d < distanceToClosestSnake)
            {
                closestSnake           = snake;
                distanceToClosestSnake = d;
            }
        }
    }

    private bool isOutOfScreen(Transform t)
    {
        Vector3 vp = Camera.main.WorldToViewportPoint(t.position);
        return vp.x < 0f || vp.x > 1f || vp.y < 0f || vp.y > 1f;
    }
}
```

**Why:** The starter Frog had no A* integration at all — it moved directly toward the click via steering. This version: requests a path on click, follows waypoints (Seek for intermediate, Arrive for final so it slows down naturally), checks for dynamic obstacles every 0.3 seconds, and clears the path correctly when the frog arrives.

---

That is all the code. **No other files need changes.**

---

## PHASE 2 — UNITY LAYER SETUP

Do this in the Unity Editor before touching the scene.

**Step 5 — Create the required layers**

1. In Unity, go to **Edit → Project Settings → Tags and Layers**
2. In the **Layers** section, find the first empty slot (probably User Layer 6 or 7)
3. Create these layers one by one by typing the name in the box:
   - `Mud`
   - `Water`
   - `Grass`
   - `DynamicObstacle`
4. Close Project Settings

> These exact names do not matter — what matters is that you assign the same layers in the Inspector later. Just be consistent.

---

## PHASE 3 — SCENE SETUP

**Open the FrogGame scene.** Do the following:

---

### Step 6 — Set up the A* Grid GameObject

1. In the **Hierarchy**, find the GameObject that has the **Pathfinding** component on it
   (it should also have **AStarGrid** on it — both must be on the same object)
2. If they are not on the same GameObject, select the Pathfinding GameObject, then in the
   Inspector click **Add Component** and add **AStarGrid**
3. Set these values on the **AStarGrid** component:
   - `Grid World Size` → set X and Y to cover the full scene (e.g. X=40, Y=25)
   - `Grid Size` → 0.5 (half a Unity unit per node)
   - `Overlap Circle Radius` → 0.4
   - `Include Diagonal Neighbours` → **checked**
   - `Enable Path Smoothing` → **checked**
   - `Heuristic Type` → Euclidean (you can change this during the demo)
   - `Display Grid Gizmos` → **checked** (so you can see the grid)
   - `Display Terrain Gizmos` → **checked**
   - `Display Path Gizmos` → **checked**
4. Under **Obstacle Layers**, click the `Unwalkable Mask` dropdown and tick every layer that
   contains rocks, trees, walls — whatever is physically blocking the scene

---

### Step 7 — Create terrain tiles (Mud, Water, Grass)

You need coloured tile objects placed in the scene. Do this for each terrain type:

**For Mud:**
1. In the Hierarchy, right-click → **2D Object → Sprite → Square**
2. Name it `MudTile`
3. In the Inspector, set its **SpriteRenderer** colour to a brown colour
   (R=100, G=65, B=25 or just pick brown)
4. Add a **Box Collider 2D** component to it (this is how the grid detects it)
5. In the Inspector at the top, click the **Layer** dropdown and select **Mud**
6. Scale it to cover a region of your scene (e.g. scale X=4, Y=4 for a 4×4 tile)
7. Position it somewhere in the walkable area of the scene
8. Repeat — place 2 or 3 mud tiles in different spots

**For Water:** Same steps, colour it blue, layer = Water, name it `WaterTile`

**For Grass:** Same steps, colour it green, layer = Grass, name it `GrassTile`

> **Important:** The `Box Collider 2D` must NOT be a trigger. It must be a solid collider.
> The grid uses `Physics2D.OverlapCircle` to detect which terrain a node is on.

---

### Step 8 — Assign terrain layers in AStarGrid Inspector

1. Select the AStarGrid GameObject in the Hierarchy
2. In the Inspector, find the **Terrain Layers** section
3. Click the `Mud Mask` dropdown → tick **Mud**
4. Click the `Water Mask` dropdown → tick **Water**
5. Click the `Grass Mask` dropdown → tick **Grass**

---

### Step 9 — Create a moving dynamic obstacle

The simplest option: use the existing snake as the dynamic obstacle. Alternatively, create a new
moving object:

**Option A — Use the snake (easiest):**
1. Select the Snake GameObject in the Hierarchy
2. Change its **Layer** to **DynamicObstacle**
3. Make sure it has a **Collider 2D** on it

**Option B — Create a new simple patrol obstacle:**
1. Right-click Hierarchy → **2D Object → Sprite → Square**
2. Name it `MovingObstacle`
3. Set its layer to **DynamicObstacle**
4. Give it a **Rigidbody 2D** (set Body Type = Kinematic) and a **Box Collider 2D**
5. Colour it black or orange so it is obvious in the demo
6. Create a new script called `PatrolObstacle.cs` and paste this:

```csharp
using UnityEngine;

public class PatrolObstacle : MonoBehaviour
{
    public Vector2 pointA;
    public Vector2 pointB;
    public float speed = 2f;

    private Vector2 target;

    void Start()
    {
        target = pointB;
    }

    void Update()
    {
        transform.position = Vector2.MoveTowards(transform.position, target, speed * Time.deltaTime);
        if (Vector2.Distance(transform.position, target) < 0.1f)
            target = (target == pointA) ? pointB : pointA;
    }
}
```

7. Attach this script to the MovingObstacle. Set `Point A` and `Point B` to two positions in the
   scene that cross a path the frog would normally take.

**Then in AStarGrid Inspector:**
- Click `Dynamic Obstacle Mask` → tick **DynamicObstacle**

---

## PHASE 4 — INSPECTOR WIRING

### Step 10 — Check the Frog's Inspector values

Select the **Frog** GameObject. Set these values:

| Field | Suggested Value |
|---|---|
| Health | 3 |
| Max Speed | 5 |
| Max Accel | 20 |
| Accel Time | 0.2 |
| Arrive Pct | 0.3 |
| Min Arrive Radius | 0.5 |
| Max Arrive Radius | 5 |
| Hide Flag Once Reached | checked |
| Waypoint Tolerance | 0.5 |
| Dynamic Repath Interval | 0.3 |
| Draw Path Debug Lines | checked |
| Allow Direct Fallback When No Path | unchecked |

---

### Step 11 — Press Play and verify everything works

Go through this checklist in order:

1. **Grid appears** — In the Scene view (not Game view), do you see coloured squares over the
   scene? Red = unwalkable (rocks/trees), white = normal. If you see nothing, check that
   `Display Grid Gizmos` is on and `Grid World Size` is large enough.

2. **Terrain colours appear** — Do you see brown/blue/green tiles where you placed terrain objects?
   If not, check that terrain layer masks are assigned in the AStarGrid Inspector.

3. **Frog follows path** — Right-click in the scene. Does the frog move toward the click while
   going around rocks? You should see a yellow debug line (in Game view) showing the current
   waypoint.

4. **Path gizmo appears** — In Scene view during Play, do you see a yellow line showing the full
   A* path? If not, check `Display Path Gizmos` is on.

5. **Smoothing works** — Turn `Enable Path Smoothing` off in the Inspector during Play. Does the
   path become more zig-zag? Turn it back on. Does it become smoother?

6. **Terrain affects path** — Click a destination that is accessible through either normal ground
   or mud. Does the frog prefer the longer normal-ground route over the shorter muddy route?
   If mud cost is 3× and the path through mud is less than 3× shorter, A* should avoid it.

7. **Dynamic obstacle reroutes frog** — Click somewhere. While the frog is walking, move the
   dynamic obstacle (or wait for it to patrol) into the frog's path. Within 0.3 seconds, does the
   frog change direction to go around it?

8. **Heuristic switch** — During Play, change `Heuristic Type` in the Inspector from Euclidean to
   Chebyshev. Click somewhere. In the Scene view gizmos, does the search frontier (the path
   shape) look wider? Switch back to Euclidean — does it look tighter?

---

## QUICK TROUBLESHOOTING

| Problem | Likely Cause | Fix |
|---|---|---|
| Frog doesn't move at all | Path always empty | Check `Unwalkable Mask` — if it includes the wrong layer, every node is unwalkable |
| Frog walks through walls | Unwalkable mask not set | Assign the wall/rock layer to `Unwalkable Mask` in AStarGrid |
| Terrain colours not showing | Layer masks not assigned | Assign Mud/Water/Grass layers in AStarGrid Terrain Layers section |
| Terrain doesn't affect path | Collider missing on terrain tile | Add Box Collider 2D to each terrain tile GameObject |
| Dynamic repath not happening | Dynamic mask not set | Assign DynamicObstacle layer to `Dynamic Obstacle Mask` in AStarGrid |
| Frog freezes near destination | Arrive radius too large | Lower `Min Arrive Radius` to 0.3 or lower `Waypoint Tolerance` |
| "No AStarGrid found" warning | Pathfinding and AStarGrid not on same object | Add AStarGrid component to same GameObject as Pathfinding |
| Path smoothing cuts through mud | IsPathSegmentClear missing terrain mask | Check Step 2 — the new AStarGrid code already fixes this |

---

## FOR THE DEMO VIDEO — What to show for each feature

### A* Base movement (2 marks)
- Right-click → frog navigates around a rock/tree
- Point to the yellow debug line in the Game view showing the waypoint
- Say: "The path is computed with A*, 8-direction movement, Euclidean heuristic. It only
  recalculates when the player clicks, not every frame."

### Varying Terrain (2 marks)
- Enable `Display Terrain Gizmos`, show the brown/blue/green tiles in Scene view
- Click a destination reachable through mud OR around it — show the frog going around
- Say: "Mud costs 3× normal movement. A* prefers a longer path on flat ground over a shorter
  path through mud. The gizmo shows terrain colour per node."

### Varying Heuristics (2 marks)
- In Play Mode, switch heuristic in Inspector from Euclidean → Chebyshev, click somewhere
- Show Scene view: wider search pattern with Chebyshev
- Switch to Octile: show more direct path
- Say: "Chebyshev is max(dx,dy) — it underestimates more than Euclidean, so A* explores
  more nodes. Octile is optimal for 8-direction grids. Both are admissible."

### Path Smoothing (2 marks)
- Uncheck `Enable Path Smoothing`, click a destination near corners, show zig-zag path gizmo
- Recheck it, same click — show the smoother diagonal path
- Say: "Smoothing uses line-of-sight. It skips grid waypoints if there's a clear straight line
  between them. It does NOT skip through mud or water because those layers are in the
  linecast mask."

### Dynamic Obstacles (2 marks)
- Show the patrol obstacle moving back and forth
- Right-click a destination on the other side of the obstacle
- Show the frog navigating around the obstacle as it moves
- Say: "Every 0.3 seconds, the frog checks if any remaining waypoint is blocked by a dynamic
  obstacle. If so, it requests a new path from its current position."

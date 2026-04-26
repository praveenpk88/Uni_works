// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;
using System.Collections.Generic;

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

    // 8-direction movement support.
    public bool includeDiagonalNeighbours = true;

    [HideInInspector]
    public Vector2[] lastWorldPath;

    public enum PathHeuristic
    {
        Euclidean,
        Manhattan,
        Octile,
        // Custom admissible heuristic: Chebyshev distance.
        // Returns max(dx, dy) — the fewest moves needed if every step were free.
        // Always admissible because max(dx,dy) <= actual path cost for 8-direction movement.
        // Less informed than Euclidean so A* explores more nodes, which is visible in gizmos.
        Chebyshev
    }

    Node[,] grid;
    float nodeDiameter;
    int gridSizeX, gridSizeY;
    Vector2 worldBottomLeft;
    bool warnedGridSize;
    bool warnedWorldSize;
    bool warnedOverlap;

    void Awake()
    {
        CreateGrid();
    }

    public int MaxSize
    {
        get
        {
            long size = (long)gridSizeX * gridSizeY;
            if (size <= 0)
            {
                return 1;
            }

            if (size > int.MaxValue)
            {
                return int.MaxValue;
            }

            return (int)size;
        }
    }

    public void CreateGrid()
    {
        // Guard against invalid inspector values causing division by zero/overflow.
        if (gridSize <= 0f)
        {
            if (!warnedGridSize)
            {
                Debug.LogWarning("AStarGrid.gridSize must be > 0. Auto-correcting to 0.5.");
                warnedGridSize = true;
            }
            gridSize = 0.5f;
        }

        if (gridWorldSize.x <= 0f || gridWorldSize.y <= 0f)
        {
            if (!warnedWorldSize)
            {
                Debug.LogWarning("AStarGrid.gridWorldSize must be positive. Auto-correcting invalid axes to 1.");
                warnedWorldSize = true;
            }
            gridWorldSize = new Vector2(Mathf.Max(1f, gridWorldSize.x), Mathf.Max(1f, gridWorldSize.y));
        }

        if (overlapCircleRadius <= 0f)
        {
            overlapCircleRadius = gridSize * 0.8f;
            if (!warnedOverlap)
            {
                Debug.LogWarning("AStarGrid.overlapCircleRadius must be > 0. Auto-correcting based on gridSize.");
                warnedOverlap = true;
            }
        }

        nodeDiameter = gridSize * 2f;
        gridSizeX = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.x / nodeDiameter));
        gridSizeY = Mathf.Max(1, Mathf.RoundToInt(gridWorldSize.y / nodeDiameter));

        grid = new Node[gridSizeX, gridSizeY];
        worldBottomLeft = (Vector2)transform.position - Vector2.right * gridWorldSize.x / 2 - Vector2.up * gridWorldSize.y / 2;

        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector2 worldPoint = worldBottomLeft + Vector2.right * (x * nodeDiameter + gridSize) + Vector2.up * (y * nodeDiameter + gridSize);

                bool blockedByStatic = Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, unwalkableMask) != null;
                // Dynamic obstacles are handled at runtime by repath checks; they should not permanently mark cells unwalkable.
                bool walkable = !blockedByStatic;

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
                if (x == 0 && y == 0)
                {
                    continue;
                }

                if (!includeDiagonalNeighbours && Mathf.Abs(x) + Mathf.Abs(y) == 2)
                {
                    continue;
                }

                int checkX = node.gridX + x;
                int checkY = node.gridY + y;

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
                float diagonal = Mathf.Min(dx, dy);
                float straight = Mathf.Max(dx, dy) - diagonal;
                return diagonal * Mathf.Sqrt(2f) + straight;
            case PathHeuristic.Chebyshev:
                // max(dx, dy) — the number of moves needed if we could go in any direction for free.
                // Admissible: the cheapest possible move costs 1.0, and we need at least max(dx,dy)
                // moves, so max(dx,dy) * 1.0 never exceeds the actual cost.
                // Because it underestimates more than Euclidean, A* expands more nodes and you
                // can visually see the wider search frontier in the gizmos.
                return Mathf.Max(dx, dy);
            default:
                return Mathf.Sqrt(dx * dx + dy * dy);
        }
    }

    public float GetStepCost(Node from, Node to)
    {
        float baseStepCost = Vector2.Distance(from.worldPosition, to.worldPosition);
        return baseStepCost * to.movementCost;
    }

    public bool IsPathSegmentClear(Vector2 from, Vector2 to)
    {
        LayerMask blockingMask = unwalkableMask | dynamicObstacleMask;
        return Physics2D.Linecast(from, to, blockingMask) == false;
    }

    public bool IsPointBlockedByDynamicObstacle(Vector2 worldPoint)
    {
        return Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, dynamicObstacleMask) != null;
    }

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

    public Node NodeFromWorldPoint(Vector2 worldPosition)
    {
        if (grid == null || gridSizeX <= 0 || gridSizeY <= 0)
        {
            return null;
        }

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
        if (grid == null)
        {
            return;
        }

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
            if (n != null)
            {
                return n;
            }
        }
        return null;
    }

    Node FindWalkableInRadius(int centreX, int centreY, int radius)
    {
        for (int i = -radius; i <= radius; i++)
        {
            int verticalSearchX = i + centreX;
            int horizontalSearchY = i + centreY;

            // Top
            if (InBounds(verticalSearchX, centreY + radius))
            {
                if (grid[verticalSearchX, centreY + radius].walkable)
                {
                    return grid[verticalSearchX, centreY + radius];
                }
            }

            // Bottom
            if (InBounds(verticalSearchX, centreY - radius))
            {
                if (grid[verticalSearchX, centreY - radius].walkable)
                {
                    return grid[verticalSearchX, centreY - radius];
                }
            }

            // Right
            if (InBounds(centreX + radius, horizontalSearchY))
            {
                if (grid[centreX + radius, horizontalSearchY].walkable)
                {
                    return grid[centreX + radius, horizontalSearchY];
                }
            }

            // Left
            if (InBounds(centreX - radius, horizontalSearchY))
            {
                if (grid[centreX - radius, horizontalSearchY].walkable)
                {
                    return grid[centreX - radius, horizontalSearchY];
                }
            }

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
                {
                    Gizmos.color = Color.red;
                }
                else
                {
                    Gizmos.color = displayTerrainGizmos ? GetTerrainColor(n.terrainType) : Color.white;
                }

                Gizmos.DrawCube(n.worldPosition, Vector3.one * (nodeDiameter - 0.1f));
            }
        }

        if (displayPathGizmos && lastWorldPath != null && lastWorldPath.Length > 1)
        {
            Gizmos.color = Color.yellow;
            for (int i = 0; i < lastWorldPath.Length - 1; i++)
            {
                Gizmos.DrawLine(lastWorldPath[i], lastWorldPath[i + 1]);
            }
        }
    }

    private Node.TerrainType GetTerrainTypeAtPoint(Vector2 worldPoint)
    {
        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, mudMask) != null)
        {
            return Node.TerrainType.Mud;
        }

        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, waterMask) != null)
        {
            return Node.TerrainType.Water;
        }

        if (Physics2D.OverlapCircle(worldPoint, overlapCircleRadius, grassMask) != null)
        {
            return Node.TerrainType.Grass;
        }

        return Node.TerrainType.Normal;
    }

    private float GetTerrainCost(Node.TerrainType terrainType)
    {
        switch (terrainType)
        {
            case Node.TerrainType.Mud:
                return mudCost;
            case Node.TerrainType.Water:
                return waterCost;
            case Node.TerrainType.Grass:
                return grassCost;
            default:
                return normalCost;
        }
    }

    private Color GetTerrainColor(Node.TerrainType terrainType)
    {
        switch (terrainType)
        {
            case Node.TerrainType.Mud:
                return mudColor;
            case Node.TerrainType.Water:
                return waterColor;
            case Node.TerrainType.Grass:
                return grassColor;
            default:
                return normalColor;
        }
    }
}

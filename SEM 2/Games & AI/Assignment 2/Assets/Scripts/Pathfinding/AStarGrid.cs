using System.Collections.Generic;
using UnityEngine;

public class AStarGrid : MonoBehaviour
{
    [Header("Gizmo/Debug Visualization")]
    public bool showGridGizmos = true;
    public bool showTerrainGizmos = true;
    public bool showPathGizmos = true;
    // Stores the last computed path for visualization
    [HideInInspector]
    public List<Vector2> lastPath;
    // Terrain types and costs
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
    // Assign terrain by layer mask
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

    private Node[,] grid;
    private float nodeDiameter;
    private int gridSizeX, gridSizeY;
    private Vector2 worldBottomLeft;

    private void Awake()
    {
        CreateGrid();
    }

    public void CreateGrid()
    {
        nodeDiameter = nodeRadius * 2f;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
        grid = new Node[gridSizeX, gridSizeY];
        worldBottomLeft = (Vector2)transform.position - Vector2.right * (gridWorldSize.x / 2f) - Vector2.up * (gridWorldSize.y / 2f);

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
    }

    public List<Vector2> FindPath(Vector2 startWorldPos, Vector2 targetWorldPos, HeuristicType? heuristicOverride = null, bool smoothPath = true, bool recordForGizmos = false)
    {
        if (grid == null) CreateGrid();

        Node startNode = NodeFromWorldPoint(startWorldPos);
        Node targetNode = NodeFromWorldPoint(targetWorldPos);

        if (startNode == null || targetNode == null)
            return null;

        HeuristicType heuristic = heuristicOverride ?? heuristicType;

        List<Node> openSet = new List<Node>();
        HashSet<Node> closedSet = new HashSet<Node>();
        startNode.gCost = 0;
        startNode.hCost = GetHeuristic(startNode, targetNode, heuristic);
        openSet.Add(startNode);

        while (openSet.Count > 0)
        {
            Node currentNode = openSet[0];
            for (int i = 1; i < openSet.Count; i++)
            {
                if (openSet[i].fCost < currentNode.fCost || (Mathf.Approximately(openSet[i].fCost, currentNode.fCost) && openSet[i].hCost < currentNode.hCost))
                {
                    currentNode = openSet[i];
                }
            }

            openSet.Remove(currentNode);
            closedSet.Add(currentNode);

            if (currentNode == targetNode)
            {
                var rawPath = RetracePath(startNode, targetNode);
                var result = smoothPath ? SmoothPath(rawPath) : rawPath;
                if (recordForGizmos)
                    lastPath = result;
                return result;
            }

            foreach (Node neighbour in GetNeighbours(currentNode))
            {
                if (!neighbour.walkable || closedSet.Contains(neighbour))
                    continue;

                // Add terrain movement cost
                float tentativeG = currentNode.gCost + Vector2.Distance(currentNode.worldPosition, neighbour.worldPosition) * neighbour.movementCost;
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

    // Path smoothing: removes unnecessary waypoints if line of sight is clear
    private List<Vector2> SmoothPath(List<Vector2> path)
    {
        if (path == null || path.Count < 3) return path;
        List<Vector2> smoothed = new List<Vector2>();
        int i = 0;
        while (i < path.Count)
        {
            smoothed.Add(path[i]);
            int next = i + 1;
            for (int j = path.Count - 1; j > next; j--)
            {
                if (HasLineOfSight(path[i], path[j]))
                {
                    next = j;
                    break;
                }
            }
            i = next;
        }
        // Always add the last point if not already
        if (smoothed[smoothed.Count - 1] != path[path.Count - 1])
            smoothed.Add(path[path.Count - 1]);
        return smoothed;
    }

    // Uses Physics2D.Linecast to check for obstacles
    private bool HasLineOfSight(Vector2 a, Vector2 b)
    {
        return !Physics2D.Linecast(a, b, obstacleMask);
    }

    private List<Vector2> RetracePath(Node startNode, Node endNode)
    {
        List<Vector2> path = new List<Vector2>();
        Node current = endNode;
        while (current != startNode)
        {
            path.Add(current.worldPosition);
            current = current.parent;
            if (current == null) break;
        }
        path.Reverse();
        return path;
    }

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

    // Stub for ClosestWalkableNode for compatibility
    public Node ClosestWalkableNode(Node node)
    {
        // Not implemented, return input for now
        return node;
    }

    // Stub for MaxSize property for compatibility
    public int MaxSize
    {
        get { return (grid != null) ? grid.GetLength(0) * grid.GetLength(1) : 0; }
    }

    private List<Node> GetNeighbours(Node node)
    {
        List<Node> neighbours = new List<Node>();

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0)
                    continue;

                if (!allowDiagonal && Mathf.Abs(x) + Mathf.Abs(y) == 2)
                    continue;

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

    private void OnDrawGizmos()
    {
        if (showGridGizmos)
        {
            Gizmos.color = Color.gray;
            Gizmos.DrawWireCube(transform.position, new Vector3(gridWorldSize.x, gridWorldSize.y, 1f));
        }
        if (grid != null)
        {
            if (showTerrainGizmos)
            {
                foreach (Node n in grid)
                {
                    if (!n.walkable)
                    {
                        Gizmos.color = Color.red;
                    }
                    else
                    {
                        // Color by terrain type
                        Gizmos.color = GetTerrainColor(n.terrainType);
                    }
                    Gizmos.DrawCube(n.worldPosition, Vector3.one * (nodeRadius * 1.8f));
                }
            }
            if (showPathGizmos && lastPath != null && lastPath.Count > 1)
            {
                Gizmos.color = Color.yellow;
                for (int i = 0; i < lastPath.Count - 1; i++)
                {
                    Gizmos.DrawLine(lastPath[i], lastPath[i + 1]);
                    Gizmos.DrawSphere(lastPath[i], nodeRadius * 0.7f);
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
            // Lower fCost = higher priority
            return -compare;
        }

        public Node(bool walkable, Vector2 worldPos, int x, int y, TerrainType terrainType = TerrainType.Normal, float movementCost = 1f)
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

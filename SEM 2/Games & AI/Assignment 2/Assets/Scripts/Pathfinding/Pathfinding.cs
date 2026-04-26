// Adapted from: https://github.com/SebLague/Pathfinding-2D

using UnityEngine;
using System.Collections.Generic;
using System;

public class Pathfinding : MonoBehaviour
{
    public static AStarGrid grid;
    static bool warnedNoGrid;



    // This is used instead of Start() so that the
    // A* grid is only greated once when the game is launched
    void Awake()
    {
        grid = GetComponent<AStarGrid>();
    }

    // Public callable method
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
        {
            grid = UnityEngine.Object.FindFirstObjectByType<AStarGrid>();
        }

        if (grid != null)
        {
            warnedNoGrid = false;
        }
    }


    // Internal private implementation
    static Node[] FindPath(Vector2 from, Vector2 to)
    {
        // A* Waypoints to return
        Node[] waypoints = new Node[0];

        if (grid == null)
        {
            return waypoints;
        }

        grid.ResetSearchData();

        // Set to true if a path is found
        bool pathSuccess = false;

        // Starting node point - selected from the A* Grid
        Node startNode = grid.NodeFromWorldPoint(from);

        // Goal node point - selected from the A* Grid
        Node targetNode = grid.NodeFromWorldPoint(to);

        if (startNode == null || targetNode == null)
        {
            return waypoints;
        }

        // Ensure the starting node's parent is not null
        // Also let's us detect the start node if needed
        startNode.parent = startNode;

        // Niceity check to ensure the start and target nodes are walkable
        // by the frog (such as if you clock on a object)
        // If not, we find the closest walkable point in the grid
        if (!startNode.walkable)
        {
            startNode = grid.ClosestWalkableNode(startNode);
        }
        if (!targetNode.walkable)
        {
            targetNode = grid.ClosestWalkableNode(targetNode);
        }

        if (startNode == null || targetNode == null)
        {
            return waypoints;
        }

        if (startNode.walkable && targetNode.walkable)
        {
            // A* Starts here!!!
            // TODO: Your job is to fill in the missing code below the marked comments

            // Track the open set of nodes to explore, as a heap sorted by the A* Cost
            Heap<Node> openSet = new Heap<Node>(grid.MaxSize);

            // Track closed set of all visited nodes
            HashSet<Node> closedSet = new HashSet<Node>();

            startNode.gCost = 0f;
            startNode.hCost = Heuristic(startNode, targetNode);
            startNode.parent = startNode;

            // TODO: Commence A* by adding the start node to the open set
            openSet.Add(startNode);
            

            // Stop if we have a path or run out of nodes to explore (means no path can be found!)
            while (!pathSuccess && openSet.Count > 0)
            {
                // TODO: Get the node with the lowest F cost from the open set
                //     and add it to the closed set
                Node currentNode = openSet.RemoveFirst();
                closedSet.Add(currentNode);
                

                // TODO: If we have reached the target node, we have found a path! (repalce false)
                if (currentNode == targetNode)
                {
                    pathSuccess = true;
                }
                else
                {
                    // TODO: Otherwise, explore the neighbours of the current node
                    //       You'll need to get all of the neighbours of the current node
                    //       and then loop through them to find the best path
                    List<Node> neighbours = grid.GetNeighbours(currentNode);
                    foreach (Node node in neighbours)
                    {
                        // Skip nodes that are statically blocked, already visited, or blocked by a moving obstacle.
                        if (node.walkable && !closedSet.Contains(node) && !grid.IsPointBlockedByDynamicObstacle(node.worldPosition))
                        {
                            // TODO: Calculate the G Cost of the neighbour node
                            float newCostToNeighbour = currentNode.gCost + GCost(currentNode, node);


                            // TOSO: If the neighbour is not in the open set OR
                            //    the neighour was previously checked and the new G Cost is less than the previous G Cost 
                            //    (repalce false)
                            if (!openSet.Contains(node) || newCostToNeighbour < node.gCost)
                            {
                                // TODO: Set neightbour G Cost
                                node.gCost = newCostToNeighbour;
                                

                                // TODO: Compute and set the H Cost for the neighbour
                                node.hCost = Heuristic(node, targetNode);
                                

                                // TODO: Set the parent of the neighbour to the current node
                                node.parent = currentNode;
                                

                                // TODO: Add neighbour to the open set, but need to check if the neighbour is already in the open set
                                // If not in the open set, then add to the heap
                                // If in the open set, then UDPATE the neighbour in the heap
                                if (!openSet.Contains(node))
                                {
                                    // TODO: (see above comment)
                                    openSet.Add(node);
                                }
                                else
                                {
                                    // TODO: (see above comment)
                                    openSet.UpdateItem(node);
                                }
                            }
                        }
                    }
                }
            }
        }

        // If we have a path, then actually get the path from the start to goal
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
    }

    // Creates the actual A* Path from the start to the goal
    // TODO: Your job is to fill in the missing code below the marked comments
    static Node[] RetracePath(Node startNode, Node endNode)
    {
        // Store the computed path
        List<Node> path = new List<Node>();

        // TODO: Commence retracing the path from the end node
        Node currentNode = endNode;
        

        // TODO: Loop while the current node isn't the start node (replace false)
        while (currentNode != startNode)
        {
            // TODO: Add the current node to the path
            path.Add(currentNode);
            

            // TODO: Set the current node to the parent of the current node
            currentNode = currentNode.parent;
            if (currentNode == null)
            {
                break;
            }
            
        }

        // Convert this list to an array and reverse it
        Node[] waypoints = path.ToArray();
        Array.Reverse(waypoints);
        return waypoints;
    }

    static float GCost(Node nodeA, Node nodeB)
    {
        return grid.GetStepCost(nodeA, nodeB);
    }


    static float Heuristic(Node nodeA, Node nodeB)
    {
        return grid.GetHeuristicDistance(nodeA, nodeB);
    }

    static Node[] SmoothPath(Node[] originalPath)
    {
        if (originalPath == null || originalPath.Length < 3)
        {
            return originalPath;
        }

        List<Node> smoothedPath = new List<Node>();
        int currentIndex = 0;
        smoothedPath.Add(originalPath[currentIndex]);

        while (currentIndex < originalPath.Length - 1)
        {
            int furthestVisible = currentIndex + 1;

            for (int candidate = originalPath.Length - 1; candidate > currentIndex; candidate--)
            {
                if (grid.IsPathSegmentClear(originalPath[currentIndex].worldPosition, originalPath[candidate].worldPosition))
                {
                    furthestVisible = candidate;
                    break;
                }
            }

            if (furthestVisible == currentIndex)
            {
                break;
            }

            currentIndex = furthestVisible;
            smoothedPath.Add(originalPath[currentIndex]);
        }

        return smoothedPath.ToArray();
    }
}

# Frog Game AI & A* Pathfinding Validation Guide

This guide helps you validate all implemented features for the Frog AI assignment in Unity. Follow these steps to confirm everything works as expected.

---

## 1. Scene & Object Setup
- Open your main Frog scene in Unity.
- Ensure the following objects exist:
  - **Frog** (with Frog.cs attached)
  - **AStarGrid** (with AStarGrid.cs attached)
  - Terrain and obstacle GameObjects (with correct layers for Mud, Water, Grass, Obstacles)

---

## 2. Inspector Checks
- Select the **AStarGrid** object.
- In the Inspector, confirm these toggles are visible and enabled:
  - `showGridGizmos`
  - `showTerrainGizmos`
  - `showPathGizmos`
- Adjust `gridWorldSize` and `nodeRadius` if the grid is not visible or too small/large.

---

## 3. Scene View Gizmos
- Make sure the **Gizmos** button is enabled in the Scene view toolbar.
- You should see:
  - A wireframe grid (gray)
  - Terrain cells colored by type (white, green, blue, brown)
  - Obstacles (red cells)
  - Path lines and waypoints (yellow) after a path is computed

---

## 4. Pathfinding & Movement
- Enter Play mode.
- Right-click (or use the assigned input) to set a target for the Frog.
- The Frog should:
  - Compute a path around obstacles
  - Move along the path, following waypoints
  - Stop at the target

---

## 5. Heuristic Toggle
- In the Inspector, change the AStarGrid’s `heuristicType` (Euclidean, Manhattan, Octile).
- Set a new target for the Frog and observe the path shape changes.

---

## 6. Terrain Costs
- Place different terrain types (Mud, Water, Grass) in the scene.
- Set a target across various terrains.
- The Frog should prefer lower-cost terrain and avoid high-cost terrain when possible.
- Terrain cells should be colored according to their type.

---

## 7. Path Smoothing
- Set a target with a clear line of sight.
- The path should be smoothed (fewer waypoints, straight lines where possible).

---

## 8. Dynamic Obstacles
- Move or add obstacles during Play mode.
- Set a new target for the Frog.
- The path should update to avoid new obstacles.

---

## 9. Gizmo/UI Toggles
- While in Play mode, toggle the gizmo options in the Inspector.
- Confirm that grid, terrain, and path visualization appear/disappear as expected.

---

## 10. Error Checking
- Watch the Console for errors or warnings during all tests.

---

## 11. Demo Evidence (Optional)
- Take screenshots or record a short video showing:
  - Pathfinding around obstacles
  - Terrain cost avoidance
  - Gizmo toggles in action
  - Heuristic/path smoothing differences

---

If all steps work as described, your implementation is correct and ready for submission!

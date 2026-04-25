# Frog Game AI & AStarGrid Setup – Chat History Reference

## Summary
This file contains a step-by-step record of the chat guidance for setting up the AStarGrid and terrain layers in Unity for the Frog Game AI assignment.

---

### 1. Initial Issue
- User could not see the AStarGrid object in the Unity scene.
- Solution: Create an empty GameObject named `AStarGrid` and attach the `AStarGrid.cs` script.

### 2. Inspector & Gizmo Setup
- Enable `showGridGizmos`, `showTerrainGizmos`, and `showPathGizmos` in the Inspector.
- Adjust grid size and node radius as needed.

### 3. Layer Masks – What & Why
- Layers are used to group GameObjects for logic like pathfinding.
- Create layers: Mud, Water, Grass, Obstacle.
- Assign these layers to the appropriate GameObjects (e.g., mud tiles → Mud).
- Set the corresponding Layer Masks in the AStarGrid Inspector.

### 4. How to Create and Assign Layers
- Go to Inspector > Layer dropdown > Add Layer…
- Add: Mud, Water, Grass, Obstacle.
- Select a GameObject, use the Layer dropdown to assign the correct layer.
- Apply to children if prompted.

### 5. What If You Don’t Have All Terrain Types?
- Only assign layers and masks for the terrain types present in your scene.
- If you don’t have water or grass, leave those masks as “Nothing.”

### 6. Confirmation
- User correctly assigned the Mud layer to MudPatch GameObjects.
- Repeat for other terrain/obstacle types as needed.

### 7. Next Steps
- Assign all relevant GameObjects to their correct layers.
- Set Layer Masks in AStarGrid Inspector.
- Test in Play mode and check for errors.

### 8. User Added Delays and Verified Grid
- User added delays to the relevant parts of the project (details not specified).
- User confirmed the grid is showing up in the Gizmos during Play mode.
- Next steps requested.

### 9. Issue: Frog Gets Stuck on Obstacles
- User reports that when clicking behind or along an obstacle, the Frog gets stuck and does not move around the obstacle.
- The Frog does not avoid obstacles as expected; it appears to get stuck instead of pathfinding around them.
- User is unsure of the cause and requests troubleshooting help.

### 10. Issue: Obstacle Mask Not Visible in Inspector
- User reports that the "Obstacle Mask" field is not visible in the AStarGrid Inspector.
- Troubleshooting steps provided:
  - Confirm `public LayerMask obstacleMask;` exists in AStarGrid.cs.
  - Save the script and let Unity recompile.
  - Ensure the script is attached to the AStarGrid GameObject.
  - Reset the component if needed.
  - Field must be public or marked with [SerializeField].
- User asked if this troubleshooting was saved in the README.

---

**This README documents the full chat-based setup process for future reference.**

using UnityEngine;
using Globals;
using UnityEngine.InputSystem;


public class Frog : MonoBehaviour
{
    // References to various objects in the scene that we want to be able to modify.
    private Transform _flag;
    private SpriteRenderer _flagSr;
    private Animator _animator;
    private Rigidbody2D _rb;

    private InputAction ClickMoveAction;
    // Stores the last position that the player right-clicked. Initially null.
    private Vector2? _lastClickPos;

    // For pathfinding
    private Node[] path;

    void Start()
    {
        // Initialise the various object references.
        _flag = GameObject.Find("Flag").transform;
        _flagSr = _flag.GetComponent<SpriteRenderer>();
        _flagSr.enabled = false;

        _animator = GetComponent<Animator>();

        _rb = GetComponent<Rigidbody2D>();

        ClickMoveAction = InputSystem.actions.FindAction("Attack");
        _lastClickPos = null;
        path = new Node[0];
    }

    void Update()
    {

        // Check whether the player right-clicked (mouse button #1).
        if (ClickMoveAction.WasPressedThisFrame())
        {
            Vector2 mousePos = Mouse.current.position.ReadValue();
            _lastClickPos = Camera.main.ScreenToWorldPoint(mousePos);
            _flag.position = (Vector2)_lastClickPos + new Vector2(0.55f, 0.55f);
            _flagSr.enabled = true;

            path = Pathfinding.RequestPath(transform.position, (Vector2)_lastClickPos);
            Debug.Log("Path length: " + path.Length);

            // Change the world position of the final path node to the actual clicked position,
            // since the centre of the final node might be off somewhat.
            if (path.Length > 0)
            {
                Node fixedFinalNode = path[path.Length - 1].Clone();
                fixedFinalNode.worldPosition = (Vector2)_lastClickPos;
                path[path.Length - 1] = fixedFinalNode;
            }
        }
    }

    void FixedUpdate()
    {
        // If the last-clicked position is non-null, move there. Otherwise do nothing.
        if (_lastClickPos != null)
        {
            // Draw the path found by the A* algorithm.
            if (path.Length > 0)
            {
                for (int i = 1; i < path.Length; i++)
                {
                    Debug.DrawLine(path[i - 1].worldPosition, path[i].worldPosition, Color.black);
                }
            }
        }

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

}

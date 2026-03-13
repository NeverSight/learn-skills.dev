---
name: unity-so-prefab-manager
description: "Manages the structured relationship between ScriptableObjects (Data) and Prefabs (Logic/Visuals) in Unity 6. Follows the 'SO-to-Mono' Bridge pattern to ensure instance independence (e.g., individual health for identical robots) while maintaining a clean, data-driven architecture. Use when: (1) Creating new unit/item types, (2) Wiring SO data to Prefab MonoBehaviours, (3) Resolving data-sharing bugs where changing one SO affects all instances."

---

# Unity SO-Prefab Manager

This skill enforces a strictly modular "Bridge" pattern between Data and Logic.

## Core Workflow: The Bridge Pattern

To ensure that multiple instances of the same unit (e.g., 4 Robots) can have independent runtime values (Health, Energy) while sharing the same Template (RobotSO), follow these steps:

### 1. Structure the ScriptableObject (The Template)
The SO should contain **Static/Read-Only** data that defines the "Ideal" version of the object.
- Example: `maxHealth`, `baseSpeed`, `displayName`.

### 2. Structure the MonoBehaviour (The Instance)
The script on the Prefab should contain **Runtime/Mutable** data and a reference to the SO.
- Example: `currentHealth`, `activeBuffs`.

### 3. Initialize the Bridge
Use `Awake()` to copy values from the SO to the local instance variables.

```csharp
[Header("Data Reference")]
[SerializeField] private RobotSO data;

[Header("Runtime State")]
private float currentHealth;

private void Awake() {
    if (data == null) {
        Debug.LogError($"[System] Fail: Missing SO data on {gameObject.name}");
        return;
    }
    // Initialize independent state
    currentHealth = data.MaxHealth;
    
    Debug.Log($"[{data.name}] Success: Initialized instance | Health: {currentHealth}");
}
```

## Advanced Usage

### 1. File Creation: API-First vs. YAML Power-Mode

#### **Standard (1-10 Files) - Use Unity API**
For most tasks, use `mcp_unityMCP_manage_scriptable_object`. This is the **healthiest** method as it ensures GUID integrity and immediate `.meta` file availability.
- **Workflow:** `Call manage_scriptable_object` -> `Apply Patches`.

#### **Performance (10+ Files) - Use YAML Generation**
For massive data dumps (e.g., importing 50 items), bypass the API latency by writing files directly.
- **Workflow:** 
    1. Create a YAML template based on an existing `.asset` file.
    2. Write `.asset` files directly to `Assets/Data/` via `write_to_file`.
    3. Call `mcp_unityMCP_refresh_unity(scope="assets")` to force Unity to generate `.meta` files.

### 2. Surgical YAML (Deep Debugging)
Use direct file reading/parsing for "Deep Audits" that the API can't quickly handle:
- **GUID Verification:** Search for a specific `m_Script: {fileID: ..., guid: ...}` in prefabs to find which scripts are actually attached.
- **Reference Repair:** Use `grep_search` and `replace_file_content` project-wide to swap broken GUIDs without opening the Editor for every file.

## Reference Material
- See [references/bridge-pattern.md](references/bridge-pattern.md) for detailed implementation details and troubleshooting.
- See [references/naming-conventions.md](references/naming-conventions.md) for the project-standard folder structure.
- See [references/yaml-templates.md](references/yaml-templates.md) for standard Unity YAML boilerplate.

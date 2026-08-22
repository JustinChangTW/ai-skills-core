# Blender Control Operation Playbook

## 1. Environment Probe

Before generating or running Blender actions, classify the execution route:

- `mcp-live`: a Blender MCP tool is available and can inspect or mutate the current scene.
- `toolkit-live`: a Blender Toolkit or WebSocket wrapper is available.
- `script-only`: no live tool is available; return Blender Python that the user can run.
- `blocked`: the user asks for a live operation, but Blender/addon/path state is unknown.

Required checks:

- Blender version, when available.
- MCP/addon connection status, when available.
- Current scene inventory before destructive edits.
- Intended output path before export or render.
- Whether the operation writes files, downloads assets, uses credentials, clears scene data, or starts a long render.

## 2. Intent Categories

Use one primary category per turn:

- `scene-inspection`: list objects, materials, cameras, lights, collections, dimensions, units, render settings.
- `parametric-modeling`: create or modify primitives, containers, lids, holes, ribs, threads, bevels, arrays.
- `material-modifier`: create/assign material, set PBR properties, add modifiers, apply or keep non-destructive stack.
- `camera-render`: configure camera, turntable, slow zoom, dolly, crane shot, transparent background, image sequence.
- `export-handoff`: export STL, OBJ, FBX, glTF, or prepare handoff for Three.js/3D printing.
- `troubleshooting`: diagnose connection, addon, port, timeout, context/active object, version API issues.

## 3. Parameter Rules

- Ask for missing dimensions when geometry depends on exact size.
- Keep the user's unit system explicit. Use millimeters for product/industrial parts only when requested or strongly implied.
- Do not guess object names. Inspect the scene or ask the user.
- Use a dedicated collection for generated objects when preserving the current scene.
- Prefer non-destructive modifiers until the user asks to apply geometry.
- For 3D printing or manufacturing, flag that mesh validity, tolerances, materials, and engineering review are not verified by this skill.

## 4. Blender Python Rules

Generated scripts must:

- Import only required standard Blender modules such as `bpy`, `math`, `os`, and `mathutils`.
- Avoid relying on `bpy.context.active_object` after multi-step operations unless the script just created the object.
- Resolve objects by explicit name and fail with a readable error when absent.
- Create output directories before writing files.
- Use object, material, and collection names that are stable and human-readable.
- Return or print a compact summary of created objects, output paths, and settings.

Generated scripts must not:

- Clear the whole scene unless the user has confirmed it.
- Delete existing objects by broad pattern without confirmation.
- Download remote assets or call paid APIs without confirmation.
- Hide failures behind broad `except Exception: pass`.

## 5. Render And Animation Rules

For camera animation:

- First identify the target object or bounding box center.
- Use a target empty and a track-to constraint for camera stability.
- For transparent output, prefer PNG sequence with alpha, then encode separately when ffmpeg is available.
- Long renders require confirmation of output path, resolution, fps, duration, render engine, and expected frame count.
- If the MCP call may timeout during render, render frames to a known directory and poll/check files afterward.

## 6. Verification Checklist

Report at least one observable proof:

- Scene inventory: object names, types, dimensions, material names.
- Modifier stack: modifier names and important values.
- Camera/render: camera name, frame range, fps, resolution, transparent flag.
- Export/render files: absolute path and existence/size when available.
- Error state: exact error message and the next diagnostic step.

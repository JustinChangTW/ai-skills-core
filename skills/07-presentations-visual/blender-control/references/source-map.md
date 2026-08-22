# Source Map

Audit date: 2026-06-14

## yanlin-cheng/skill-blender-industrial

Repository: https://github.com/yanlin-cheng/skill-blender-industrial

Adopted:

- Industrial/product modeling categories: primitives, Boolean operations, bevel/chamfer, arrays, lip/groove, threads, ribs, materials, container body, lid assembly, OBJ/STL export.
- The idea that a Blender skill often generates Blender Python and sends it through BlenderMCP rather than acting as a standalone program.
- The need to handle MCP connection failure and Blender installation/addon readiness.

Not adopted:

- The old single-line frontmatter and `triggerKeywords` shape, because this repo validates YAML frontmatter plus semantic blocks.
- The dependency on `skill-dev-driver`, because this skill must work as a portable Agent Skill with local handoff rules.
- Any claim that generated geometry is manufacturing-ready without external engineering validation.

## kevinbadi/blender-skills

Repository: https://github.com/kevinbadi/blender-skills

Adopted:

- Separation between model generation, camera animation, product polish, and automation/toolkit tasks.
- Installation and connection checks before using Blender automation.
- Camera animation concepts such as turntable, slow zoom, dolly/rotate, crane reveal, transparent background, frame sequence, and ffmpeg post-encoding.
- The safety principle that scripts/wrappers should be used as tools and not fully loaded into context unless necessary.

Not adopted:

- A hard dependency on a specific WebSocket wrapper, port range, project config path, Meshy API, Mixamo workflow, or Blender 5.x.
- Default render output locations from that repo; this skill asks for or reports explicit paths.

## BlenderMCP

Repository: https://github.com/ahujasid/blender-mcp

Adopted:

- BlenderMCP provides two-way communication between the assistant and Blender through an addon plus MCP server.
- Relevant capabilities include scene/object inspection, shape modification, material control, and arbitrary Blender Python execution.
- Arbitrary Python execution is powerful and requires caution, especially before destructive or file-writing actions.

Compatibility note:

- This skill treats BlenderMCP as an optional live execution route. When no live MCP tool is present, it returns Blender Python and validation steps instead of pretending execution occurred.

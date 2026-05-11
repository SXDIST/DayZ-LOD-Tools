# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DayZ LOD Tools** is a Blender 4.5+ addon that automates LOD (Level of Detail) generation for DayZ and Arma 3 modding. It integrates with the Arma 3 Object Builder addon to provide a streamlined workflow for creating multiple LOD types with correct naming conventions and properties.

## Architecture

The addon is organized into six modules:

- **[**init**.py](/__init__.py)**: Entry point that registers all classes and properties, sets up scene-level property groups, and registers a post-load handler to ensure default properties exist on scene load.

- **[properties.py](/properties.py)**: Defines all Blender `PropertyGroup` classes that store settings and LOD configuration:
  - `A3OBE_PG_NamedProperty`: Generic property name/value pair with autocomplete integration for Arma 3 Object Builder
  - `A3OBE_PG_ResolutionLODs`: Resolution LOD settings (prefix, LOD start level, decimation presets/values)
  - `A3OBE_PG_GeometryLOD`: Geometry LOD settings (type: box or empty, name)
  - `A3OBE_PG_MemoryLOD`: Memory LOD settings (toggle flags for invview, bounding box, radius, center points)
  - `A3OBE_PG_FireGeometryLOD`: Fire Geometry LOD settings (quality slider 1–10)
  - `A3OBE_PG_ViewGeometryLOD`: View Geometry LOD settings (name)
  - All support custom named properties for game-specific flags

- **[panel.py](/panel.py)**: Single UI panel (`A3OBE_PT_AutoLOD`) displayed in the 3D Viewport under the "Object Builder" tab. Renders toggles and settings for each LOD type in collapsible sections.

- **[operators.py](/operators.py)**: Implements user-facing operators:
  - `A3OBE_OT_GenerateLODs`: Main button that orchestrates LOD generation by calling the appropriate `lod_generators` functions in order
  - One add/remove property operator per LOD type to manage custom named properties

- **[lod_generators.py](/lod_generators.py)**: Core generation logic with separate functions for each LOD type:
  - `generate_resolution_lods()`: Duplicates mesh, applies decimate modifiers, sets LOD properties
  - `generate_geometry_lod()`: Creates collision geometry (box or empty) with A3OB component detection
  - `generate_memory_lod()`: Creates vertex-based memory points (invview, bounding box, radius, center) with vertex groups
  - `generate_fire_geometry_lod()`: Creates convex hull, applies quality-based decimation, triangulates, sets fire LOD properties
  - `generate_view_geometry_lod()`: Creates bounding box for AI occlusion
  - Helper `run_a3ob_component_search()` invokes Arma 3 Object Builder's component detection operator

- **[utils.py](/utils.py)**: Shared utilities for collection and object management:
  - `get_or_create_collection()`, `get_or_create_subcollection()`: Collection hierarchy management
  - `organize_collections()`: Enforces collection order (Visuals → Geometries → Point Clouds) for game engine compatibility
  - `duplicate_object()`: Copies mesh and children while preserving hierarchy
  - `create_bounding_box()`: Calculates world-space bounds and creates cube
  - `add_named_property()`: Adds game-specific properties via A3OB's property system

## Key Workflows

**User Workflow**: Select object → Open panel (N-key, Object Builder tab) → Toggle desired LOD types → Adjust settings → Click "Generate LODs"

**Code Workflow**:

1. User toggles LOD type checkboxes in panel (sets `PropertyGroup.active` flags)
2. Clicks "Generate LODs" button → executes `A3OBE_OT_GenerateLODs.execute()`
3. Operator validates selection has A3OB properties, then calls each LOD generator in order
4. Generators create objects in appropriate collections, apply modifiers, set LOD/property values
5. `organize_collections()` enforces final collection order

**Data Persistence**: All settings are stored in `Scene.a3obe_*` property groups, persisting across Blender save/load. The post-load handler ensures default properties (e.g., `lodnoshadow=1` for resolution LODs) always exist.

## Important Implementation Details

**Collection Organization**: Visuals (resolution LODs), Geometries (collision, fire, view), and Point Clouds (memory) are kept in enforced order for game engine recognition.

**Memory Points**: Stored as vertices with vertex groups (e.g., "invview", "boundingbox_min"). Invview is offset 2.5m along local Y from object center; bounding box points use world-space corners; ce_radius duplicates boundingbox_max; ce_center uses local center.

**Fire Geometry**: Uses convex hull instead of bounding box for accurate hit geometry. Quality slider (1–10) maps to decimate ratio (0.1–1.0). Always triangulated to ensure no n-gons in physics mesh.

**LOD Property Mapping**: Each LOD type sets specific A3OB LOD values: Resolution=0+, Geometry=6, Memory=9, Fire=15, View=14. Game recognition depends on exact naming and LOD property values.

**Decimation Presets**: Three built-in presets (Tris, Quads, Custom) provide default ratios per LOD level. Custom allows per-level override.

**A3OB Integration**: The addon imports `Arma3ObjectBuilder.utilities.data` for property autocomplete and invokes `bpy.ops.a3ob.find_components()` after generating geometry LODs to auto-assign collision components.

## Development Notes

- No external build or test system; changes to `.py` files take effect on addon reload in Blender
- Requires Arma 3 Object Builder addon installed and enabled for full functionality (property autocomplete, component detection)
- All modifiers are applied immediately (non-destructive workflow not preserved)
- Object transforms (location, rotation, scale) are correctly handled in memory point calculations via `matrix_world`
- Named properties use A3OB's internal `properties` collection; ensure property names match game engine expectations

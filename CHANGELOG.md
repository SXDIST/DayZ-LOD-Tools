# Changelog

All notable changes to DayZ LOD Tools are documented here.

---

## [5.0.1] — 2026-05-12

### Added
- **Auto-update system** — compact "Check for updates" button at the top of the panel
  - Fetches `__init__.py` from the GitHub main branch and compares the `version` tuple
  - When an update is found, the row turns red/orange and shows the new version number
  - One-click install button downloads the main branch zip and installs it via Blender's addon installer
  - Reports "Restart Blender to apply it" after a successful install
  - State resets each session (`UNKNOWN` → `UP_TO_DATE` / `AVAILABLE` / `ERROR`)
- `updater.py` — new module with `check()`, `download_and_install()`, and `set_local_version()` helpers
- Operators `a3obe.check_for_updates` and `a3obe.install_update`

---

## [5.0.0]

### Added
- **View Pilot LOD** — new LOD type for first-person pilot/driver camera occlusion
  - `A3OBE_PG_ViewPilotLOD` property group with mesh type toggle and named properties
  - `generators/view_pilot.py` generator
  - UI section inside the Resolution LODs box with add/remove named property operators
  - Scene pointer property, registration and unregistration wired up in `__init__.py`
- **`build.py`** — packaging script to zip the addon for distribution
- **`AGENTS.md`** — guidance file for AI coding agents working in this repo
- Deferred init timer (`bpy.app.timers`) to ensure default scene properties are applied on startup
- Depsgraph update handler to apply default properties when new scenes are added

### Fixed
- Fire Geometry LOD: unified modifier application using evaluated depsgraph; added `_apply_modifiers` helper; fixed convex hull cleanup to delete faces then vertices in the correct order
- Geometry LOD: create a proper empty object when the geometry type is not mesh

---

## [4.0.0]

### Changed (Breaking — full codebase restructure)
- Split monolithic `lod_generators.py` into a `generators/` package:
  - `generators/resolution.py`
  - `generators/geometry.py`
  - `generators/memory.py`
  - `generators/fire_geometry.py`
  - `generators/view_geometry.py`
  - `generators/a3ob_bridge.py` (Arma 3 Object Builder integration)
- Moved `utils.py` into `core/utils.py`
- Moved `panel.py` into `ui/panel.py`
- Extracted all magic strings/values into `constants.py`
- Deduplicated 10 add/remove named property operators into 2 base classes (`_AddNamedPropertyBase`, `_RemoveNamedPropertyBase`)
- Added `'UNDO'` to all operators

### Fixed (Critical bugs)
- Replaced `bpy.ops.mesh.primitive_cube_add` with the data API to prevent active object mutation side-effects
- Replaced `bpy.ops` convex hull call with `bmesh` API to remove context dependency
- Wrapped `modifier_apply` in `context.temp_override` for correct context propagation
- Fixed bounding box calculation for rotated objects (now samples all 8 corners in world space)
- Fixed `invview` point offset to use world space instead of local space
- Fixed memory leaks in mesh creation routines
- Fixed `matrix_parent_inverse` not being set in `duplicate_object`

---

## [3.0.0]

### Added
- **Memory LOD** — vertex-based memory point generation
  - Standard points: `invview` (offset 2.5 m along local Y), bounding box corners (`boundingbox_min` / `boundingbox_max`), `ce_radius`, `ce_center`
  - Points stored as vertices in vertex groups
  - UI with expandable Standard Points section and named property list
- **Fire Geometry LOD** — convex hull-based hit geometry
  - Quality slider (1–10) maps to decimate ratio (0.1–1.0)
  - Always triangulated to prevent n-gons in physics mesh
  - UI with quality slider and named property list
- **View Geometry LOD** — bounding box for AI occlusion
  - Configurable LOD name
  - UI with name field and named property list
- Collection management system: Visuals → Geometries → Point Clouds order enforced for game engine recognition
- `organize_collections()` in `utils.py` to enforce collection order in the Outliner

### Changed
- Default Resolution LOD prefix changed to `'LOD '`
- Default Geometry LOD name changed to `'Geometry'`
- Removed Weapons Points properties (`bolt_axis`, `bullet_eject`, `eye_ads`) in favour of the generic named property system

---

## [2.0.0]

### Added
- Named property system for all LOD types — add/remove arbitrary game-engine properties (name + value) per LOD
- `A3OBE_PG_NamedProperty` property group with autocomplete integration via `Arma3ObjectBuilder.utilities.data`
- Named property add/remove operators for Resolution and Geometry LOD types
- `lodnoshadow=1` default named property auto-applied to Resolution LODs on scene load
- `autocenter=0` default named property auto-applied to Geometry LODs on scene load
- `on_scene_load` persistent handler to ensure defaults survive file open/reload
- Resolution LOD first-level toggle (`LOD0` / `LOD1`)
- Three decimation presets: Tris, Quads, Custom (per-level override)
- Geometry LOD type option: `box` or `empty`
- `bpy.ops.a3ob.find_components()` invoked automatically after Geometry LOD generation

### Changed
- Geometry LOD generation enabled by default

### Fixed
- Removed auto smooth settings that were incompatible with the current Blender API
- Improved child object duplication to preserve full hierarchy

---

## [1.0.0]

### Added
- Initial **Auto LODs Generator** Blender addon
- Panel in the 3D Viewport N-panel under the "Object Builder" tab
- **Resolution LODs** — duplicates the source mesh and applies Decimate modifiers (up to 4 levels)
  - Configurable LOD prefix
  - Three decimation presets with per-level ratio values
- **Geometry LOD** — creates collision geometry with A3OB component detection
- `A3OBE_OT_GenerateLODs` main operator
- `duplicate_object()` utility preserving mesh and child hierarchy
- `create_bounding_box()` utility for world-space bounds
- `add_named_property()` utility using A3OB's property system
- LOD property value mapping: Resolution = 0+, Geometry = 6, Memory = 9, Fire = 15, View = 14
- Settings stored in `Scene.a3obe_*` property groups, persisted across save/load

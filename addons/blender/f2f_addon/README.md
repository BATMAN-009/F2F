# F2F Blender Add-on

**Status**: Placeholder (scaffolded in Feature 01).
**Owner**: Feature 13 — Blender add-on (DCC hand-off).

This folder reserves the add-on slot. The real implementation arrives in
Feature 13, which will:

- Authenticate against the F2F API.
- List the user's projects/assets.
- Import generated meshes (with embedded Design Ledger metadata) directly
  into the active Blender scene.
- Support re-export back to F2F.

For now, `f2f_addon/__init__.py` provides a valid `bl_info` block and
empty `register()` / `unregister()` functions so Blender can load the
add-on without error.

## Manual install (dev)

```
# From repo root
blender --command extension install-file ./addons/blender/f2f_addon  # Blender 4.2+
```

Or zip `f2f_addon/` and drop it into Blender's add-on preferences panel.

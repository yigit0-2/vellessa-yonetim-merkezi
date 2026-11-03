import bpy, sys
from pathlib import Path
argv=sys.argv[sys.argv.index("--")+1:]
src=Path(argv[0]).resolve(); dst=Path(argv[1]).resolve()
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
if src.suffix.lower()==".obj":
    try: bpy.ops.wm.obj_import(filepath=str(src))
    except Exception: bpy.ops.import_scene.obj(filepath=str(src))
elif src.suffix.lower()==".ply": bpy.ops.wm.ply_import(filepath=str(src))
else: raise RuntimeError("Unsupported mesh: "+str(src))
# Keep source materials and UVs; do not reshape or smooth product geometry.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=str(dst), export_format="GLB", use_selection=True, export_materials="EXPORT")
print("Exported",dst)

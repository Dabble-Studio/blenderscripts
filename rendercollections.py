import bpy
import json
import sys
import os
import re
from pathlib import Path

# Set the device and feature set
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.feature_set = "SUPPORTED"

filename = Path(bpy.data.filepath)
filename = filename.stem
renderPath = bpy.path.abspath("//Renders\\")

print('Render path: ' + renderPath)

col_names = {"Container"}

found_col = 0

for vl in bpy.context.scene.view_layers:
    for l in vl.layer_collection.children:
        if not l.name in col_names:
            continue

        found_col = 1

        for c in l.children:
            current_col = c.name

            current_col_cleaned = re.sub('[^A-Za-z0-9]+', '_', current_col)

            for m in l.children:
                m.exclude = m.name != current_col

            for obj in bpy.data.objects:
                if obj.type != "CAMERA":
                    continue

                if obj.hide_render == True:
                    continue
                print('Rendering collection ' + current_col)
                print('Setting up camera "' + obj.name +'" ')
                bpy.context.scene.camera = obj
                bpy.context.scene.cycles.samples = 128
                bpy.context.scene.render.engine = 'CYCLES'
                #bpy.context.scene.render.resolution_percentage = 100

                bpy.context.scene.render.filepath = renderPath + "\\" + current_col_cleaned + "\\" + current_col_cleaned + "__" + obj.name
                print ("Rendering..")
                bpy.ops.render.render(animation=False, write_still=True)
                print ("Done..")

if found_col == 0:
    print('\nDid not find "Container" collection. Check your blend file')
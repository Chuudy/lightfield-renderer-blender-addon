############################################################################
#  This file is part of the 4D Light Field Benchmark.                      #
#                                                                          #
#  This work is licensed under the Creative Commons                        #
#  Attribution-NonCommercial-ShareAlike 4.0 International License.         #
#  To view a copy of this license,                                         #
#  visit http://creativecommons.org/licenses/by-nc-sa/4.0/.                #
#                                                                          #
#  Authors: Katrin Honauer & Ole Johannsen & Krzysztof Wolski              #
#  Contact: contact@lightfield-analysis.net                                #
#  Website: www.lightfield-analysis.net                                    #
#                                                                          #
#  This add-on is based upon work of Maximilian Diebold                    #
#                                                                          #
#  The 4D Light Field Benchmark was jointly created by the University of   #
#  Konstanz and the HCI at Heidelberg University. If you use any part of   #
#  the benchmark, please cite our paper "A dataset and evaluation          #
#  methodology for depth estimation on 4D light fields". Thanks!           #
#                                                                          #
#  @inproceedings{honauer2016benchmark,                                    #
#    title={A dataset and evaluation methodology for depth estimation on   #
#           4D light fields},                                              #
#    author={Honauer, Katrin and Johannsen, Ole and Kondermann, Daniel     #
#            and Goldluecke, Bastian},                                     #
#    booktitle={Asian Conference on Computer Vision},                      #
#    year={2016},                                                          #
#    organization={Springer}                                               #
#    }                                                                     #
#                                                                          #
############################################################################

import bpy
from bpy.props import *



class VIEW3D_PT_lightfield_setup(bpy.types.Panel):
    # bl_space_type = "VIEW_3D"
    # bl_context = "objectmode"
    # bl_label = "Light Field Renderer"
    # bl_space_type = "VIEW_3D"
    # bl_region_type = "UI"

    bl_idname = "VIEW3D_PT_lightfield_setup"
    bl_label = "LF Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LF"
    bl_context = "objectmode"

    def separator(self,context,layout):        
        col = layout.column(align=True)
        col.label(text="")


    def draw(self, context):
        LF = bpy.context.scene.LF
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Camera parameters:")
        col.prop(LF, "focal_length")
        col.prop(LF, "x_res")
        col.prop(LF, "y_res")
        col.prop(LF, "sensor_size")
        col.prop(LF, "fstop")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Camera grid parameters:")
        col.prop(LF, "camera_setup")
        if(LF.camera_setup == 'LF'):
            col.prop(LF, "num_cams_x")
            col.prop(LF, "num_cams_y")
            col.prop(LF, "baseline_mm")
        else:
            col.prop(LF, "ipd_mm")            
        col.prop(LF, "focus_dist")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Grid generation:")
        col.operator("scene.create_lightfield", text="Add Camera Grid")
        col.operator("scene.delete_lightfield", text="Delete Camera Grid")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Disparity Preview:")
        col.prop(LF, "frustum_mode")

        if(LF.frustum_mode == 'Distance'):
            col.prop(LF, "frustum_min_distance")
            col.prop(LF, "frustum_max_distance")
        if(LF.frustum_mode == 'Disparity'):
            col.prop(LF, "frustum_min_disp")
            col.prop(LF, "frustum_max_disp")

        if LF.frustum_is_hidden():
            col.operator("scene.show_frustum", text="Show Frustum", icon="HAND")
        else:
            col.operator("scene.hide_frustum", text="Hide Frustum", icon="HAND")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Output:")
        col.prop(LF, "tgt_dir")
        col.prop(LF, "color_map_format")
        col.prop(LF, "depth_map_format")
        # col.prop(LF, "depth_map_scale") ### not necessary now

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Animation:")
        col.prop(LF, "render_single_frame")
        if(LF.render_single_frame == False):
            col.prop(LF, "sequence_start")
            col.prop(LF, "sequence_end")
            col.prop(LF, "sequence_steps")
        # col.prop(LF, "save_depth_for_all_views")
        # col.prop(LF, "save_object_id_maps_for_all_views")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Rendering:")
        col.operator("scene.render_lightfield", text="Render Light Field", icon="HAND")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Meta information:")
        col.prop(LF, "show_meta")
        if(LF.show_meta == True):
            col.prop(LF, "scene")
            col.prop(LF, "category")
            col.prop(LF, "date")
            col.prop(LF, "version")
            col.prop(LF, "authors")
            col.prop(LF, "contact")

        self.separator(context,layout)
        col = layout.column(align=True)
        col.label(text="Save/load light field settings:")
        col.prop(LF, "path_config_file")
        col.operator("scene.load_lightfield", text="Load config file", icon="SCENE_DATA")
        col.operator("scene.save_lightfield", text="Save config file", icon="SCENE_DATA")

UI_CLASSES = [VIEW3D_PT_lightfield_setup]

def register():
    for cls in UI_CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")


def unregister():
    for cls in UI_CLASSES:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
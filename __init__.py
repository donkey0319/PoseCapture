bl_info = {
    "name": "PoseCapture",
    "author": "donkey0319",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Capture actions of video and convert to armature actions",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
import os
import sys

# if bpy.data.is_saved and bpy.data.filepath:
#     dir = os.path.dirname(bpy.data.filepath)
#     if dir not in sys.path:
#             sys.path.append(dir)

# import execute
# import imp
# imp.reload(execute)
# from execute import read_video_and_set_pose

from . execute_file import print_hello
from . execute_file import read_video_and_set_pose


# ==============================================================================

bl_info = {
    "name": "File Selector Add-on",
    "blender": (2, 80, 0),
    "category": "Object",
}

class OpenMP4File(bpy.types.Operator):
    """Click this button to select the mp4 video to import"""
    bl_idname = "object.open_mp4_file"
    bl_label = "Open MP4 File"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.mp4',
        options={'HIDDEN'}
    )

    def execute(self, context):
        context.scene.file_path = self.filepath
        read_video_and_set_pose(context.scene.file_path, context.scene.armature_selector)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ArmatureSelector(bpy.types.PropertyGroup):
    target_armature: bpy.props.PointerProperty(
        name="Target Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    shoulder_R: bpy.props.StringProperty(name="Shoulder R")
    shoulder_L: bpy.props.StringProperty(name="Shoulder L")
    upperarm_R: bpy.props.StringProperty(name="Upperarm R")
    upperarm_L: bpy.props.StringProperty(name="Upperarm L")
    forearm_R: bpy.props.StringProperty(name="Forearm R")
    forearm_L: bpy.props.StringProperty(name="Forearm L")
    hand_R: bpy.props.StringProperty(name="Hand R")
    hand_L: bpy.props.StringProperty(name="Hand L")
    thigh_R: bpy.props.StringProperty(name="Thigh R")
    thigh_L: bpy.props.StringProperty(name="Thigh L")
    shin_R: bpy.props.StringProperty(name="Shin R")
    shin_L: bpy.props.StringProperty(name="Shin L")
    foot_R: bpy.props.StringProperty(name="Foot R")
    foot_L: bpy.props.StringProperty(name="Foot L")
    
    pelvis: bpy.props.StringProperty(name="Pelvis")
    spine_0: bpy.props.StringProperty(name="Spine 0")
    spine_1: bpy.props.StringProperty(name="Spine 1")
    spine_2: bpy.props.StringProperty(name="Spine 2")
    
    neck: bpy.props.StringProperty(name="Neck")
    head: bpy.props.StringProperty(name="Head")


class FileSelectorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Pose Capture"
    bl_idname = "OBJECT_PT_file_selector"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout
        armature_selector = context.scene.armature_selector
        
        # layout.label(text="Selected Video: " + context.scene.file_path)           
        layout.prop(data = armature_selector, property="target_armature", text="Target Armature")
        
        if armature_selector.target_armature and armature_selector.target_armature.type == 'ARMATURE':
               
            layout.row().operator("object.open_mp4_file", text="Run on MP4 File")  
            # Ensure the armature data is accessible
            if armature_selector.target_armature.data:
                layout.label(text="Retarget Bones (from bottom to top: pelvis -> spine 0 -> spine 1 -> spine 2)")
                layout.prop_search(armature_selector, "shoulder_R", armature_selector.target_armature.data, "bones", text="Right Shoulder")
                layout.prop_search(armature_selector, "shoulder_L", armature_selector.target_armature.data, "bones", text="Left Shoulder")
                layout.prop_search(armature_selector, "upperarm_R", armature_selector.target_armature.data, "bones", text="Right Upperarm")
                layout.prop_search(armature_selector, "upperarm_L", armature_selector.target_armature.data, "bones", text="Left Upperarm")
                layout.prop_search(armature_selector, "forearm_R", armature_selector.target_armature.data, "bones", text="Right Forearm")
                layout.prop_search(armature_selector, "forearm_L", armature_selector.target_armature.data, "bones", text="Left Forearm")
                layout.prop_search(armature_selector, "hand_R", armature_selector.target_armature.data, "bones", text="Right Hand")
                layout.prop_search(armature_selector, "hand_L", armature_selector.target_armature.data, "bones", text="Left Hand")
                layout.prop_search(armature_selector, "thigh_R", armature_selector.target_armature.data, "bones", text="Right Thigh")
                layout.prop_search(armature_selector, "thigh_L", armature_selector.target_armature.data, "bones", text="Left Thigh")
                layout.prop_search(armature_selector, "shin_R", armature_selector.target_armature.data, "bones", text="Right Shin")
                layout.prop_search(armature_selector, "shin_L", armature_selector.target_armature.data, "bones", text="Left Shin")
                layout.prop_search(armature_selector, "foot_R", armature_selector.target_armature.data, "bones", text="Right Foot")
                layout.prop_search(armature_selector, "foot_L", armature_selector.target_armature.data, "bones", text="Left Foot")
                layout.prop_search(armature_selector, "pelvis", armature_selector.target_armature.data, "bones", text="Pelvis")
                layout.prop_search(armature_selector, "spine_0", armature_selector.target_armature.data, "bones", text="Spine 0")
                layout.prop_search(armature_selector, "spine_1", armature_selector.target_armature.data, "bones", text="Spine 1")
                layout.prop_search(armature_selector, "spine_2", armature_selector.target_armature.data, "bones", text="Spine 2")
                layout.prop_search(armature_selector, "neck", armature_selector.target_armature.data, "bones", text="Neck")
                layout.prop_search(armature_selector, "head", armature_selector.target_armature.data, "bones", text="Head")

def register():
    bpy.utils.register_class(FileSelectorPanel)
    bpy.types.Scene.file_path = bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    )
    bpy.utils.register_class(OpenMP4File)
    bpy.utils.register_class(ArmatureSelector)
    bpy.types.Scene.armature_selector = bpy.props.PointerProperty(type=ArmatureSelector)

def unregister():
    bpy.utils.unregister_class(FileSelectorPanel)
    bpy.utils.unregister_class(OpenMP4File)    
    bpy.utils.unregister_class(ArmatureSelector)
    del bpy.types.Scene.armature_selector
    del bpy.types.Scene.file_path

if __name__ == "__main__":
    register()


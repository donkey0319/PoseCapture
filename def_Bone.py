import numpy as np
import bpy
import math
import sys
import os
from mathutils import Quaternion, Vector, Matrix
from def_constants import *

class Bone:
    # constructor
    def __init__(self, bone_name, armature_name = "metarig"):
        self.bone_name = bone_name
        self.armature_name = armature_name
          
    def set_bone_align_to_world_vector(self, world_vector):
        # initialize bone rotation to 0
        bpy.ops.object.mode_set(mode='POSE')
        bone = bpy.context.object.pose.bones[self.bone_name]
        bone.rotation_quaternion = self.axis_angle_to_quaternion(np.array([1, 0, 0]), 0)
        # Update the scene to reflect the new bone alignment
        bpy.context.view_layer.update()
        
        # get y axis in pose space
        y_axis_world = bone.matrix.col[1].to_3d()
        
        # turn world_vector into pose_space
        armature = bpy.data.objects[self.armature_name]
        global_x_axis_vector = bone.matrix.col[0].to_3d()
        global_y_axis_vector = bone.matrix.col[1].to_3d()
        global_z_axis_vector = bone.matrix.col[2].to_3d()
        
        world_2_pose = np.array([global_x_axis_vector, global_y_axis_vector, global_z_axis_vector])
        
        world_vector = world_vector / np.linalg.norm(world_vector)
        cross_product = np.cross(y_axis_world, world_vector)
        # normalize cross_product
        cross_product = cross_product / np.linalg.norm(cross_product)
        dot_product = np.dot(y_axis_world, world_vector)
        degrees = np.degrees(np.arccos(dot_product))
        
        cross_product = world_2_pose @ cross_product
        
        bone.rotation_quaternion = self.axis_angle_to_quaternion(cross_product, degrees)
    
    def set_bone_rotation_around_pose_space_vector(self, pose_vector, degrees):
        bpy.ops.object.mode_set(mode='POSE')
        bone = bpy.context.object.pose.bones[self.bone_name]
        pose_vector = pose_vector / np.linalg.norm(pose_vector)
        bone.rotation_quaternion = self.axis_angle_to_quaternion(pose_vector, degrees)
    
    def set_bone_rotation_around_world_space_vector(self, world_vector, degrees):
        # initialize bone rotation to 0
        bpy.ops.object.mode_set(mode='POSE')
        bone = bpy.context.object.pose.bones[self.bone_name]
        bone.rotation_quaternion = self.axis_angle_to_quaternion(np.array([1, 0, 0]), 0)
        world_vector = world_vector / np.linalg.norm(world_vector)
        # Update the scene to reflect the new bone alignment
        bpy.context.view_layer.update()
        
         # turn world_vector into pose_space
        armature = bpy.data.objects[self.armature_name]
        global_x_axis_vector = bone.matrix.col[0].to_3d()
        global_y_axis_vector = bone.matrix.col[1].to_3d()
        global_z_axis_vector = bone.matrix.col[2].to_3d()        
        world_2_pose = np.array([global_x_axis_vector, global_y_axis_vector, global_z_axis_vector])
        
        pose_vector = world_2_pose @ world_vector
        bone.rotation_quaternion = self.axis_angle_to_quaternion(pose_vector, degrees)
    
    def get_y_axis_pose(self):
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select the armature by name
        armature = bpy.data.objects.get(self.armature_name)
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)

        # Switch to Pose mode
        bpy.ops.object.mode_set(mode='POSE')

        # Ensure the bone exists
        if self.bone_name in armature.data.bones:
            bone = armature.pose.bones[self.bone_name]
            bone_matrix = bone.matrix
            # Store the current rotation of the bone
            stored_rotation = bone.rotation_quaternion.copy()
            
            # Clear the bone's rotation
            bone.rotation_quaternion = (1, 0, 0, 0)
            
            # get y_axis
            global_y_axis_vector = armature.matrix_world @ bone_matrix.col[1].to_3d()
            
            # Restore the stored rotation
            bone.rotation_quaternion = stored_rotation
        
        return global_y_axis_vector

    def quaternion_to_axis_angle(self, q):
        w, x, y, z = q
        angle = 2 * math.acos(w)
        
        s = math.sqrt(1 - w**2)
        
        if s < 0.0001:
            x = 1
            y = 0
            z = 0
        else:
            x = x / s
            y = y / s
            z = z / s
        return [x, y, z], math.degrees(angle)

    def axis_angle_to_quaternion(self, axis, angle):
        axis = np.array(axis).astype(np.float64) / np.linalg.norm(axis)
        angle_rad = math.radians(angle)
        return Quaternion(axis, angle_rad)
    
    def insert_rotation_to_current_keyframe(self):
        bpy.ops.object.mode_set(mode='POSE')
        bone = bpy.context.object.pose.bones[self.bone_name]
        bpy.context.object.pose.bones[self.bone_name].keyframe_insert(data_path="rotation_quaternion", frame=bpy.context.scene.frame_current)
        bpy.context.object.pose.bones[self.bone_name].keyframe_insert(data_path="rotation_quaternion", frame=bpy.context.scene.frame_current)


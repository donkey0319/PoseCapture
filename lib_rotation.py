import bpy
import math
import sys
import os
import numpy as np
import json

# dir = os.path.dirname(bpy.data.filepath)
# if not dir in sys.path:
#     sys.path.append(dir)
# import def_Bone
# import def_constants
# import imp
# imp.reload(def_Bone)
# imp.reload(def_constants)
# from def_Bone import *
# from def_constants import *

from . import def_Bone
from . import def_constants


# ============================================= FUNCTIONS LIST HERE ========================================================

def convert_mediapipe_output_into_rotation_list(mediapipe_output):

    # Sanity Check
    if mediapipe_output.shape != (39, 5):
        print("mediapipe_output.shape: ", mediapipe_output.shape)
        raise ValueError("mediapipe_output.shape != (39, 5), Please check your video!")
        return

    mediapipe_output = np.array(mediapipe_output)
    mediapipe_xyz = mediapipe_output[:, 0:3]

    # change to blender orientation
    rotate_x = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
    for i in range(0, len(mediapipe_xyz)):
        mediapipe_xyz[i] = np.dot(rotate_x, mediapipe_xyz[i])
        
    mediapipe_xyz = np.array(mediapipe_xyz)
    
    # Mediapipe y-Offset    
    mediapipe_xyz[:, 1] *= 0.2
    
    # ============================================ LEFT LIMBS ===========================================================
    
    # Set up shoulder_L_rotation
    shoulder_L_rotation = mediapipe_xyz[def_constants.MP_ELBOW_L] - mediapipe_xyz[def_constants.MP_SHOULDER_L]
    shoulder_L_rotation = shoulder_L_rotation / np.linalg.norm(shoulder_L_rotation)

    # Set up elbow_L_rotation
    elbow_L_rotation = mediapipe_xyz[def_constants.MP_HAND_L] - mediapipe_xyz[def_constants.MP_ELBOW_L]
    elbow_L_rotation = elbow_L_rotation / np.linalg.norm(elbow_L_rotation)

    # Set up hand_L_rotation
    hand_L_midpoint = (mediapipe_xyz[def_constants.MP_FINGER1_L] + mediapipe_xyz[def_constants.MP_FINGER2_L]) / 2
    hand_L_rotation = hand_L_midpoint - mediapipe_xyz[def_constants.MP_HAND_L]
    hand_L_rotation = hand_L_rotation / np.linalg.norm(hand_L_rotation)

    # Set up hips_L_rotation
    hips_L_rotation = mediapipe_xyz[def_constants.MP_KNEES_L] - mediapipe_xyz[def_constants.MP_HIPS_L]
    hips_L_rotation = hips_L_rotation / np.linalg.norm(hips_L_rotation)

    # Set up knee_L_rotation
    knee_L_rotation = mediapipe_xyz[def_constants.MP_ANKLE_L] - mediapipe_xyz[def_constants.MP_KNEES_L]
    knee_L_rotation = knee_L_rotation / np.linalg.norm(knee_L_rotation)

    # Set up foot_L_rotation
    foot_L_rotation = mediapipe_xyz[def_constants.MP_TOE_L] - mediapipe_xyz[def_constants.MP_ANKLE_L]
    foot_L_rotation = foot_L_rotation / np.linalg.norm(foot_L_rotation)

    # ============================================ RIGHT LIMBS ===========================================================

    # Set up shoulder_L_rotation
    shoulder_R_rotation = mediapipe_xyz[def_constants.MP_ELBOW_R] - mediapipe_xyz[def_constants.MP_SHOULDER_R]
    shoulder_R_rotation = shoulder_R_rotation / np.linalg.norm(shoulder_R_rotation)

    # Set up elbow_L_rotation
    elbow_R_rotation = mediapipe_xyz[def_constants.MP_HAND_R] - mediapipe_xyz[def_constants.MP_ELBOW_R]
    elbow_R_rotation = elbow_R_rotation / np.linalg.norm(elbow_R_rotation)

    # Set up hand_L_rotation
    hand_R_midpoint = (mediapipe_xyz[def_constants.MP_FINGER1_R] + mediapipe_xyz[def_constants.MP_FINGER2_R]) / 2
    hand_R_rotation = hand_R_midpoint - mediapipe_xyz[def_constants.MP_HAND_R]
    hand_R_rotation = hand_R_rotation / np.linalg.norm(hand_R_rotation)

    # Set up hips_L_rotation
    hips_R_rotation = mediapipe_xyz[def_constants.MP_KNEES_R] - mediapipe_xyz[def_constants.MP_HIPS_R]
    hips_R_rotation = hips_R_rotation / np.linalg.norm(hips_R_rotation)

    # Set up knee_L_rotation
    knee_R_rotation = mediapipe_xyz[def_constants.MP_ANKLE_R] - mediapipe_xyz[def_constants.MP_KNEES_R]
    knee_R_rotation = knee_R_rotation / np.linalg.norm(knee_R_rotation)

    # Set up foot_L_rotation
    foot_R_rotation = mediapipe_xyz[def_constants.MP_TOE_R] - mediapipe_xyz[def_constants.MP_ANKLE_R]
    foot_R_rotation = foot_R_rotation / np.linalg.norm(foot_R_rotation)
    
    # ============================================ SPINE ===========================================================
    
    # Set up root_rotation (pelvis) 
    root_x_rotation = mediapipe_xyz[def_constants.MP_HIPS_L] - mediapipe_xyz[def_constants.MP_HIPS_R]
    root_x_rotation = root_x_rotation / np.linalg.norm(root_x_rotation)
    
    # chest bone
    chest_x_rotation = mediapipe_xyz[def_constants.MP_SHOULDER_L] - mediapipe_xyz[def_constants.MP_SHOULDER_R]
    chest_x_rotation = chest_x_rotation / np.linalg.norm(chest_x_rotation)
    
    # head bone
    head_x_rotation = mediapipe_xyz[def_constants.MP_HEAD_L] - mediapipe_xyz[def_constants.MP_HEAD_R]
    head_x_rotation = head_x_rotation / np.linalg.norm(head_x_rotation)
    
    eyebrow_midpoint = (mediapipe_xyz[def_constants.MP_HEAD_L] + mediapipe_xyz[def_constants.MP_HEAD_R]) / 2
    head_y_rotation = eyebrow_midpoint - mediapipe_xyz[def_constants.MP_NOSE]
    head_y_rotation = head_y_rotation / np.linalg.norm(head_y_rotation)
    
    return [shoulder_L_rotation, 
            elbow_L_rotation, 
            hand_L_rotation, 
            hips_L_rotation, 
            knee_L_rotation, 
            foot_L_rotation, 
            shoulder_R_rotation, 
            elbow_R_rotation, 
            hand_R_rotation, 
            hips_R_rotation, 
            knee_R_rotation, 
            foot_R_rotation,
            root_x_rotation,
            chest_x_rotation,
            head_x_rotation,
            head_y_rotation
            ]

def set_rotation_for_single_bone(target_armature_name, bone_name, vector):    
    # open bone class
    try:
        bone = def_Bone.Bone(bone_name=bone_name, armature_name=target_armature_name)
        
        # get y-axis of upper_arm.L
        bone.set_bone_align_to_world_vector(world_vector = vector)  
        
        # set bone rotation to current keyframe
        bone.insert_rotation_to_current_keyframe()
        return
    
    except:
        return

def set_face_direction_for_single_bone(target_armature_name, bone_name, vector):    
    # open bone class
    try:
        bone = def_Bone.Bone(bone_name=bone_name, armature_name=target_armature_name)
        
        # get y-axis of upper_arm.L
        bone.set_bone_face_to_world_vector(world_vector = vector)  
        
        # set bone rotation to current keyframe
        bone.insert_rotation_to_current_keyframe()
        return
    
    except:
        return

def MP_set_rotation_for_all_bones(armature_selector, mediapipe_output):

    def ease_in_out_lerp(a, b, t):
        # Cubic ease-in-ease-out
        t = t * t * (3 - 2 * t)
        return a + (b - a) * t
    
    def lerp(a, b, t):
        return a + (b - a) * t
    
    rotation_list = convert_mediapipe_output_into_rotation_list(mediapipe_output)
    
    # set rotation of spines    
    spine_rotation_check = mediapipe_output[def_constants.MP_SHOULDER_R][def_constants.PRESENCE] > 0.5 and armature_selector.pelvis
    spine_rotation_check = spine_rotation_check and mediapipe_output[def_constants.MP_SHOULDER_L][def_constants.PRESENCE] > 0.5 and armature_selector.spine_0
    spine_rotation_check = spine_rotation_check and mediapipe_output[def_constants.MP_HIPS_L][def_constants.PRESENCE] > 0.5 and armature_selector.spine_1
    spine_rotation_check = spine_rotation_check and mediapipe_output[def_constants.MP_HIPS_R][def_constants.PRESENCE] > 0.5 and armature_selector.spine_2
    
    if spine_rotation_check:
        spine0_vector = lerp(rotation_list[def_constants.MP_ROOT_ROTATION], rotation_list[def_constants.MP_CHEST_ROTATION], 0.333)
        spine1_vector = lerp(rotation_list[def_constants.MP_ROOT_ROTATION], rotation_list[def_constants.MP_CHEST_ROTATION], 0.666)
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.pelvis, vector=rotation_list[def_constants.MP_ROOT_ROTATION])
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.spine_0, vector=spine0_vector)
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.spine_1, vector=spine1_vector)
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.spine_2, vector=rotation_list[def_constants.MP_CHEST_ROTATION])
    
    # rotate shoudler
    if mediapipe_output[def_constants.MP_SHOULDER_L][def_constants.PRESENCE] > 0.5 and armature_selector.shoulder_L:
        bone = def_Bone.Bone(bone_name=armature_selector.shoulder_L, armature_name=armature_selector.target_armature.name)
        if rotation_list[def_constants.MP_SHOULDER_L_ROTATION][def_constants.Z] > 0:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], ease_in_out_lerp(0, 45, rotation_list[def_constants.MP_SHOULDER_L_ROTATION][def_constants.Z]))
        elif rotation_list[def_constants.MP_SHOULDER_L_ROTATION][def_constants.Z] > -0.2:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], ease_in_out_lerp(0, -30, rotation_list[def_constants.MP_SHOULDER_L_ROTATION][def_constants.Z] / 0.2))
        else:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], -30)
    if mediapipe_output[def_constants.MP_SHOULDER_R][def_constants.PRESENCE] > 0.5 and armature_selector.shoulder_R:
        bone = def_Bone.Bone(bone_name=armature_selector.shoulder_R, armature_name=armature_selector.target_armature.name)
        if rotation_list[def_constants.MP_SHOULDER_R_ROTATION][def_constants.Z] > 0:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], ease_in_out_lerp(0, 45, rotation_list[def_constants.MP_SHOULDER_R_ROTATION][def_constants.Z]))
        elif rotation_list[def_constants.MP_SHOULDER_R_ROTATION][def_constants.Z] > -0.2:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], ease_in_out_lerp(0, -30, rotation_list[def_constants.MP_SHOULDER_R_ROTATION][def_constants.Z] / 0.2))
        else:
            bone.set_bone_rotation_around_world_space_vector([1, 0, 0], -30)
    
    # Rotate Neck
    if mediapipe_output[def_constants.MP_HEAD_L][def_constants.PRESENCE] > 0.5 and armature_selector.neck and mediapipe_output[def_constants.MP_HEAD_R][def_constants.PRESENCE] > 0.5:
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.head, vector=rotation_list[def_constants.MP_HEAD_X_ROTATION])
        set_face_direction_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.neck, vector=(rotation_list[def_constants.MP_HEAD_X_ROTATION] + rotation_list[def_constants.MP_CHEST_ROTATION])/2)
    
    # align limbs to world vector
    if mediapipe_output[def_constants.MP_SHOULDER_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.upperarm_L, vector=rotation_list[def_constants.MP_SHOULDER_L_ROTATION])
    if mediapipe_output[def_constants.MP_ELBOW_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.forearm_L, vector=rotation_list[def_constants.MP_ELBOW_L_ROTATION])
    if mediapipe_output[def_constants.MP_HAND_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.hand_L, vector=rotation_list[def_constants.MP_HAND_L_ROTATION])
    if mediapipe_output[def_constants.MP_HIPS_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.thigh_L, vector=rotation_list[def_constants.MP_HIPS_L_ROTATION])
    if mediapipe_output[def_constants.MP_KNEES_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.shin_L, vector=rotation_list[def_constants.MP_KNEE_L_ROTATION])
    if mediapipe_output[def_constants.MP_TOE_L][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.foot_L, vector=rotation_list[def_constants.MP_FOOT_L_ROTATION])
    if mediapipe_output[def_constants.MP_SHOULDER_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.upperarm_R, vector=rotation_list[def_constants.MP_SHOULDER_R_ROTATION])
    if mediapipe_output[def_constants.MP_ELBOW_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.forearm_R, vector=rotation_list[def_constants.MP_ELBOW_R_ROTATION])
    if mediapipe_output[def_constants.MP_HAND_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.hand_R, vector=rotation_list[def_constants.MP_HAND_R_ROTATION])
    if mediapipe_output[def_constants.MP_HIPS_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.thigh_R, vector=rotation_list[def_constants.MP_HIPS_R_ROTATION])
    if mediapipe_output[def_constants.MP_KNEES_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.shin_R, vector=rotation_list[def_constants.MP_KNEE_R_ROTATION])
    if mediapipe_output[def_constants.MP_TOE_R][def_constants.PRESENCE] > 0.5:
        set_rotation_for_single_bone(target_armature_name=armature_selector.target_armature.name, bone_name=armature_selector.foot_R, vector=rotation_list[def_constants.MP_FOOT_R_ROTATION])
    

def MP_set_rotation_for_all_bones_in_frame(armature_selector, frame_number, mediapipe_output):
    # Enable auto keyframing
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
    
    # Move to the specified frame
    bpy.context.scene.frame_set(frame_number)    
    
    # Set rotation for all bones
    MP_set_rotation_for_all_bones(armature_selector, mediapipe_output)
    
    # Update scene to create real time display
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

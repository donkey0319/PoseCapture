import bpy
import mediapipe as mp
import cv2
import numpy as np
import json
import sys
import os
import time

# dir = os.path.dirname(bpy.data.filepath)
# if not dir in sys.path:
#     sys.path.append(dir)
    
# import lib_rotation
# import imp
# imp.reload(lib_rotation)
# from lib_rotation import *

from . import lib_rotation
from lib_rotation import *

# =============================== FINISH IMPORTING STUFF ===============================

def read_video_and_set_pose(video_path = 'videos/yuchieh5.mp4', armature_selector = None):
    frame_number = 0

    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = mp_pose.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            # Draw pose landmarks.
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

            # Extract landmarks.
            landmarks = results.pose_landmarks.landmark
            pose_array = np.zeros((39, 5))  # Initialize an array of zeros with shape (39, 5).

            for i, landmark in enumerate(landmarks):
                if i < 39:  # Ensure we only process the first 39 landmarks.
                    pose_array[i] = [landmark.x, landmark.y, landmark.z, landmark.visibility, landmark.presence]

            MP_set_rotation_for_all_bones_in_frame(armature_selector, frame_number, pose_array)
            frame_number += 1

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

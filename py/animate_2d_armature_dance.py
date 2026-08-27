import math, bpy

scene = bpy.context.scene
arm_obj = bpy.data.objects.get("Guray2DArmature")

if arm_obj and hasattr(arm_obj, "pose"):
    arm_obj.rotation_mode = 'XYZ'
    pose = arm_obj.pose

    # Keyframe 14 strategic pose frames
    for frame in [1, 15, 30, 45, 60, 75, 90, 120, 150, 180, 210, 240, 270, 300]:
        t = frame * 0.1
        l_rot = math.sin(t) * 0.4
        r_rot = -math.sin(t + 0.5) * 0.4

        if "Arm_L" in pose.bones:
            pose.bones["Arm_L"].rotation_euler = (0, 0, l_rot)
            pose.bones["Arm_L"].keyframe_insert(data_path="rotation_euler", frame=frame)

        if "Arm_R" in pose.bones:
            pose.bones["Arm_R"].rotation_euler = (0, 0, r_rot)
            pose.bones["Arm_R"].keyframe_insert(data_path="rotation_euler", frame=frame)

    scene.frame_start = 1
    scene.frame_end = 300

print("ANIMATE_2D_ARMATURE_SUCCESS: Keyframed strategic pose frames via Python script!")

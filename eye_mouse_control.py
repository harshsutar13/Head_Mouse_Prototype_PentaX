import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

smoothing_buffer = []
buffer_size = 3

def smooth_position(x, y):
    smoothing_buffer.append((x, y))
    if len(smoothing_buffer) > buffer_size:
        smoothing_buffer.pop(0)
    avg_x = np.mean([pos[0] for pos in smoothing_buffer])
    avg_y = np.mean([pos[1] for pos in smoothing_buffer])
    return int(avg_x), int(avg_y)

BLINK_MIN_DURATION = 0.2
BLINK_MAX_DURATION = 1.0
CLICK_COOLDOWN = 1.2

blink_start_time = None
last_click_time = 0
blink_threshold = None
calibrated = False

def calibrate_blink_threshold(landmarks, calibration_frames=30):
    differences = []
    for _ in range(calibration_frames):
        left_eye = [landmarks[145], landmarks[159]]
        differences.append(left_eye[0].y - left_eye[1].y)
    return np.mean(differences) * 0.75

def detect_blink(landmarks):
    global blink_start_time, last_click_time, blink_threshold, calibrated

    left_eye = [landmarks[145], landmarks[159]]
    eye_ratio = left_eye[0].y - left_eye[1].y

    if not calibrated:
        blink_threshold = calibrate_blink_threshold(landmarks)
        calibrated = True
        print(f"Blink threshold calibrated: {blink_threshold}")

    current_time = time.time()

    if eye_ratio < blink_threshold:
        if blink_start_time is None:
            blink_start_time = current_time
        elif BLINK_MIN_DURATION <= (current_time - blink_start_time) <= BLINK_MAX_DURATION:
            if current_time - last_click_time > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = current_time
    else:
        blink_start_time = None

def main():
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise RuntimeError("Unable to open camera.")
    except Exception as e:
        print(f"Error: {e}")
        return

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 520)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)

    face_mesh = mp_face_mesh.FaceMesh(
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    screen_w, screen_h = pyautogui.size()

    max_speed = 50
    sensitivity = 3.0
    dead_zone = 0.1

    while True:
        _, frame = cam.read()
        if frame is None:
            print("Error: Unable to capture frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            detect_blink(landmarks)

            right_eye = landmarks[474:478]
            for id, landmark in enumerate(right_eye):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

                if id == 1:
                    rel_x = (landmark.x - 0.5) * 2 * sensitivity
                    rel_y = (landmark.y - 0.5) * 2 * sensitivity

                    if abs(rel_x) < dead_zone:
                        rel_x = 0
                    if abs(rel_y) < dead_zone:
                        rel_y = 0

                    move_x = rel_x * max_speed
                    move_y = rel_y * max_speed

                    smooth_x, smooth_y = smooth_position(move_x, move_y)
                    pyautogui.moveRel(smooth_x, smooth_y)

        cv2.putText(
            frame,
            "Eye Mouse (Right Eye) + Blink Click (Left Eye)",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow("Eye Controlled Mouse", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

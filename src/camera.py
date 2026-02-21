from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import cv2
import mediapipe as mp

from config import CAMERA_HEIGHT, CAMERA_INDEX, CAMERA_WIDTH


@dataclass
class FaceState:
    mouth_open_ratio: float


class CameraTracker:
    def __init__(self) -> None:
        self.capture = cv2.VideoCapture(CAMERA_INDEX)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        self._mp_face_mesh = mp.solutions.face_mesh
        self.mesh = self._mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def read_face_state(self) -> tuple[bool, Optional[FaceState], Optional[cv2.typing.MatLike]]:
        success, frame = self.capture.read()
        if not success:
            return False, None, None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.mesh.process(frame_rgb)

        face_state = None
        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            upper_lip = landmarks[13]
            lower_lip = landmarks[14]
            left_eye = landmarks[33]
            right_eye = landmarks[263]

            mouth_gap = abs(lower_lip.y - upper_lip.y)
            eye_width = abs(right_eye.x - left_eye.x)
            mouth_open_ratio = mouth_gap / eye_width if eye_width > 0 else 0.0

            face_state = FaceState(mouth_open_ratio=mouth_open_ratio)

        return True, face_state, frame

    def close(self) -> None:
        self.mesh.close()
        self.capture.release()
        cv2.destroyAllWindows()

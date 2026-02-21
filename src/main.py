from __future__ import annotations

import cv2

from camera import CameraTracker
from game import BeatGame
from gestures import GestureEngine


def main() -> None:
    tracker = CameraTracker()
    gesture_engine = GestureEngine()
    game = BeatGame()

    try:
        while game.running:
            game.poll_events()
            dt = game.tick()

            success, face_state, frame = tracker.read_face_state()
            if not success:
                continue

            gesture = gesture_engine.infer(face_state)
            game.step(dt=dt, hit_action=gesture.hit)

            if frame is not None:
                if face_state is not None:
                    label = f"mouth_ratio={face_state.mouth_open_ratio:.2f}"
                else:
                    label = "no face"

                cv2.putText(
                    frame,
                    label,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )
                cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        tracker.close()
        game.close()


if __name__ == "__main__":
    main()

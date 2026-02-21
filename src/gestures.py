from __future__ import annotations

import time
from dataclasses import dataclass

from camera import FaceState
from config import GESTURE_COOLDOWN_SECONDS


@dataclass
class GestureOutput:
    hit: bool


class GestureEngine:
    def __init__(self) -> None:
        self._last_trigger_time = 0.0

    def infer(self, face_state: FaceState | None) -> GestureOutput:
        if face_state is None:
            return GestureOutput(hit=False)

        now = time.perf_counter()
        cooldown_ok = (now - self._last_trigger_time) >= GESTURE_COOLDOWN_SECONDS

        mouth_open = face_state.mouth_open_ratio > 0.22
        hit = mouth_open and cooldown_ok

        if hit:
            self._last_trigger_time = now

        return GestureOutput(hit=hit)

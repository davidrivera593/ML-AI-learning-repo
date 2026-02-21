# ML-AI-learning-repo

## Webcam Beat Game (MVP)

This repo now includes a beginner-friendly starter architecture for a Python rhythm game controlled by face gestures.

### Recommended stack

- Python 3.10+
- MediaPipe (face landmarks)
- OpenCV (camera frames)
- PyGame (beat game window and input)
- Optional later: PyTorch (custom gesture classifier)

### Why this approach

For a beat game, low latency matters more than identity recognition. Start with **face landmarks + simple gesture rules** (smile, mouth open, head left/right). It is faster to build and easier to debug than full facial recognition.

---

## Learning + Build Plan (3 Weeks)

### Week 1: Foundations

1. Learn webcam + frame processing with OpenCV.
2. Learn MediaPipe face landmarks and visualize landmark points.
3. Implement one gesture detector (example: mouth open).

### Week 2: Game Loop

1. Build a simple PyGame beat lane with notes falling.
2. Map one gesture to one action (`hit`).
3. Add timing windows (`perfect`, `good`, `miss`).

### Week 3: Improve Control Quality

1. Add 2–3 gestures (left, right, hit).
2. Add smoothing and per-user calibration.
3. Record basic metrics: FPS, gesture confidence, hit accuracy.

---

## Project Structure

```text
.
├── README.md
├── requirements.txt
└── src
	├── main.py
	├── config.py
	├── camera.py
	├── gestures.py
	└── game.py
```

### Responsibilities

- `src/main.py`: app entrypoint and wiring.
- `src/config.py`: runtime constants.
- `src/camera.py`: webcam capture and face landmark extraction.
- `src/gestures.py`: convert landmarks into game actions.
- `src/game.py`: rhythm loop, scoring, and rendering.

---

## Quickstart

### 1) Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run

```powershell
python src/main.py
```

Controls:

- Press `Q` in the camera window to quit.
- Press `ESC` in the game window to quit.

---

## Next Upgrades

1. Add beat map loading from JSON.
2. Add audio sync and offset calibration.
3. Replace rule-based gestures with a PyTorch sequence model trained on landmark windows.~
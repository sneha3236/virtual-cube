<img width="1280" height="640" alt="banner" src="https://github.com/user-attachments/assets/0add7f9d-17da-42cf-a0cc-aaa5dfbbb619" />


# Virtual Cube: Hand-Controlled Rubik's Cube

Control and solve a 3D Rubik's Cube using only your hand. The laptop webcam
tracks your hand in real time, gestures are recognised, and they drive a 3D
cube that can be rotated, scrambled and solved on screen.

> Built with Python, OpenCV, MediaPipe and Ursina.
## Features

- **Real-time hand tracking** using MediaPipe (21 landmarks per hand)
- **Gesture recognition**: pinch to rotate the cube, point and swipe to turn a layer, hold a fist to auto-solve
- **3D cube** with smooth animated layer turns (Ursina)
- **Accurate cube model**: every sticker is tracked in 3D space, so what you see always matches the logical state
- **Auto-solve** using the Kociemba algorithm (if installed) or by undoing the move history
- **Keyboard and mouse fallback** if no webcam is available
- Unit tests for the cube logic and solver (`test_cube.py`)

## How it works

<img width="1280" height="420" alt="architecture" src="https://github.com/user-attachments/assets/5064f255-8883-4721-9619-af62c87d7360" />


1. OpenCV reads frames from the webcam.
2. MediaPipe detects 21 hand landmarks per frame.
3. Simple geometric rules turn landmarks into gestures. Pinch distance is
   normalised by hand size, so it works at different distances from the camera.
   Positions are smoothed with an exponential moving average to reduce jitter.
4. Gestures are mapped to cube actions (rotate view, turn a layer, solve).
5. The cube logic updates the sticker state and Ursina animates the turn.

## Controls

| Input | Action |
|---|---|
| Pinch (thumb + index) and move hand | Rotate the whole cube |
| Only index finger up, swipe right / left | Turn the U layer (U / U') |
| Only index finger up, swipe up / down | Turn the R layer (R / R') |
| Fist held for about 1.2 s | Auto-solve |
| Keys `U R F D L B` (hold Shift for prime) | Turn a face |
| `S` / `Space` / `C` | Scramble / Solve / Reset |
| Mouse drag | Rotate the view |

## Installation

**Requirements:** Windows, macOS or Linux, a webcam, and **Python 3.9 to 3.12**
(MediaPipe does not support Python 3.13 yet).

```bash
git clone https://github.com/YOUR-USERNAME/virtual-cube.git
cd virtual-cube

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
python test_cube.py     # optional: run the logic tests
python main.py
```

No webcam? Set `USE_HAND = False` in `main.py` and use the keyboard and mouse.

## Project structure

```
virtual-cube/
├── main.py            # app loop, 3D view, animations
├── hand_control.py    # webcam + MediaPipe + gesture detection
├── cube_state.py      # cube model, moves, solver
├── test_cube.py       # tests for cube logic and solver
├── requirements.txt
└── assets/            # images used in this README
```

## Limitations

- Only the 3x3 cube is supported so far.
- Without the optional `kociemba` package, the solver undoes the moves made in
  the app. It cannot solve an arbitrary cube loaded from outside.
- Gestures use rule-based detection, so lighting and camera angle can affect accuracy.

## Roadmap

- [ ] Train a custom gesture classifier on collected landmark data and report accuracy
- [ ] Scan a real cube with the webcam and load its colours
- [ ] Support 2x2 and other cube types
- [ ] Measure and report FPS and gesture latency

## Tech stack

Python · OpenCV · MediaPipe · Ursina · Kociemba (optional)

## Author

**Your Name**: [GitHub](https://github.com/YOUR-USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR-PROFILE)

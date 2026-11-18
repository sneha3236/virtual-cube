# Virtual Cube - hand-controlled Rubik's cube (Python)

## Setup (Python 3.9 - 3.12 needed for mediapipe)
    python -m venv venv
    venv\Scripts\activate        # Windows   (Mac/Linux: source venv/bin/activate)
    pip install -r requirements.txt
    python test_cube.py          # logic test
    python main.py

## Controls
| Input | Action |
|---|---|
| Pinch thumb+index and move hand | Rotate whole cube |
| Only index finger up + swipe | right=U, left=U', up=R, down=R' |
| Fist held ~1.2 s | Auto-solve (Kociemba) |
| Keys U R F D L B (+Shift) | Face turns |
| S / SPACE / C | Scramble / Solve / Reset |
| Mouse drag | Rotate view |

No webcam? Set USE_HAND = False in main.py.
If the cube spins the wrong way with your hand, change the sign of HAND_ROT_SPEED.

## Next steps (for your resume)
1. Train your own gesture classifier (landmarks -> MLP) and report accuracy.
2. Scan a real cube with the camera (color detection) and load it.
3. Add 2x2 and other cube types.

"""Webcam -> MediaPipe hand landmarks -> simple gestures.
GRAB  (pinch thumb+index, move hand) : rotate whole cube
POINT (only index finger up) + swipe : turn a layer (right=U, left=U', up=R, down=R')
FIST  (hold ~1.2s)                   : auto-solve"""
import time, math
from collections import deque
import cv2
import mediapipe as mp


class HandControl:
    def __init__(self, cam=0):
        self.cap = cv2.VideoCapture(cam)
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)
        self.draw = mp.solutions.drawing_utils
        self.prev = None
        self.trail = deque(maxlen=12)
        self.last_swipe = 0.0
        self.fist_since = None
        self.fist_fired = False
        self.sx = self.sy = None  # smoothed position

    def poll(self):
        out = {'gesture': 'none', 'dx': 0.0, 'dy': 0.0, 'swipe': None, 'solve': False}
        ok, frame = self.cap.read()
        if not ok:
            return out
        frame = cv2.flip(frame, 1)
        res = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        now = time.time()
        g = 'none'
        if res.multi_hand_landmarks:
            hl = res.multi_hand_landmarks[0]
            lm = hl.landmark
            size = math.hypot(lm[0].x - lm[9].x, lm[0].y - lm[9].y) or 1e-6
            pinch = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y) / size < 0.35
            up = [lm[t].y < lm[p].y for t, p in ((8, 6), (12, 10), (16, 14), (20, 18))]
            if pinch: g = 'grab'
            elif not any(up): g = 'fist'
            elif up == [True, False, False, False]: g = 'point'
            else: g = 'open'

            # smooth the tracked point (exponential moving average)
            x, y = lm[9].x, lm[9].y
            self.sx = x if self.sx is None else self.sx * 0.6 + x * 0.4
            self.sy = y if self.sy is None else self.sy * 0.6 + y * 0.4

            if g == 'grab':
                if self.prev:
                    out['dx'], out['dy'] = self.sx - self.prev[0], self.sy - self.prev[1]
                self.prev = (self.sx, self.sy)
            else:
                self.prev = None

            if g == 'point':
                self.trail.append((now, lm[8].x, lm[8].y))
                recent = [p for p in self.trail if now - p[0] < 0.35]
                if len(recent) >= 3 and now - self.last_swipe > 0.9:
                    dx, dy = recent[-1][1] - recent[0][1], recent[-1][2] - recent[0][2]
                    if max(abs(dx), abs(dy)) > 0.22:
                        out['swipe'] = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) \
                            else ('down' if dy > 0 else 'up')
                        self.last_swipe = now
                        self.trail.clear()
            else:
                self.trail.clear()

            if g == 'fist':
                self.fist_since = self.fist_since or now
                if now - self.fist_since > 1.2 and not self.fist_fired:
                    out['solve'] = self.fist_fired = True
            else:
                self.fist_since, self.fist_fired = None, False

            self.draw.draw_landmarks(frame, hl, mp.solutions.hands.HAND_CONNECTIONS)
        else:
            self.prev = None
            self.trail.clear()

        out['gesture'] = g
        cv2.putText(frame, g.upper(), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera (ESC in this window = ignore)', cv2.resize(frame, (480, 360)))
        cv2.waitKey(1)
        return out

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

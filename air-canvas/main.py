import cv2, math
import mediapipe as mp
import numpy as np

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
canvas = None
prev = None
smooth = None
last_mode = None
alpha = 0.65   # higher = smoother but laggier, try 0.5 to 0.85
hue = 0        # hue of the drawing color, in [0, 180]

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None:
        canvas = frame * 0

    res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    mode = None
    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0].landmark
        pt = lambda i: (lm[i].x * w, lm[i].y * h)
        wrist = pt(0)
        up = lambda tip, pip: math.dist(wrist, pt(tip)) > 1.1 * math.dist(wrist, pt(pip))
        idx, mid, ring, pinky = up(8, 6), up(12, 10), up(16, 14), up(20, 18)

        if idx and not (mid or ring or pinky):
            mode, target = "draw", pt(8)      # only the index finger is up
        elif idx and mid and ring and pinky:
            mode, target = "erase", pt(9)     # open palm, tracks the palm center

    if mode != last_mode:                     # gesture changed, so restart the line
        smooth, prev = None, None
    last_mode = mode

    if mode:
        smooth = target if smooth is None else (
            smooth[0] * alpha + target[0] * (1 - alpha),
            smooth[1] * alpha + target[1] * (1 - alpha))
        p = (int(smooth[0]), int(smooth[1]))
        if mode == "draw":
            cv2.circle(frame, p, 8, (0, 255, 0), -1)
            if prev:
                hue = (hue + 2) % 180
                col = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
                cv2.line(canvas, prev, p, tuple(int(c) for c in col), 6)
            prev = p
        else:
            cv2.circle(canvas, p, 50, (0, 0, 0), -1)
            cv2.circle(frame, p, 50, (255, 255, 255), 2)

    blur = cv2.GaussianBlur(canvas, (0, 0), 12)
    glow = cv2.addWeighted(blur, 1.6, blur, 0, 0)
    cv2.imshow("air canvas", cv2.add(cv2.add(frame, canvas), glow))
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    if key == ord("c"):
        canvas[:] = 0

cap.release()
cv2.destroyAllWindows()
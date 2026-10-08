import cv2, math, random, time
import mediapipe as mp
from collections import Counter, deque

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

def classify(lm, w, h):
    pt = lambda i: (lm[i].x * w, lm[i].y * h)
    wrist = pt(0)
    up = lambda tip, pip: math.dist(wrist, pt(tip)) > 1.1 * math.dist(wrist, pt(pip))
    idx, mid, ring, pinky = up(8, 6), up(12, 10), up(16, 14), up(20, 18)
    if idx and mid and ring and pinky:
        return "paper"
    if idx and mid and not (ring or pinky):
        return "scissors"
    if not (idx or mid or ring or pinky):
        return "rock"
    return None   # anything else = not a valid move

def text(img, s, pos, scale=1, color=(255, 255, 255), thick=2):
    cv2.putText(img, s, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)

state, t0 = "idle", 0
recent = deque(maxlen=8)          # last few gestures, so one bad frame doesn't ruin a round
player = comp = result = None
score = {"you": 0, "cpu": 0}

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    gesture = None
    if res.multi_hand_landmarks:
        gesture = classify(res.multi_hand_landmarks[0].landmark, w, h)
    recent.append(gesture)

    now = time.time()
    if state == "counting":
        elapsed = now - t0
        if elapsed < 3:
            text(frame, str(3 - int(elapsed)), (w // 2 - 30, h // 2), 4, (0, 255, 255), 6)
        else:
            votes = Counter(g for g in recent if g)
            if not votes:
                player, comp, result = None, None, "No move detected!"
            else:
                player = votes.most_common(1)[0][0]
                comp = random.choice(list(BEATS))
                if player == comp:
                    result = "Draw!"
                elif BEATS[player] == comp:
                    result = "You win!"; score["you"] += 1
                else:
                    result = "CPU wins!"; score["cpu"] += 1
            state, t0 = "show", now

    elif state == "show":
        if player:
            text(frame, f"You: {player}", (20, h - 90), 1)
            text(frame, f"CPU: {comp}", (20, h - 50), 1)
        text(frame, result, (w // 2 - 120, h // 2), 1.6, (0, 255, 0), 4)
        if now - t0 > 3:
            state = "idle"

    else:
        text(frame, "SPACE to play", (w // 2 - 130, 60), 1.1, (0, 255, 255))

    text(frame, f"You {score['you']} - {score['cpu']} CPU", (20, 40), 0.8)
    text(frame, f"seeing: {gesture or '-'}", (20, 75), 0.6, (200, 200, 200), 1)

    cv2.imshow("rock paper scissors", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    if key == 32 and state == "idle":
        state, t0 = "counting", time.time()

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp

# Initialize mediapipe
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

hands = mpHands.Hands()

# Start webcam
cap = cv2.VideoCapture(0)

# Finger tip landmark IDs
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            # Get landmark positions
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            # Draw hand skeleton
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    fingers = []

    if lmList:

        # Thumb (check x direction)
        if lmList[4][1] < lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other four fingers (check y direction)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # Display finger count
        cv2.putText(img, f'Fingers: {totalFingers}', (40, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Hand Gesture Recognition", img)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
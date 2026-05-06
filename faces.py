import cv2
import time

# Load the Haar Cascade model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start video capture
cap = cv2.VideoCapture(0)

people_count = 0
in_frame = 0

person_detected=False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to 640x480
    frame = cv2.resize(frame, (640, 480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # if not person_detected and len(faces) > 0:
    #     people_count+=1
    #     person_detected=True
    # elif len(faces) == 0:
    #     person_detected=False

    if len(faces) > in_frame:
        people_count += len(faces) - in_frame

        # time.s

    in_frame = len(faces)

    # Log number of faces
    print(f"Total Count: {people_count} New faces detected: {len(faces)}")

    # (Optional) log coordinates too
    for i, (x, y, w, h) in enumerate(faces):
        print(f"Face {i}: x={x}, y={y}, w={w}, h={h}")

        # Draw rectangles
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import face_recognition
import numpy as np

# Configuration
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Smaller = stricter matching
FACE_MATCH_THRESHOLD = 0.5

face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

# Storage for known people
known_face_encodings = []

total_people = 0

# Start Camera
cap = cv2.VideoCapture(0)

print("Starting people counter...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    # Resize for performance
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Convert formats
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Haar Cascade Face Detection
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30)
    )

    people_in_frame = []

    # Process Each Face
    for (x, y, w, h) in faces:

        # Convert OpenCV coords -> face_recognition coords
        top = y
        right = x + w
        bottom = y + h
        left = x

        # Encode face
        encodings = face_recognition.face_encodings(
            rgb,
            [(top, right, bottom, left)]
        )

        # Sometimes encoding fails
        if len(encodings) == 0:
            continue

        face_encoding = encodings[0]

        person_id = None

        # Compare against known faces
        if len(known_face_encodings) > 0:

            distances = face_recognition.face_distance(
                known_face_encodings,
                face_encoding
            )

            best_match_index = np.argmin(distances)

            if distances[best_match_index] < FACE_MATCH_THRESHOLD:
                person_id = best_match_index

                people_in_frame.append(int(person_id))

        # New person
        if person_id is None:
            print(f"NEW PERSON DETECTED -> Person {len(known_face_encodings)}")
            people_in_frame.append(len(known_face_encodings))
            known_face_encodings.append(face_encoding)

        # Draw UI
        # cv2.rectangle(frame,(x, y),(x + w, y + h),(255, 0, 0),2)
        # cv2.putText(frame,f"Person {person_id}",(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 0, 0),2)


    # Display Total Unique People
    if len(faces) != total_people:

        total_people = len(faces)

        print(f"Total unique people seen: {len(known_face_encodings)}, Faces currently visible: {len(faces)} {people_in_frame}")

    # Show frame
    # cv2.putText(frame,f"Unique People Seen: {total_people}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2) 
    # cv2.imshow("Face Recognition Tracker", frame)
    # Quit
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Cleanup
cap.release()
cv2.destroyAllWindows()

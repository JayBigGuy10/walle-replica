import cv2
import time
import serial
import pyttsx3

# Initialize serial connection
ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)

# Load the Haar Cascade model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start video capture
cap = cv2.VideoCapture(0)

people_count = 0
in_frame = 0

person_detected=False


#67 Hands

def move_hands():
    for i in range(20, 81, 2):
        ser.write(f"L{i}\n".encode())
        ser.write(f"R{100-i}\n".encode())
        time.sleep(0.015)

    for i in range(80, 19, -2):
        ser.write(f"L{i}\n".encode())
        ser.write(f"R{100-i}\n".encode())
        time.sleep(0.015)

# Speech

def speak(p):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    phrase = str(p)
    engine.say(phrase)
    engine.runAndWait()
    


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

        # Play Sound and Animation here
        speak(people_count)
        move_hands()
        time.sleep(3)

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

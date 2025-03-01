from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import mediapipe as mp
import time






app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Mediapipe Hand Solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Recognize Hand Gestures
def recognize_gesture(hand_landmarks, frame):
    h, w, _ = frame.shape
    landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

    fingertips = [8, 12, 16, 20]  # Indices for fingertips
    thumb_tip = 4
    index_tip = 8


    # Gesture E: Fist shape, thumb beside fingers
    if all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips) and landmarks[thumb_tip][0] < landmarks[3][0]:
        return 'E'

    # Gesture B: Open palm, fingers straight
    elif all(landmarks[i][1] < landmarks[i - 2][1] for i in fingertips) and landmarks[thumb_tip][0] > landmarks[3][0]:
        return 'B'

    # Gesture D: Index finger extended, others curled
    elif all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips[1:]) and landmarks[8][1] < landmarks[6][1]:
        return 'D'

    # Gesture A: Thumb pointing out, fingers curled
    elif (
        landmarks[thumb_tip][1] < (
            sum(landmarks[i][1] for i in fingertips[1:]) / len(fingertips[1:]) - 20
        )  # Adjust the offset (20) as needed
    ):
        return 'A'

    elif (
        abs(landmarks[thumb_tip][0] - landmarks[index_tip][0]) < 30 and  # Thumb close to index (x-coordinate)
        abs(landmarks[thumb_tip][1] - landmarks[index_tip][1]) < 30 and  # Thumb close to index (y-coordinate)
        landmarks[12][1] < landmarks[10][1] and  # Middle finger extended
        landmarks[16][1] < landmarks[14][1] and  # Ring finger extended
        landmarks[20][1] < landmarks[18][1]  # Pinky extended
    ):
        return 'F'

    elif (
        abs(landmarks[thumb_tip][0] - landmarks[index_tip][0]) < 30 and  # Thumb close to index (x-coordinate)
        abs(landmarks[thumb_tip][1] - landmarks[index_tip][1]) > 30 and  # Thumb slightly raised compared to the index (y-coordinate)
        landmarks[8][0] > landmarks[6][0] and  # Index finger pointing forward
        landmarks[12][1] > landmarks[10][1] and  # Middle finger curled
        landmarks[16][1] > landmarks[14][1] and  # Ring finger curled
        landmarks[20][1] > landmarks[18][1]  # Pinky curled
    ):
        return 'G'

    elif (
        landmarks[20][1] < landmarks[18][1] and  # Pinky is extended
        landmarks[8][1] > landmarks[6][1] and   # Index finger is curled
        landmarks[12][1] > landmarks[10][1] and # Middle finger is curled
        landmarks[16][1] > landmarks[14][1] and # Ring finger is curled
        landmarks[4][1] > landmarks[3][1]       # Thumb is curled inward
    ):
        return 'I'

    elif (
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [8, 12, 16, 20]) and  # All fingers (index, middle, ring, pinky) are curled
        landmarks[4][0] > landmarks[3][0] and  # Thumb is extended outward (X-coordinate of the thumb tip is greater than its base)
        landmarks[4][1] < landmarks[3][1]      # Thumb is slightly above or level with its base
    ):
         return 'J'

    elif (
        landmarks[8][1] < landmarks[6][1] and    # Index finger is extended
        landmarks[12][1] < landmarks[10][1] and  # Middle finger is extended
        landmarks[16][1] > landmarks[14][1] and  # Ring finger is curled
        landmarks[20][1] > landmarks[18][1] and  # Pinky is curled
        landmarks[4][0] < landmarks[8][0]        # Thumb is outward, towards the index finger
    ):
        return 'K'

    # Detect "K" gesture


# Detect "L" gesture
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger is extended
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [12, 16, 20]) and  # Middle, ring, and pinky fingers are curled
        landmarks[4][1] > landmarks[3][1]  # Thumb is curled inward
    ):
        return 'L'
    

    # Gesture H: Index and middle finger extended, others curled
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger pointing up
        landmarks[12][1] < landmarks[10][1] and  # Middle finger pointing up
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [16, 20])  # Ring and pinky curled
    ):
        return 'H'

    # Gesture C: All fingers curled except thumb
    elif (
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips) and  # All fingers curled
        landmarks[thumb_tip][0] > landmarks[3][0]  # Thumb extended outward
    ):
        return 'C'

    # Gesture M: All fingers curled, thumb crosses palm
    elif (
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips) and  # All fingers curled
        landmarks[thumb_tip][0] < landmarks[3][0]  # Thumb crosses palm
    ):
        return 'M'

    # Gesture N: All fingers curled, thumb touches middle finger
    elif (
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips) and  # All fingers curled
        abs(landmarks[thumb_tip][0] - landmarks[12][0]) < 30  # Thumb touches middle finger
    ):
        return 'N'

    # Gesture O: All fingers form a circle
    elif (
        abs(landmarks[thumb_tip][0] - landmarks[index_tip][0]) < 30 and  # Thumb close to index (x-coordinate)
        abs(landmarks[thumb_tip][1] - landmarks[index_tip][1]) < 30 and  # Thumb close to index (y-coordinate)
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips)  # All fingers curled
    ):
        return 'O'

    # Gesture P: Index and middle finger extended, thumb touches ring finger
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger extended
        landmarks[12][1] < landmarks[10][1] and  # Middle finger extended
        landmarks[16][1] > landmarks[14][1] and  # Ring finger curled
        landmarks[20][1] > landmarks[18][1] and  # Pinky curled
        abs(landmarks[thumb_tip][0] - landmarks[16][0]) < 30  # Thumb touches ring finger
    ):
        return 'P'

    # Gesture Q: Thumb and index finger form a circle, other fingers curled
    elif (
        abs(landmarks[thumb_tip][0] - landmarks[index_tip][0]) < 30 and  # Thumb close to index (x-coordinate)
        abs(landmarks[thumb_tip][1] - landmarks[index_tip][1]) < 30 and  # Thumb close to index (y-coordinate)
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips[1:])  # Other fingers curled
    ):
        return 'Q'

    # Gesture R: Index and middle finger crossed, others curled
    elif (
        abs(landmarks[8][0] - landmarks[12][0]) < 30 and  # Index and middle finger close (x-coordinate)
        abs(landmarks[8][1] - landmarks[12][1]) < 30 and  # Index and middle finger close (y-coordinate)
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [16, 20])  # Ring and pinky curled
    ):
        return 'R'

    # Gesture S: Fist shape, thumb crosses fingers
    elif (
        all(landmarks[i][1] > landmarks[i - 2][1] for i in fingertips) and  # All fingers curled
        landmarks[thumb_tip][0] < landmarks[3][0]  # Thumb crosses fingers
    ):
        return 'S'

    # Gesture T: Thumb between index and middle finger
    elif (
        abs(landmarks[thumb_tip][0] - landmarks[8][0]) < 30 and  # Thumb close to index (x-coordinate)
        abs(landmarks[thumb_tip][1] - landmarks[8][1]) < 30 and  # Thumb close to index (y-coordinate)
        landmarks[12][1] > landmarks[10][1] and  # Middle finger curled
        landmarks[16][1] > landmarks[14][1] and  # Ring finger curled
        landmarks[20][1] > landmarks[18][1]  # Pinky curled
    ):
        return 'T'

    # Gesture U: Index and middle finger extended, others curled
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger extended
        landmarks[12][1] < landmarks[10][1] and  # Middle finger extended
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [16, 20])  # Ring and pinky curled
    ):
        return 'U'

    # Gesture V: Index and middle finger form a V shape, others curled
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger extended
        landmarks[12][1] < landmarks[10][1] and  # Middle finger extended
        landmarks[16][1] > landmarks[14][1] and  # Ring finger curled
        landmarks[20][1] > landmarks[18][1]  # Pinky curled
    ):
        return 'V'

    # Gesture W: Index, middle, and ring finger extended, pinky curled
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger extended
        landmarks[12][1] < landmarks[10][1] and  # Middle finger extended
        landmarks[16][1] < landmarks[14][1] and  # Ring finger extended
        landmarks[20][1] > landmarks[18][1]  # Pinky curled
    ):
        return 'W'

    # Gesture X: Index finger bent, others curled
    elif (
        landmarks[8][1] > landmarks[6][1] and  # Index finger bent
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [12, 16, 20])  # Other fingers curled
    ):
        return 'X'

    # Gesture Y: Thumb and pinky extended, others curled
    elif (
        landmarks[4][1] < landmarks[3][1] and  # Thumb extended
        landmarks[20][1] < landmarks[18][1] and  # Pinky extended
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [8, 12, 16])  # Other fingers curled
    ):
        return 'Y'

    # Gesture Z: Index finger draws a Z shape
    elif (
        landmarks[8][1] < landmarks[6][1] and  # Index finger extended
        all(landmarks[i][1] > landmarks[i - 2][1] for i in [12, 16, 20])  # Other fingers curled
    ):
        return 'Z'

    # Default case: Unknown gesture
    return "Unknown"



# Function for generating video frames and recognizing gestures
def generate_frames():
    cap = cv2.VideoCapture(1)
    last_sent_time = time.time()
    last_recognized_gesture = None  # Store the last recognized gesture

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if time.time() - last_sent_time >= 2:  # Limit updates to every 2 seconds
                    gesture = recognize_gesture(hand_landmarks, frame)
                    if gesture != last_recognized_gesture:  # Only proceed if the gesture changes
                        last_recognized_gesture = gesture

                        # Emit gesture to client (if using a socket)
                        socketio.emit('gesture_result', {'gesture': gesture})
                        last_sent_time = time.time()

                        

                        # # Display gesture on the frame
                        # cv2.putText(frame, f'Alphabet is: {gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 60), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Socket.IO Events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Run the App
if __name__ == "__main__":
    socketio.run(app, debug=True)
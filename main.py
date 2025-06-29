import os, time
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, Response, jsonify
from tensorflow.keras.models import load_model

# Load model and labels
model = load_model("DenseNet121_Final.keras", compile=False)
class_names = sorted(os.listdir(r"C:\Users\KAZUHA\Downloads\propject new\Translating-Silence\data"))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

app = Flask(__name__)
predicted_sequence = ""
last_active_time = time.time()
word_break_added = False
latest_confidence = 0.0
latest_prediction = ""
last_prediction_time = 0

def preprocess_image(img_roi):
    img_resized = cv2.resize(img_roi, (224, 224))
    img_resized = img_resized.astype('float32') / 255.0
    return np.expand_dims(img_resized, axis=0)

def generate_frames():
    global predicted_sequence, last_active_time, word_break_added, latest_confidence, latest_prediction, last_prediction_time
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    frame_skip = 2
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        if frame_count % frame_skip == 0:
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                last_active_time = time.time()
                word_break_added = False

                x_min, y_min, x_max, y_max = w, h, 0, 0
                for hand_landmarks in results.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        px, py = int(lm.x * w), int(lm.y * h)
                        x_min, y_min = min(x_min, px), min(y_min, py)
                        x_max, y_max = max(x_max, px), max(y_max, py)
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                margin = 30
                x_min = max(x_min - margin, 0)
                y_min = max(y_min - margin, 0)
                x_max = min(x_max + margin, w)
                y_max = min(y_max + margin, h)

                roi = image_rgb[y_min:y_max, x_min:x_max]
                if roi.size != 0:
                    input_tensor = preprocess_image(roi)
                    preds = model.predict(input_tensor, verbose=0)[0]
                    class_idx = int(np.argmax(preds))
                    confidence = float(preds[class_idx])

                    if confidence >= 0.20:
                        current_time = time.time()
                        predicted_char = class_names[class_idx]

                        # Only add new character if 2 seconds have passed since last
                        if current_time - last_prediction_time >= 2.0:
                            predicted_sequence += predicted_char
                            last_prediction_time = current_time

                        latest_prediction = predicted_char
                        latest_confidence = round(confidence * 100, 2)

                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        cv2.putText(frame, f"{predicted_char} ({latest_confidence:.1f}%)",
                                    (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 0), 2)
                    else:
                        latest_prediction = "unknown"
                        latest_confidence = 0.0
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                        cv2.putText(frame, "Low Confidence", (x_min, y_min - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                latest_prediction = "unknown"
                latest_confidence = 0.0
                cv2.putText(frame, "No Hand Detected", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                if predicted_sequence and not word_break_added:
                    if time.time() - last_active_time > 2.0:
                        predicted_sequence += " "
                        word_break_added = True

        frame_count += 1
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/predict')
def predict():
    return jsonify({
        'predicted_char': latest_prediction,
        'confidence': latest_confidence
    })

@app.route('/reset')
def reset():
    global predicted_sequence, word_break_added, last_active_time, latest_prediction, latest_confidence, last_prediction_time
    predicted_sequence = ""
    word_break_added = False
    last_active_time = time.time()
    latest_prediction = ""
    latest_confidence = 0.0
    last_prediction_time = 0
    return jsonify({'message': 'Reset successful'})

import webbrowser
from threading import Timer
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=False)

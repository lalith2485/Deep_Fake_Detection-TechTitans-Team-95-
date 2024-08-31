from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load your trained model
model = load_model('deepfake_detection_model.keras')

# Function to extract frames from the video
def extract_frames(video_path, max_frames=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))
        frame = frame.astype('float32') / 255.0  # Normalize
        frames.append(frame)
    cap.release()
    return np.array(frames)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract frames and make prediction
        frames = extract_frames(file_path)
        if len(frames) == 30:
            frames = np.expand_dims(frames, axis=0)  # Add batch dimension
            prediction = model.predict(frames)
            if prediction > 0.5:
                result = "The video is a deepfake."
            else:
                result = "The video is real."
        else:
            result = "The video does not have enough frames for analysis. Please use a longer video."
        
        return jsonify({'result': result})

    return jsonify({'error': 'File upload failed'})

if __name__ == '__main__':
    app.run(debug=True)

# verify_face.py
from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import tempfile
import os

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    if 'reference' not in request.files or 'test' not in request.files:
        return jsonify({'error': 'Please upload both reference and test images'}), 400

    ref_file = request.files['reference']
    test_file = request.files['test']

    # Save temp files
    ref_path = tempfile.mktemp(suffix='.jpg')
    test_path = tempfile.mktemp(suffix='.jpg')
    ref_file.save(ref_path)
    test_file.save(test_path)

    try:
        # Load images
        ref_image = face_recognition.load_image_file(ref_path)
        test_image = face_recognition.load_image_file(test_path)

        # Encode faces
        ref_encodings = face_recognition.face_encodings(ref_image)
        test_encodings = face_recognition.face_encodings(test_image)

        if not ref_encodings or not test_encodings:
            return jsonify({'match': False, 'error': 'No face detected in one of the images'})

        # Compare faces
        match_results = face_recognition.compare_faces([ref_encodings[0]], test_encodings[0])
        distance = face_recognition.face_distance([ref_encodings[0]], test_encodings[0])[0]

        return jsonify({
            'match': bool(match_results[0]),
            'distance': float(distance)
        })

    finally:
        os.remove(ref_path)
        os.remove(test_path)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# main.py
from flask import Flask, request, jsonify
from deepface import DeepFace
import tempfile
import os

app = Flask(__name__)

# API key protection
API_KEY = os.getenv("PY_API_KEY", "changeme")

@app.before_request
def check_api_key():
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/verify', methods=['POST'])
def verify_face():
    try:
        # Check if files are provided
        if 'student' not in request.files or 'captured' not in request.files:
            return jsonify({"error": "Both 'student' and 'captured' files are required"}), 400

        student_file = request.files['student']
        captured_file = request.files['captured']

        # Save to temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as student_temp:
            student_file.save(student_temp.name)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as captured_temp:
            captured_file.save(captured_temp.name)

        # Run DeepFace verification
        result = DeepFace.verify(
            student_temp.name,
            captured_temp.name,
            model_name="ArcFace",
            enforce_detection=False,
            distance_metric="cosine",
            detector_backend="opencv",
        )

        # Calculate confidence
        confidence = max(0, 100 * (1 - result['distance'] / 0.68))
        result['confidence'] = confidence
        result['verified'] = confidence >= 60

        # Clean up temp files
        os.remove(student_temp.name)
        os.remove(captured_temp.name)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on Deta.space assigned port
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

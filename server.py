from flask import Flask, request, jsonify
from deepface import DeepFace
import tempfile

app = Flask(__name__)

@app.route("/verify_face", methods=["POST"])
def verify_face():
    try:
        # ✅ Expect files as multipart/form-data
        if "student_photo" not in request.files or "captured_photo" not in request.files:
            return jsonify({"error": "Missing files"}), 400

        student_file = request.files["student_photo"]
        captured_file = request.files["captured_photo"]

        # Save to temp files
        student_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
        captured_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name

        student_file.save(student_path)
        captured_file.save(captured_path)

        # Run DeepFace verification
        result = DeepFace.verify(
            student_path,
            captured_path,
            model_name="ArcFace",
            enforce_detection=False,
            distance_metric="cosine",
            detector_backend="opencv",
        )

        confidence = max(0, 100 * (1 - result['distance'] / 0.68))
        result['confidence'] = confidence
        result['verified'] = confidence >= 60

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

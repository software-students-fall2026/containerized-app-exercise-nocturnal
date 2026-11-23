"""receive photos and save ingredient detections"""

import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from PIL import UnidentifiedImageError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from model import detect_objects_in_image, load_pretrained_yolo_world_model


def create_image_detection_app(model=None, scans=None):
    """create the image detection service"""
    if model is None:
        model = load_pretrained_yolo_world_model()
    if scans is None:
        client = MongoClient(
            os.environ.get("MONGO_URI", "mongodb://localhost:27017"),
            serverSelectionTimeoutMS=5000,
        )
        scans = client["fridge"]["scans"]

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

    @app.errorhandler(413)
    def reject_images_that_are_too_large(_error):
        """reject uploads larger than the limit"""
        return jsonify({"error": "image is too large"}), 413

    @app.post("/detect")
    def detect_ingredients_and_save_scan():
        """detect ingredients in an uploaded photo"""
        image = request.files.get("image")
        if image is None or not image.filename:
            return jsonify({"error": "an image is required"}), 400

        try:
            detections = detect_objects_in_image(model, image.stream)
        except (UnidentifiedImageError, OSError, ValueError):
            return jsonify({"error": "invalid image"}), 400

        scan = {
            "filename": image.filename,
            "created_at": datetime.now(timezone.utc),
            "detections": detections,
        }
        try:
            result = scans.insert_one(scan)
        except PyMongoError:
            return jsonify({"error": "could not save scan"}), 503

        return jsonify({"scan_id": str(result.inserted_id), "detections": detections})

    return app

"""tests for the image endpoint"""

from io import BytesIO
from pathlib import Path

import mongomock
from pymongo import MongoClient

from server import create_image_detection_app


def test_uploaded_image_returns_and_saves_detected_ingredients(kitchen_model):
    """check the response and saved scan"""
    scans = mongomock.MongoClient().fridge.scans
    client = create_image_detection_app(kitchen_model, scans).test_client()
    photo = Path(__file__).parent / "images" / "015011cc-fruit_109.jpg"

    with photo.open("rb") as image:
        response = client.post("/detect", data={"image": (image, photo.name)})

    assert response.status_code == 200
    body = response.get_json()
    assert {"apple", "carrot", "orange"} <= {
        item["name"] for item in body["detections"]
    }
    scan = scans.find_one()
    assert str(scan["_id"]) == body["scan_id"]
    assert scan["filename"] == photo.name
    assert scan["detections"] == body["detections"]


def test_request_without_an_image_returns_an_error(kitchen_model):
    """check that an image is required"""
    scans = mongomock.MongoClient().db.scans
    client = create_image_detection_app(kitchen_model, scans).test_client()

    response = client.post("/detect", data={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "an image is required"


def test_invalid_image_returns_an_error(kitchen_model):
    """check that invalid images are rejected"""
    scans = mongomock.MongoClient().db.scans
    client = create_image_detection_app(kitchen_model, scans).test_client()

    response = client.post("/detect", data={"image": (BytesIO(b"invalid"), "bad.jpg")})

    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid image"


def test_image_larger_than_the_limit_returns_an_error(kitchen_model):
    """check that large uploads are rejected"""
    scans = mongomock.MongoClient().db.scans
    client = create_image_detection_app(kitchen_model, scans).test_client()
    image = BytesIO(b"x" * (11 * 1024 * 1024))

    response = client.post("/detect", data={"image": (image, "big.jpg")})

    assert response.status_code == 413
    assert response.get_json()["error"] == "image is too large"


def test_database_failure_returns_an_error(kitchen_model):
    """check that failed saves are reported"""

    scans = MongoClient("mongodb://localhost:1", serverSelectionTimeoutMS=50).db.scans
    client = create_image_detection_app(kitchen_model, scans).test_client()
    photo = Path(__file__).parent / "images" / "0023c920-fruit_145.jpg"

    with photo.open("rb") as image:
        response = client.post("/detect", data={"image": (image, photo.name)})

    assert response.status_code == 503
    assert response.get_json()["error"] == "could not save scan"


def test_service_can_create_its_own_model_and_database_client():
    """check the default service setup"""
    app = create_image_detection_app()

    assert app.test_client().post("/detect", data={}).status_code == 400

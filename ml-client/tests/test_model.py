"""tests for ingredient detection"""

from pathlib import Path

import pytest
from PIL import Image, UnidentifiedImageError
from ultralytics import YOLOWorld

import model as model_client


def test_prepare_yolo_world_with_kitchen_ingredient_labels(tmp_path):
    """check that the model has ingredient labels"""
    output_path = tmp_path / "kitchen-world.pt"
    model_client.prepare_yolo_world_for_kitchen_ingredients(output_path)
    prepared_model = YOLOWorld(output_path)

    assert output_path.is_file()
    assert "apple" in prepared_model.names.values()
    assert "beer can" in prepared_model.names.values()


def test_detect_labeled_ingredients_in_four_food_photos(kitchen_model):
    """check predictions against the image labels"""
    images = Path(__file__).parent / "images"
    expected = {
        "0023c920-fruit_145.jpg": {"carrot"},
        "015011cc-fruit_109.jpg": {"apple", "carrot", "orange"},
        "0202fe83-fruit_62.jpg": {"apple", "orange"},
        "05dc044d-fruit_83.jpg": {"apple", "carrot", "orange"},
    }

    for filename, labels in expected.items():
        detections = model_client.detect_objects_in_image(
            kitchen_model, images / filename
        )
        detected_labels = {item["name"] for item in detections}

        assert labels <= detected_labels
        assert all(0 <= item["confidence"] <= 1 for item in detections)


def test_detect_objects_rejects_invalid_image(tmp_path, kitchen_model):
    """check that invalid images are rejected"""
    image_path = tmp_path / "invalid.png"
    image_path.write_text("not an image")

    with pytest.raises(UnidentifiedImageError):
        model_client.detect_objects_in_image(kitchen_model, image_path)


def test_empty_image_has_no_detected_ingredients(tmp_path, kitchen_model):
    """check that an empty image has no ingredients"""
    image_path = tmp_path / "empty.png"
    Image.new("RGB", (128, 128), "black").save(image_path)

    assert not model_client.detect_objects_in_image(kitchen_model, image_path)

"""shared model fixture"""

import pytest

from model import load_pretrained_yolo_world_model


@pytest.fixture(scope="session")
def kitchen_model():
    """load the model for image tests"""
    return load_pretrained_yolo_world_model()

"""shared pytest fixture"""

import pytest
from app import create_app


@pytest.fixture(name="app")
def app_fixture():
    """create the Flask app for pytest-flask"""
    return create_app()

"""Tests for web app"""

from app import create_app


class Tests:
    """tests for web app"""

    def test_home_page_loads(self):
        """the home page responds"""
        app = create_app()
        with app.test_client() as test_client:
            response = test_client.get("/")
            response_data = response.data.decode("utf8")
            status = response.status_code
            assert status == 200, f"Expected / to respond with 200, got {status}"
            assert len(response_data) > 0, "Expected / to return non empty page"

    def test_unknown_page_with_invalid_route(self):
        """Verify page that does not exist responds with HTTP 404"""
        app = create_app()
        with app.test_client() as test_client:
            response = test_client.get("/no-such-page")
            status = response.status_code
            assert status == 404, f"Expected 404 for missing page, got {status}"

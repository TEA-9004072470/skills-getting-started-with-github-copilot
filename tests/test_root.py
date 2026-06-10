"""Tests for the root endpoint."""

from fastapi.responses import RedirectResponse


def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows(client):
    """Test that following the redirect returns the HTML page."""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200

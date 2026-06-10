"""Pytest configuration and shared fixtures for FastAPI tests."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client(monkeypatch):
    """Provide a TestClient with isolated activities data per test."""
    # Deep copy activities to isolate test state
    isolated_activities = copy.deepcopy(activities)
    
    # Monkeypatch the app's activities dict with the isolated copy
    monkeypatch.setattr("src.app.activities", isolated_activities)
    
    return TestClient(app)


@pytest.fixture
def mock_activities(monkeypatch):
    """Provide isolated activities dict for manual manipulation in tests."""
    isolated_activities = copy.deepcopy(activities)
    monkeypatch.setattr("src.app.activities", isolated_activities)
    return isolated_activities

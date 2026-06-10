"""Tests for the activities list endpoint."""


def test_get_activities_success(client):
    """Test that GET /activities returns all activities with correct structure."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_has_expected_fields(client):
    """Test that each activity has required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that all participants are email strings."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_data in activities.values():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email check


def test_get_activities_chess_club_exists(client):
    """Test that Chess Club is in the activities list."""
    response = client.get("/activities")
    activities = response.json()
    
    assert "Chess Club" in activities
    assert activities["Chess Club"]["max_participants"] == 12


def test_get_activities_consistent_across_calls(client):
    """Test that multiple calls return the same data."""
    response1 = client.get("/activities")
    response2 = client.get("/activities")
    
    assert response1.json() == response2.json()

"""Tests for the unregister endpoint."""


def test_unregister_success(client):
    """Test successful unregistration of a student."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes participant from activity."""
    email = "michael@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()["Chess Club"]["participants"])
    
    # Unregister student
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()["Chess Club"]["participants"])
    assert updated_count == initial_count - 1
    assert email not in updated_response.json()["Chess Club"]["participants"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from non-existent activity fails."""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered_fails(client):
    """Test that unregistering someone not in activity fails."""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_response_structure(client):
    """Test that unregister response has correct structure."""
    email = "michael@mergington.edu"
    
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_same_student_twice_fails(client):
    """Test that unregistering the same student twice fails."""
    email = "michael@mergington.edu"
    
    # First unregister succeeds
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second unregister fails
    response2 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"]


def test_unregister_case_sensitive_activity_name(client):
    """Test that activity name lookup is case-sensitive."""
    response = client.delete(
        "/activities/chess club/unregister",  # lowercase
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 404


def test_unregister_case_sensitive_email(client):
    """Test that email is case-sensitive in unregister."""
    # Try to unregister with different case than registered
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "MICHAEL@MERGINGTON.EDU"}
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_with_special_characters_in_email(client):
    """Test unregister with special characters in email."""
    email = "student+test@mergington.edu"
    
    # First sign up
    client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    
    # Then unregister
    response = client.delete(
        "/activities/Drama Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify it was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Drama Club"]["participants"]

"""Tests for the signup endpoint."""


def test_signup_success(client):
    """Test successful signup for a student."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert "newstudent@mergington.edu" in response.json()["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds participant to activity."""
    email = "newstudent@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    
    # Sign up new student
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()["Chess Club"]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert email in updated_participants


def test_signup_duplicate_fails(client):
    """Test that signing up an already-registered student fails."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for non-existent activity fails."""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with special characters in email."""
    email = "student+test@mergington.edu"
    
    response = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify it was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()["Programming Class"]["participants"]


def test_signup_multiple_activities_same_student(client):
    """Test that a student can sign up for multiple different activities."""
    email = "newstudent@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups worked
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_response_structure(client):
    """Test that signup response has correct structure."""
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": "artist@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)


def test_signup_case_sensitive_activity_name(client):
    """Test that activity name lookup is case-sensitive."""
    response = client.post(
        "/activities/chess club/signup",  # lowercase
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404


def test_signup_case_sensitive_email(client):
    """Test that email comparison is case-sensitive (should allow different cases)."""
    email1 = "Student@mergington.edu"
    email2 = "student@mergington.edu"
    
    # First signup
    response1 = client.post(
        "/activities/Math Club/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    # Try to signup with lowercase - should succeed (different email)
    response2 = client.post(
        "/activities/Math Club/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200

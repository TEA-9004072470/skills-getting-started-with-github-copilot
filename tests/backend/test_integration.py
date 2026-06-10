"""Integration tests for complete workflows."""


def test_signup_then_unregister_workflow(client):
    """Test complete workflow: signup → unregister."""
    email = "workflow_student@mergington.edu"
    activity = "Soccer Club"
    
    # Get initial participant count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Verify participant count increased
    after_signup_response = client.get("/activities")
    after_signup_count = len(after_signup_response.json()[activity]["participants"])
    assert after_signup_count == initial_count + 1
    assert email in after_signup_response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Verify participant count is back to initial
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity]["participants"])
    assert final_count == initial_count
    assert email not in final_response.json()[activity]["participants"]


def test_multiple_signups_and_unregisters(client):
    """Test multiple signups and unregisters in sequence."""
    activity = "Debate Team"
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    # Initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Sign up three students
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all three were added
    after_signup = client.get("/activities")
    assert len(after_signup.json()[activity]["participants"]) == initial_count + 3
    
    # Unregister first student
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": emails[0]}
    )
    assert response.status_code == 200
    
    # Verify count is now initial + 2
    after_first_unregister = client.get("/activities")
    assert len(after_first_unregister.json()[activity]["participants"]) == initial_count + 2
    assert emails[0] not in after_first_unregister.json()[activity]["participants"]
    assert emails[1] in after_first_unregister.json()[activity]["participants"]
    assert emails[2] in after_first_unregister.json()[activity]["participants"]
    
    # Unregister remaining two
    for email in emails[1:]:
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify we're back to initial count
    final = client.get("/activities")
    assert len(final.json()[activity]["participants"]) == initial_count


def test_signup_different_activities_same_student(client):
    """Test a student signing up for and unregistering from multiple activities."""
    email = "multi_activity@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Art Studio"]
    
    # Sign up for all three
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify in all three
    check_response = client.get("/activities")
    for activity in activities:
        assert email in check_response.json()[activity]["participants"]
    
    # Unregister from first one
    response = client.delete(
        f"/activities/{activities[0]}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify removed from first but still in others
    check_response = client.get("/activities")
    assert email not in check_response.json()[activities[0]]["participants"]
    assert email in check_response.json()[activities[1]]["participants"]
    assert email in check_response.json()[activities[2]]["participants"]
    
    # Unregister from remaining two
    for activity in activities[1:]:
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify completely removed from all
    final_check = client.get("/activities")
    for activity in activities:
        assert email not in final_check.json()[activity]["participants"]


def test_signup_unregister_signup_again(client):
    """Test that a student can re-signup after unregistering."""
    email = "reregister@mergington.edu"
    activity = "Basketball Team"
    
    # Sign up
    response1 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Unregister
    response2 = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    # Verify in activity
    final_check = client.get("/activities")
    assert email in final_check.json()[activity]["participants"]

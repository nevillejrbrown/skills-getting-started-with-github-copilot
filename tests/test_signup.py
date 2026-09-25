def test_signup_adds_a_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity}"
    }
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    before = client.get("/activities").json()[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    after = client.get("/activities").json()[activity]["participants"]
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert after == before

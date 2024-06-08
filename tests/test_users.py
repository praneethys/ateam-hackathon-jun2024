from random import randint

from fastapi.testclient import TestClient


def test_users(client: TestClient) -> None:
    rand_int = randint(0, 1000)
    email = f"test{rand_int}@example.com"
    response = client.get(f"/api/v1/users/{email}")
    assert response.status_code == 404

    response = client.post(
        "/api/v1/users",
        json={"email": email, "name": "Full Name Test", "hashed_password": "test"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert response.json().get("name") == "Full Name Test"
    assert response.json().get("is_deleted") == False

    response = client.get(f"/api/v1/users/{email}")
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert response.json().get("name") == "Full Name Test"
    assert response.json().get("is_deleted") == False

    response = client.put(
        f"/api/v1/users/{email}",
        json={"email": email, "name": "Full Name Test 2", "hashed_password": "test"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert response.json().get("name") == "Full Name Test 2"
    assert response.json().get("is_deleted") == False

    response = client.delete(f"/api/v1/users/{email}")
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert response.json().get("name") == "Full Name Test 2"
    assert response.json().get("is_deleted") == True

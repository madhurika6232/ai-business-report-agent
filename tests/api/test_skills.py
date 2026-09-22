from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_list_all_skills():
    response = client.get(
        "/api/v1/skills"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 19
    assert data["domain"] is None
    assert len(data["skills"]) == 19


def test_business_skills():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "business",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 4
    assert data["domain"] == "business"

    assert all(
        skill["domain"] == "business"
        for skill in data["skills"]
    )


def test_operations_skills():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "operations",
        },
    )

    assert response.status_code == 200
    assert response.json()["count"] == 5


def test_customer_skills():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "customer",
        },
    )

    assert response.status_code == 200
    assert response.json()["count"] == 6


def test_risk_skills():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "risk",
        },
    )

    assert response.status_code == 200
    assert response.json()["count"] == 4


def test_invalid_domain_rejected():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "finance",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Unknown skill domain.",
    }


def test_skill_public_fields():
    response = client.get(
        "/api/v1/skills",
        params={
            "domain": "business",
        },
    )

    skill = response.json()[
        "skills"
    ][0]

    assert set(skill.keys()) == {
        "name",
        "domain",
        "description",
    }
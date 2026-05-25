from uuid import UUID
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from src.core.constants import ChecklistItemStatus
from src.core.models import Program


def test_applicant_application_flow(
    api_client: TestClient,
    programs: list[Program],
) -> None:
    email = "applicant.flow@example.com"
    password = "Password1234!"

    response = api_client.post(
        "/profiles",
        json={
            "name": "Alice",
            "family_name": "Smith",
            "email": email,
            "password": password,
            "gpa": 3.8,
            "target_term": "2027",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(
        "/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, Any] = response.json()
    access_token = response_data.get("access_token")
    auth_headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/programs", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, Any] = response.json()
    listed_ids = [program.get("id") for program in response_data.get("items")]
    assert str(programs[0].id) in listed_ids
    assert str(programs[1].id) in listed_ids

    target = programs[0]
    response = api_client.post(
        "/applications",
        json={"program_id": str(target.id)},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, Any] = response.json()
    application_id = UUID(response_data.get("id"))

    response = api_client.post(
        "/applications",
        json={"program_id": str(target.id)},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_409_CONFLICT

    response = api_client.get(
        f"/applications/{application_id}",
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    detail_data: dict[str, Any] = response.json()
    assert detail_data["id"] == str(application_id)
    assert detail_data["program"]["id"] == str(target.id)
    assert detail_data["program"]["name"] == target.name
    assert len(detail_data["checklist_items"]) == len(target.requirements)
    assert all(
        item["status"] == ChecklistItemStatus.NOT_STARTED
        for item in detail_data["checklist_items"]
    )
    checklist_item_id = detail_data["checklist_items"][0]["id"]

    response = api_client.get(
        f"/applications/{application_id}/readiness", headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    readiness_data = response.json()

    required_count = sum(1 for r in target.requirements if r.required)
    assert readiness_data["readiness_score"] == 0.0
    assert len(readiness_data["missing_requirements"]) == required_count
    assert len(readiness_data["checklist_items"]) == len(target.requirements)

    response = api_client.get(
        f"/applications/{application_id}/timeline", headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    timeline_before = response.json()
    assert len(timeline_before) == len(target.requirements)
    first_event = timeline_before[0]
    assert "checklist_item" in first_event
    assert "checklist_item_id" not in first_event
    assert isinstance(first_event["checklist_item"], dict)
    assert "id" in first_event["checklist_item"]
    assert "status" in first_event["checklist_item"]

    response = api_client.patch(
        f"/applications/{application_id}/checklist/{checklist_item_id}",
        json={"status": ChecklistItemStatus.COMPLETE},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    updated_item = response.json()
    assert updated_item["id"] == checklist_item_id
    assert updated_item["status"] == ChecklistItemStatus.COMPLETE

    response = api_client.get(
        f"/applications/{application_id}/timeline", headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    timeline_after = response.json()
    assert len(timeline_after) == len(target.requirements)

    response = api_client.get(
        f"/applications/{application_id}/readiness", headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    update_readiness = response.json()

    assert update_readiness["readiness_score"] > 0.0
    assert len(update_readiness["missing_requirements"]) == required_count - 1
    completed_item = next(
        item
        for item in update_readiness["checklist_items"]
        if item["status"] == ChecklistItemStatus.COMPLETE
    )
    assert completed_item is not None

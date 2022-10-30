import json
import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework.reverse import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, category, price, status_code",
    [
        # Passes
        ("Notebook", "Stationary", 5.5, 201),
        # Fails param validation
        ("", "Stationary", 5.5, 400),
        ("Notebook", "", 5.5, 400),
        ("Notebook", "Stationary", "", 400),
    ],
)
def test_create(name, category, price, status_code, api_client):
    response = api_client.post(
        path=reverse("api:item-list"),
        data={
            "name": name,
            "category": category,
            "price": price,
        },
    )
    assert response.status_code == status_code

    # Checks response body only if status is ok
    if response.status_code == 201:
        assert response.json().get("id") is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "dt_from, dt_to, count, status_code",
    [
        # Passes
        (
            (timezone.now() - timedelta(hours=1)).isoformat(),
            (timezone.now() + timedelta(hours=1)).isoformat(),
            2,
            200,
        ),
        (
            (timezone.now() + timedelta(hours=1)).isoformat(),
            (timezone.now() + timedelta(hours=2)).isoformat(),
            0,
            200,
        ),
        # Fails param validation
        (
            "Invalid Datetime",
            (timezone.now() + timedelta(hours=2)).isoformat(),
            None,
            400,
        ),
        (
            (timezone.now()).isoformat(),
            "Invalid Datetime",
            None,
            400,
        ),
    ],
)
def test_list(dt_from, dt_to, count, status_code, create_item, api_client):
    # Seeds DB first
    create_item(name="Notebook", category="Stationary", price=5.5)
    create_item(name="Key Chain", category="Gift", price=3)

    # Uses `.generic()` as `.get()` does not allow request body
    response = api_client.generic(
        method="GET",
        path=reverse("api:item-list"),
        data=json.dumps(
            {
                "dt_from": dt_from,
                "dt_to": dt_to,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == status_code

    # Checks response body only if status is ok
    if response.status_code == 200:
        items = response.json().get("items")
        assert items is not None
        assert len(items) == count


@pytest.mark.django_db
@pytest.mark.parametrize(
    "category, count, status_code",
    [
        # Passes
        ("all", 2, 200),
        ("Gift", 1, 200),
        # Fails param validation
        (None, None, 400),
    ],
)
def test_list(category, count, status_code, create_item, api_client):
    # Seeds DB first
    create_item(name="Notebook", category="Stationary", price=5.5)
    create_item(name="Key Chain", category="Gift", price=3)
    create_item(name="Baggage Cover", category="Gift", price=15)

    # Uses `.generic()` as `.get()` does not allow request body
    response = api_client.generic(
        method="GET",
        path=reverse("api:item-category"),
        data=json.dumps(
            {
                "category": category,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == status_code

    # Checks response body only if status is ok
    if response.status_code == 200:
        items = response.json().get("items")
        assert items is not None
        assert len(items) == count

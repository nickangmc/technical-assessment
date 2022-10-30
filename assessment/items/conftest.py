import pytest
from assessment.items.models import Category, Item


@pytest.fixture
def create_item():
    def make_item(name, category, price):
        _category, _ = Category.objects.get_or_create(name=category)

        # Similarly, updates the item object in DB if exists
        # Creates a new item object otherwise
        item, _ = Item.objects.update_or_create(
            name=name,
            defaults={
                "category": _category,
                "price": price,
            },
        )

        return item

    return make_item

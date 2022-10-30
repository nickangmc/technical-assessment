from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from assessment.items.models import Item, Category

# Request param validators for the view set
# ------------
class ItemListParamValidator(serializers.Serializer):
    dt_from = serializers.DateTimeField()
    dt_to = serializers.DateTimeField()


class ItemCategoryListParamValidator(serializers.Serializer):
    category = serializers.CharField(max_length=255)


# API Serializers
# ------------
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "category", "price"]

    # This foreign-key field returns an ID by default which is not the requirement
    # Therefore we can use SerializerMethodField to return a name instead
    category = serializers.SerializerMethodField()

    # Similarly, this field returns in string format by default, we can overwrite
    # it to convert to Decimal field
    price = serializers.SerializerMethodField()

    def get_category(self, item):
        return item.category.name

    def get_price(self, item):
        return Decimal(item.price)


class ItemCreateSerializer(serializers.Serializer):
    # Request param fields
    name = serializers.CharField(write_only=True, max_length=255)
    category = serializers.CharField(write_only=True, max_length=255)
    price = serializers.DecimalField(
        write_only=True,
        max_digits=19,
        decimal_places=4,
        min_value=Decimal(0),
    )

    # Response fields
    id = serializers.IntegerField(read_only=True, label="ID")

    @transaction.atomic
    def create(self, validated_data):
        # First try to retrieve the category object from DB via name
        # Creates a new category object if not exists
        category, _ = Category.objects.get_or_create(
            name=validated_data.get("category")
        )

        # Similarly, updates the item object in DB if exists
        # Creates a new item object otherwise
        item, _ = Item.objects.update_or_create(
            name=validated_data.get("name"),
            defaults={
                "category": category,
                "price": validated_data.get("price"),
            },
        )

        return {
            "id": item.id,
        }


# Response Serializers
# ------------
class ItemListResponseSerializer(serializers.Serializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    # Wraps the queryset under the key name "items" in the response
    def get_items(self, queryset):
        return ItemSerializer(queryset, many=True).data

    # Calculates the total price from the queryset passed in
    def get_total_price(self, queryset):
        total_price = Decimal(0)

        for item in queryset:
            total_price += Decimal(item.price)

        return total_price


class ItemCategoryListResponseSerializer(serializers.Serializer):
    items = serializers.SerializerMethodField()

    def get_items(self, queryset):
        response = []

        # Aggregrates the info required
        for category in queryset:
            total_price = Decimal(0)
            count = 0

            for item in category.items.all():
                total_price += item.price
                count += 1

            response.append(
                # Customize response structure based on the requirement
                {
                    "category": category.name,
                    "total_price": total_price,
                    "count": count,
                }
            )

        return response

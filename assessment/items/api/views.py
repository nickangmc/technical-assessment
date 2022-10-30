from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from assessment.mixins import SerializerMixin
from assessment.items.models import Category, Item
from assessment.items.api.serializers import (
    ItemSerializer,
    ItemCreateSerializer,
    ItemListParamValidator,
    ItemListResponseSerializer,
    ItemCategoryListParamValidator,
    ItemCategoryListResponseSerializer,
)


class ItemViewSet(
    SerializerMixin,
    viewsets.ModelViewSet,
):
    # Query & Filterings
    queryset = Item.objects.all()

    # Serializers
    serializer_class = ItemSerializer
    serializer_class_per_action = {
        "create": ItemCreateSerializer,
    }

    # Overwrites the `list` method in viewsets.ModelViewSet
    def list(self, request):
        # Validates request params using serializer
        validator = ItemListParamValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        params = validator.validated_data

        # Updates the queryset to be returned in the response
        queryset = Item.objects.filter(
            last_updated_dt__gte=params.get("dt_from"),
            last_updated_dt__lte=params.get("dt_to"),
        )

        serializer = ItemListResponseSerializer(queryset)
        return Response(serializer.data)

    # Creates a new endpoint in viewsets.ModelViewSet: "api/items/category"
    @action(
        methods=["get"],
        detail=False,
        url_path="category",
        url_name="category",
    )
    def list_by_category(self, request):
        # Validates request params using serializer
        validator = ItemCategoryListParamValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        params = validator.validated_data
        category_name = params.get("category")

        # Creates queryset & applies filter if needed
        queryset = Category.objects.all()

        if category_name != "all":
            queryset = queryset.filter(name=category_name)

        # Process & format response
        serializer = ItemCategoryListResponseSerializer(queryset)
        return Response(serializer.data)

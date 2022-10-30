from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from assessment.items.api.views import ItemViewSet
from assessment.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
    
router.register("users", UserViewSet)
router.register("items", ItemViewSet, basename="item")


app_name = "api"
urlpatterns = router.urls

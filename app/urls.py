from django.urls import path, include
from .views import ProductViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register("products", ProductViewSet, basename="products")

urlpatterns = [path("", include(router.urls))]

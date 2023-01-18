from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import BlogViewSet, ImageViewSet

router = DefaultRouter()

router.register('blogs', BlogViewSet)

nested_router = NestedDefaultRouter(router,'blogs', lookup = "blog")
nested_router.register('images', ImageViewSet, basename="blog-images")

urlpatterns = router.urls + nested_router.urls


from rest_framework.routers import DefaultRouter

from .views import BlogViewSet

router = DefaultRouter()

router.register('blogs', BlogViewSet)

urlpatterns = router.urls


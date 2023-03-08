from rest_framework.routers import DefaultRouter

from .views import BlogViewSet

router = DefaultRouter()

router.register("blogs", BlogViewSet, basename="blogs")


urlpatterns = router.urls

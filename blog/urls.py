from rest_framework.routers import DefaultRouter

from .views import BlogViewSet

router = DefaultRouter(trailing_slash=False)

router.register("blogs", BlogViewSet, basename="blogs")


urlpatterns = router.urls

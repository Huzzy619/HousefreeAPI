from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import ApartmentViewSet, MediaViewSet, PicturesViewSet, ReviewViewSet, BookmarkView

router = DefaultRouter()

router.register("apartment", ApartmentViewSet, basename="apartments")

nested_router = NestedDefaultRouter(router, "apartment", lookup="apartment")

nested_router.register("media", MediaViewSet, basename="apartment_media")
nested_router.register("pictures", PicturesViewSet, basename="apartment_pictures")
nested_router.register("reviews", ReviewViewSet, basename="apartments_reviews")


from django.urls import path

urlpatterns = [
    path('bookmark/', BookmarkView.as_view())
] + router.urls + nested_router.urls

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


from .views import (
    ApartmentViewSet,
    BookmarkView,
    MediaViewSet,
    PicturesViewSet,
    ReviewViewSet,
    hello,
)

router = DefaultRouter()

router.register("apartment", ApartmentViewSet, basename="apartments")

nested_router = NestedDefaultRouter(router, "apartment", lookup="apartment")

nested_router.register("videos", MediaViewSet, basename="apartment-videos")
nested_router.register("pictures", PicturesViewSet, basename="apartment-pictures")
nested_router.register("reviews", ReviewViewSet, basename="apartments-reviews")


from django.urls import path

urlpatterns = (
    [path("bookmark/", BookmarkView.as_view()), path("hello/", hello)]
    + router.urls
    + nested_router.urls
)

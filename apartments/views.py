from core.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Apartment, Media, Picture, Review
from .permissions import IsAgent
from .serializers import *



class ApartmentViewSet(ModelViewSet):
    """
        Agent can create apartment and also make edits to previously uploaded apartments

        Apartments can be searched by its location, price, category and title.

        
        It can also be filtered based on any these attributes.

        Args:
            ModelViewSet (_type_): _description_

        Returns:
            _type_: _description_
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["location", "price", "category"]
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsOwner, IsAgent]
    search_fields = ["location", "price", "category", "title"]
    ordering_fields = ["category"]

    @action(methods=["GET"], permission_classes=[IsOwner], detail=False)
    def mine(self, request):
        """
        Returns all the apartments owned by the currently logged in agent

        """
        my_apartments = Apartment.objects.filter(agent=self.request.user)
        # (
            
        #     # .order_by("-date_created")
        #     # .select_related("reviews", "pictures", "videos")
        # )


        serializer = ApartmentSerializer(my_apartments, many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ApartmentSerializer
        return CreateApartmentSerializer

    def get_serializer_context(self):
        return {"user": self.request.user, 'request':self.request}

    def get_queryset(self):
        return Apartment.objects.all()#.select_related("reviews", "pictures", "videos")


class PicturesViewSet(ModelViewSet):
    """
    Pictures of the apartment can be uploaded

    Args:
        The apartment_id

    """
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Picture.objects.all()
    permission_classes = [ IsAgent]
    serializer_class = PictureSerializer

    def get_queryset(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return Picture.objects.filter(apartment_id=pk)
        return super().get_queryset()

    def get_serializer_context(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return {"apartment_pk": pk, 'request':self.request}
        return super().get_serializer_context()


class MediaViewSet(ModelViewSet):

    """
    Short video clips of the apartment can be uploaded

    Replaced and removed 

    Args:
        The apartment_id


    """
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Media.objects.all()
    permission_classes = [IsOwner, IsAgent]
    serializer_class = MediaSerializer

    def get_queryset(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return Media.objects.filter(apartment_id=pk)
        return super().get_queryset()

    def get_serializer_context(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return {"apartment_pk": pk, 'request':self.request}
        return super().get_serializer_context()


class ReviewViewSet(ModelViewSet):
    """
    Agents and other users can leave reviews on apartments

    They can update and delete their reviews

    
    """
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return Review.objects.filter(apartment_id=pk)
        return super().get_queryset()

    def get_serializer_context(self):
        if pk := self.kwargs.get("apartment_pk", ""):
            return {"apartment_pk": pk, "user": self.request.user}
        return super().get_serializer_context()


from dj_rest_auth.views import PasswordResetView
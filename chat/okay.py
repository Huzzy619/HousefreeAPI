from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationSerializer


class InitiateConverastion(APIView):
    serializer_class = ConversationSerializer

    def post(self, request):

        data = request.data
        username = data.pop("username")
        try:
            participant = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "You cannot chat with a non existent user"})

        conversation = Conversation.objects.filter(
            Q(initiator=request.user, receiver=participant)
            | Q(initiator=participant, receiver=request.user)
        )
        if conversation.exists():
            return redirect(reverse("get_conversation", args=(conversation[0].id,)))
        else:
            conversation = Conversation.objects.create(
                initiator=request.user, receiver=participant
            )
            return Response(ConversationSerializer(instance=conversation).data)


class GetConversation(APIView):
    serializer_class = ConversationSerializer

    def get(self, request, convo_id):
        conversation = Conversation.objects.filter(id=convo_id)
        if not conversation.exists():
            return Response({"message": "Conversation does not exist"})
        else:
            serializer = ConversationSerializer(instance=conversation[0])
            return Response(serializer.data)


class Conversation(APIView):
    def get(self, request):
        conversation_list = Conversation.objects.filter(
            Q(initiator=request.user) | Q(receiver=request.user)
        )
        serializer = ConversationListSerializer(instance=conversation_list, many=True)
        return Response(serializer.data)




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('start/', views.InitiateConverastion.as_view(), name='start_convo'),
#     path('<int:convo_id>/', views.GetConversation.as_view(), name='get_conversation'),
#     path('', views.Conversation.as_view(), name='conversations')
# ]
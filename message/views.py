import os

# import environ
import socketio
from asgiref.sync import sync_to_async
from core.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from mailjet_rest import Client
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, Room, generate_short_id
from .serializers import ContactUsSerializer, MessageSerializer, message_serializer

api_key = settings.MJ_API_KEY
api_secret = settings.MJ_API_SECRET
redis_url = settings.REDIS_URL


mgr = socketio.AsyncRedisManager(redis_url)
sio = socketio.AsyncServer(
    async_mode="asgi", client_manager=mgr, cors_allowed_origins="*"
)
# Create your views here.
# establishes a connection with the client
@sio.on("connect")
async def connect(sid, env, auth):
    if auth:
        room_id = auth["room_id"]
        print("SocketIO connect")
        sio.enter_room(sid, room_id)
        await sio.emit("connect", f"Connected as {sid}")
    else:
        room_id = "VGTXC7NJY"
        print("SocketIO connect")
        sio.enter_room(sid, room_id)
        await sio.emit("connect", f"Connected as {sid}")


# communication with orm
def store_and_return_message(data):
    data = data
    if "room_id" in data:
        room_id = data["room_id"]
    else:
        room_id = "VGTXC7NJY"
    room = Room.objects.get(room_id=room_id)
    instance = Message.objects.create(
        room=room,
        author=data["author"],
        content=data["content"],
        short_id=generate_short_id(),
    )
    instance.save()
    message = message_serializer(instance)
    return message


# listening to a 'message' event from the client
@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    print(data)
    message = await sync_to_async(store_and_return_message, thread_sensitive=True)(
        data
    )  # communicating with orm
    print(message)
    await sio.emit("new_message", message, room=message["room_id"])


class GetUserMessages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, email):
        user = get_object_or_404(User, email=email)
        room = get_object_or_404(Room, user=user)
        messages = room.messages
        serializer = MessageSerializer(messages, many=True)
        response = {}
        response["room_id"] = room.room_id
        response["messages"] = serializer.data
        return Response(response, status=status.HTTP_200_OK)


# class Contact_Us(APIView):

#     """
#     A contact us form which uses mailjet as a mail library
#     Args:
#         data- a request data which contains a sender and the message body
#     """

#     permission_classes = [AllowAny]

#     @swagger_auto_schema(request_body=ContactUsSerializer)
#     def post(self, request):
#         serializer = ContactUsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         sender = serializer.validated_data["sender"]
#         message = serializer.validated_data["message"]
#         mailjet = Client(auth=(api_key, api_secret), version="v3.1")
#         data = {
#             "Messages": [
#                 {
#                     "From": {"Email": f"{sender}", "Name": "Me"},
#                     "To": [{"Email": "free_house@yahoo.com", "Name": "You"}],
#                     "Subject": "Contact Form Mail",
#                     "TextPart": "Greetings from Mailjet!",
#                     "HTMLPart": f"<h3>{message}</h3>",
#                 }
#             ]
#         }
#         result = mailjet.send.create(data=data)
#         return Response(result.json(), status=status.HTTP_201_CREATED)

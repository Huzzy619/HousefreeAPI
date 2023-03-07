from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user).order_by('-date_created')
        return queryset

class MarkNotificationAsReadAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.read = True
            notification.save()
            return Response({'detail': 'Notification marked as read.'})
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)

class NotificationDeleteView(APIView):
    def delete(self, request, notification_id, format=None):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
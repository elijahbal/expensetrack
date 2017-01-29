from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from .permissions import RecordManagementDetailLevel, RecordManagementListLevel
from .permissions import UserManagementDetailLevel, UserManagementListLevel


from restbook.models import Record
from restbook.serializers import RecordSerializer, UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'records': reverse('record-list', request=request, format=format)
    })

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class RecordListGeneric(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (RecordManagementListLevel,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user and not user.is_staff:
            return Record.objects.filter(owner_id=user.id)
        else:
            return Record.objects.all()

    def perform_create(self, serializer):
        serializer.save( owner=self.request.user )


class RecordDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (RecordManagementDetailLevel,)

class UserListGeneric(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserManagementListLevel,)


class UserDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserManagementDetailLevel,)


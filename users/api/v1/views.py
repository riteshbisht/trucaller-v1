
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from users.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, RerieveProfileSerializer, MarkNumberspamSerializer, SearchSerializer, AddContactSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend, FilterSet


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RerieveProfileApiView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = User.objects.all()
    serializer_class = RerieveProfileSerializer
    lookup_field = "mobile"

    def get(self, request, *args, **kwargs):
        self.kwargs['mobile'] = request.user.mobile
        return super(RerieveProfileApiView, self).get(request, *args, **kwargs)


class SearchApiView(ListAPIView):
    authentication_classes = (JWTAuthentication, )
    queryset = User.objects.all()
    serializer_class = SearchSerializer
    filter_fields = ['first_name',]
    filter_backends = (DjangoFilterBackend,)



class MarkNumberSpamApiView(CreateAPIView):
    serializer_class = MarkNumberspamSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)


class AddContactForUserApiView(CreateAPIView):
    serializer_class = AddContactSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )


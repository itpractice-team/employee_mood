import uuid

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import InviteCode, User

from .serializers import (RegisterSerializer, SendInviteSerializer,
                          UserSerializer)
from .utils import encode_data, send_code


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = (
        User.objects
        .select_related('department', 'position')
        .prefetch_related('hobbies')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'first_name', 'last_name',
                        'role', 'department', 'position')
    http_method_names = ('get', 'patch')


class SendInviteView(APIView):
    '''Отправка ссылки для регистрации на почту'''

    @swagger_auto_schema(
        request_body=SendInviteSerializer,
        operation_id='users_send_invite'
    )
    def post(self, request):
        serializer = SendInviteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email)

        if user.exists():
            return Response(
                {'result': 'Пользователь с таким email уже зарегистрирован'},
                status=status.HTTP_400_BAD_REQUEST
            )

        invite_code = InviteCode.objects.filter(email=email)
        uuid_code = uuid.uuid4()
        encode_uuid = encode_data(settings.INVITE_SECRET_KEY, str(uuid_code))

        if invite_code.exists():
            invite_code.update(code=uuid_code)
            send_code(email=email, code=encode_uuid, again=True)
            return Response(
                {'result': 'Ссылка отправлена повторно'},
                status=status.HTTP_200_OK
            )
        else:
            InviteCode.objects.create(email=email, code=uuid_code)
            send_code(email=email, code=encode_uuid)
            return Response(
                {'result': 'Ссылка для регистрации отправлена на email'},
                status=status.HTTP_201_CREATED
            )

# SOON


class RegisterView(APIView):

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_id='users_register'
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'result': 'угу'},
            status=status.HTTP_201_CREATED
        )
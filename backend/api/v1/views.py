import uuid

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import InviteCode, User

from .serializers import SendInviteSerializer, UserSerializer


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
    '''Регистрация пользователя и отправка инвайта почту'''

    @swagger_auto_schema(request_body=SendInviteSerializer)
    def post(self, request):
        serializer = SendInviteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email)

        if not user.exists():
            User.objects.create(email=email, is_active=False)
            InviteCode.objects.create(email=email)
            return Response(
                {'result': 'Пользователь создан. Инвайт отправлен на почту'},
                status=status.HTTP_200_OK
            )
        elif user.exists() and user.first().is_active:
            return Response(
                {'result': 'Пользователь уже существует и активирован.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            code = uuid.uuid4()
            InviteCode.objects.filter(email=email).update(code=code)
            return Response(
                {'result': 'Инвайт отправлен повторно.'},
                status=status.HTTP_200_OK
            )

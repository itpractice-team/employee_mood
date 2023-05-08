from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.select_related(
        'department', 'position').prefetch_related('hobbies')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'first_name', 'last_name',
                        'role', 'department', 'position')

    @swagger_auto_schema(operation_id='Список пользователей')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

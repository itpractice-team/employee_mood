from rest_framework import serializers
from users.models import Department, User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    position = PositionSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'position',
                  'department', 'avatar', 'about', 'phone', 'date_joined')

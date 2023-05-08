from rest_framework import serializers
from users.models import Department, Hobby, Position, User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    position = PositionSerializer()
    hobbies = HobbySerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role', 'position',
            'department', 'hobbies', 'avatar', 'about', 'phone', 'date_joined')

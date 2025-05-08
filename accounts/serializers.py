from rest_framework import serializers
from .models import User
from employee.models import Employee
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'department']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    employee_name = serializers.CharField(required=False)
    employee_phone = serializers.CharField(required=False)
    employee_address = serializers.CharField(required=False)
    employee_join_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'department',
                  'employee_name', 'employee_phone', 'employee_address', 'employee_join_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # 验证两次密码是否一致
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # 如果角色是employee，确保提供了员工信息
        if data.get('role') == 'employee' and (
                not data.get('employee_name') or
                not data.get('employee_phone') or
                not data.get('employee_address') or
                not data.get('employee_join_date')
        ):
            raise serializers.ValidationError(
                {"employee_info": "Employee information is required for employee role."}
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        # 移除password2字段
        validated_data.pop('password2')

        # 提取员工信息
        employee_name = validated_data.pop('employee_name', None)
        employee_phone = validated_data.pop('employee_phone', None)
        employee_address = validated_data.pop('employee_address', None)
        employee_join_date = validated_data.pop('employee_join_date', None)

        # 创建用户
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # 如果是员工角色，创建关联的员工记录
        if user.role == 'employee' and employee_name:
            Employee.objects.create(
                name=employee_name,
                email=user.email,
                phone=employee_phone,
                address=employee_address,
                join_date=employee_join_date,
                department=user.department,
                user=user
            )

        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords must match."})
        return data
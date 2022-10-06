from rest_framework import serializers

from apps.mentors.models import CustomUser
from apps.payments.models import Package, RegisterRequest, UserMembership, RegisterRequestPayment


class PackageListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Package
        fields = ['id', 'title', 'description', 'price', 'type']

    def get_type(self,obj):
        return obj.get_type_display()


class RegisterRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequest
        fields = ['id', 'full_name', 'phone', 'email',
                  'package_membership']


class MembershipDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequest
        fields = ('type', 'status', 'paid_price', 'expire_date')


class UserMembershipSerializer(serializers.ModelSerializer):
    register_request = MembershipDetailSerializer(read_only=True)

    class Meta:
        model = UserMembership
        fields = ('register_request',)


class UserMembershipDetailSerializer(serializers.ModelSerializer):
    user_membership = UserMembershipSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('user_membership',)


class RegisterRequestAfterPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequestPayment
        fields = ('paid_date', 'expire_date', 'type', 'paid_price', 'is_paid')


class RgObject(serializers.Serializer):
    register_request = serializers.IntegerField(label='ID')


class RG_User_lvl_Serializer(serializers.ModelSerializer):
    rg_payments = RegisterRequestAfterPaymentSerializer(many=True, read_only=True)
    class Meta:
        model = RegisterRequest
        fields = ('rg_payments',)


class UserNestedMembershipSerializer(serializers.ModelSerializer):
    register_request = RG_User_lvl_Serializer(read_only=True)
    class Meta:
        model = UserMembership
        fields = ('register_request',)


class UserPaymentsInfoSerializer(serializers.ModelSerializer):
    user_membership = UserNestedMembershipSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('user_membership',)
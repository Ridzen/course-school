from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from apps.mentors.models import CustomUser
from apps.payments.models import Package, RegisterRequest, RegisterRequestPayment
from apps.payments.serializers import PackageListSerializer, UserMembershipDetailSerializer, RgObject, \
    UserPaymentsInfoSerializer
from apps.payments.utils import get_subscription_period


class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


class UserMembershipDetaiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserMembershipDetailSerializer


class SuccessfullPayment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        rg_data = RgObject(data=request.data)
        if rg_data.is_valid(raise_exception=True):
            import datetime
            todays_date = datetime.date.today()
            rg = get_object_or_404(RegisterRequest, id=rg_data.validated_data.get('register_request'))
            end_date = get_subscription_period(rg.type, todays_date)
            rg.is_paid = 1
            rg.paid_date = todays_date
            rg.expire_date = end_date
            rg.save()
            # create payments for rg
            rg_payment = RegisterRequestPayment.objects.create(
                register_request=rg, paid_date=todays_date, expire_date=end_date,
                type=rg.type, paid_price=rg.paid_price, is_paid=1
            )
            data = {
                'register_request':rg_payment.register_request.id,
                'paid_date': rg_payment.paid_date, 'expire_date': rg_payment.expire_date, 'type':rg_payment.type,
                'paid_price': rg_payment.paid_price, 'is_paid': rg_payment.is_paid
            }
            return Response(data)


class UserPayments(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPaymentsInfoSerializer



from django.urls import re_path, include, path

from .views import RegistrationAPIView, LoginAPIView, UserProfileUpdateView
from ..payments.views import UserPayments, UserMembershipDetaiView, SuccessfullPayment

urlpatterns = [
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    path('user-profile/<int:pk>/',
         UserProfileUpdateView.as_view(), name='user-profile'),

    path('user-payments/<int:pk>/',
         UserPayments.as_view(), name='user-payments'),
    path('user-membership/<int:pk>/',
         UserMembershipDetaiView.as_view(), name='user-membership'),

]
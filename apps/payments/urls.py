from django.urls import path
from . import views
from .views import UserPayments, UserMembershipDetaiView, SuccessfullPayment

urlpatterns = [
    path('package-list/', views.PackageListView.as_view(), name='package_list'),
    path('user-payments/<int:pk>/',
         UserPayments.as_view(), name='user-payments'),
    path('user-membership/<int:pk>/',
         UserMembershipDetaiView.as_view(), name='user-membership'),

    # after payment requests
    path('after-reqister-request-payment/', SuccessfullPayment.as_view(), name='after-pay')
]

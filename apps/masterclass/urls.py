from django.urls import path
from apps.masterclass import views


urlpatterns = [
    path('masterclass/', views.MasterClassListView.as_view(),),
    path('masterclass/<int:pk>/', views.MasterClassDetailView.as_view())
]

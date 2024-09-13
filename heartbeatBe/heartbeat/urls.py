from django.urls import path
from .views import UrlAPIView

urlpatterns = [
    path('urls/', UrlAPIView.as_view(), name="urls-list"),
    path('urls/<int:pk>', UrlAPIView.as_view(), name="urls-detail"),
]
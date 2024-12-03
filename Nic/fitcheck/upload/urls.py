from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_images, name='upload_images'),  # Upload form
    path('result/', views.result, name='result'),         # Result page
]

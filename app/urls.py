from django.urls import path
from . import views

urlpatterns = [
    path('sound/<uuid>/', views.GetSound.as_view(), name='post_list'),
]

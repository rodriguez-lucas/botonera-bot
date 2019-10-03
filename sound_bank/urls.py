from django.urls import path
from . import views

urlpatterns = [
    path('sound/<uuid>/<title>', views.GetSound.as_view(), name='post_list'),
]

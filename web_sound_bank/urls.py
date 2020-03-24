from django.contrib import admin
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from web_sound_bank.views import SoundsList, GetSound, LoginView, UploadSound, LogoutView, PingView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('sounds')), name='home'),
    path('admin/', admin.site.urls),
    path('sounds', SoundsList.as_view(), name='sounds'),
    path('upload-sound', UploadSound.as_view(), name='upload-sound'),
    path('sound/<sound_id>/<title>', GetSound.as_view(), name='sound'),
    path('login/<token>', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login-required', TemplateView.as_view(template_name='login-required.html'), name='login-required'),
    path('ping/', PingView.as_view(), name='login-required'),
]

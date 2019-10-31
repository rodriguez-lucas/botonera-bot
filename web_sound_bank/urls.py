from django.contrib import admin
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from web_sound_bank.views import SoundsList, GetSound

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('sounds')), name='home'),
    path('admin/', admin.site.urls),
    path('sounds', SoundsList.as_view(), name='sounds'),
    path('sound/<sound_id>/<title>', GetSound.as_view(), name='sound'),
]

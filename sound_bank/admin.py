from django.contrib import admin
from sound_bank.models import SoundBankUser, Sound, SoundRank

admin.site.register(SoundBankUser)
admin.site.register(Sound)
admin.site.register(SoundRank)

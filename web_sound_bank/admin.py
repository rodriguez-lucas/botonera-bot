from django.contrib import admin
from web_sound_bank.models import User, Sound, SoundRank, UserLoginToken

admin.site.register(User)
admin.site.register(Sound)
admin.site.register(SoundRank)
admin.site.register(UserLoginToken)

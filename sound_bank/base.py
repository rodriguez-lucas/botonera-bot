from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from sound_bank.models import Sound, SoundBankUser, SoundRank


class SoundBankException(Exception):
    pass


class SoundBank:
    def sound_from_uuid(self, uuid):
        try:
            return Sound.objects.get(_uuid=uuid)
        except(Sound.DoesNotExist, ValidationError):
            raise SoundBankException("Sound not found for uuid: {}".format(uuid))

    def last_added_sound(self):
        if Sound.objects.count() is 0:
            raise SoundBankException("Can't return last sound because there is no sounds")
        return Sound.objects.last()

    def register_or_get_user(self, user_id, username, first_name='', last_name=''):
        return SoundBankUser.objects.get_or_create(_user_id=user_id, _username=username, _first_name=first_name,
                                                   _last_name=last_name)

    def user_add_sound(self, user, sound_title, sound_key_words, sound_binary_data, upload_datetime):
        Sound.objects.create(_title=sound_title, _key_words=sound_key_words, _bin=sound_binary_data,
                             _uploader=user, _upload_datetime=upload_datetime)

    def user_listened_sound(self, user, sound):
        sound_rank = SoundRank.objects.get_or_create(_user=user, _sound=sound)
        sound_rank.inc_sound_count()
        sound_rank.save()

    def sounds_for_user(self, user, query):
        sound_approved_or_sound_uploaded_by_user = Q(_approved=True) | Q(_uploader=user)
        query_matches_sound = Q(_title__icontains=query) | Q(_key_words__icontains=query)
        orm_filter = Q(sound_approved_or_sound_uploaded_by_user & query_matches_sound)

        sounds = Sound.objects.filter(orm_filter).annotate(listened_count=Coalesce(Sum('_rank___listened_count'), 0))
        sounds_ordered = sounds.order_by('-listened_count')

        listened_sounds_ordered = user.listened_sounds_descending_order()

        return listened_sounds_ordered + [sound for sound in sounds_ordered if sound not in listened_sounds_ordered]

    def all_sounds(self):
        return Sound.objects.all()

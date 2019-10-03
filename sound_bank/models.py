import uuid

from django.db import models


class SoundBankUser(models.Model):
    _user_id = models.CharField(max_length=100, unique=True)
    _username = models.CharField(max_length=100)
    _first_name = models.CharField(max_length=100, blank=True, null=True)
    _last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self._username

    def listened_sounds_descending_order(self):
        sound_ids = self._sound_rank.all().order_by('-_listened_count').values_list('_sound__id', flat=True)
        return [Sound.objects.get(id=sound_id) for sound_id in sound_ids]


class Sound(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    _title = models.CharField(max_length=100)
    _key_words = models.TextField(blank=True)
    _bin = models.BinaryField()

    # fixme: these props should live in another model / db table
    _approved = models.BooleanField(default=False)
    _upload_datetime = models.DateTimeField(null=True, blank=True)
    _uploader = models.ForeignKey(SoundBankUser, related_name='uploaded_sounds', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self._title

    def binary_data(self):
        return self._bin

    def upload_datetime(self):
        return self._upload_datetime

    def uuid(self):
        return self._uuid

    def title(self):
        return self._title


class SoundRank(models.Model):
    _user = models.ForeignKey(SoundBankUser, related_name='_sound_rank', on_delete=models.CASCADE)
    _sound = models.ForeignKey(Sound, on_delete=models.CASCADE, related_name='_rank')
    _listened_count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['_user', '_sound'], name='sound rank constraint')]

    def __str__(self):
        return '{} | {}'.format(self._sound, self._listened_count)

    def inc_sound_count(self):
        self._listened_count += 1

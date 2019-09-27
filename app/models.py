import uuid

from django.db import models


class BotUser(models.Model):
    _telegram_id = models.CharField(max_length=100)
    _username = models.CharField(max_length=100)
    _first_name = models.CharField(max_length=100)
    _last_name = models.CharField(max_length=100)

    def __str__(self):
        return self._username


class Sound(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    _title = models.CharField(max_length=100)
    _key_words = models.TextField(blank=True)
    _bin = models.BinaryField()
    _upload_datetime = models.DateTimeField(null=True, blank=True)
    _uploader = models.ForeignKey(BotUser, related_name='uploaded_sounds', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self._title

    def binary_data(self):
        return self._bin

    def upload_datetime(self):
        return self._upload_datetime


class SoundRank(models.Model):
    _bot_user = models.ForeignKey(BotUser, related_name='sent_sounds', on_delete=models.CASCADE)
    _sound = models.ForeignKey(Sound, on_delete=models.CASCADE)
    _sent_count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['_bot_user', '_sound'], name='sound rank constraint')]
